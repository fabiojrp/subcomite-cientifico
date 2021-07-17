import pandas as pd
import numpy as np
import datetime
import os

# ------------------------------------------------------------------------------------------
# Inicializar variáveis
# ------------------------------------------------------------------------------------------

# Número de dias no inicio da séries que serão removidos
n_remove_firsts = 10
# Número de dias do passado que serão usados para predição em uma instância
n_lag = 14
# Núemro de dias do futuro que serãopreditos
n_seq = 5
# Número de instâncias de teste
n_test = 40

# Sobre os dados
# Features numéricas
input_numeric_features = ['rt','obitos_por_semana/100k','casos_por_semana/100k','weekend','holiday']
# Features categóricas (não inclui as binárias)
input_categorical_features = ['regional_saude']
# Feature que define grupos de séries
group_name = 'regional_saude'
# Objetivo preditivos (y)
output_features = ['rt']


def transform_input_to_numpy(data, n_lag):  
  n_samples, n_dim = data.shape
  n_features = n_dim // n_lag 
  c = data.to_numpy().reshape((n_samples, n_features, n_lag))
  c = c.transpose((0,2,1))
  return c

def predict_from_date(model, scaler_dict, encoder_dict, df, date, df_y_pred_stats):
    df['data'] = pd.to_datetime(df['data'])    
    df['weekend'] = np.where( df['data'].dt.dayofweek < 5, 0, 1)
    
    df_feriados = pd.read_csv(os.getcwd() + '/back-end/covid/processa/rt_predictor/feriados.csv')
    df_feriados['data'] = pd.to_datetime(df_feriados['data'])

    df['holiday'] = df.merge(df_feriados[['data','feriado']], how='left', on='data')['feriado'].fillna(0)
    range_x = pd.date_range( start=pd.to_datetime(date) - datetime.timedelta(n_lag-1), end=pd.to_datetime(date))
    range_y = pd.date_range( start=pd.to_datetime(date) + datetime.timedelta(1), end=pd.to_datetime(date) + datetime.timedelta(n_seq))
   
    df = df[df['data'].isin(range_x)].copy()
    
    data = pd.DataFrame()
    
    for feature_name in input_numeric_features:               
        df_encoded = pd.DataFrame(
            scaler_dict[feature_name].transform(df[[feature_name]]),
            columns=[feature_name]
        )        
        data = pd.concat([data, df_encoded], axis=1)

    for feature_name in input_categorical_features:
        df_encoded = pd.DataFrame(
            encoder_dict[feature_name].transform(df[[feature_name]]),
            columns=encoder_dict[feature_name].get_feature_names([feature_name])
        )
        data = pd.concat([data, df_encoded], axis=1)   
    
    group_name = 'regional_saude'    
    data[group_name] = df[group_name].values    
    
    X_ = pd.DataFrame()
    groups = data[group_name].unique()
    for group in groups:
        df_group = data[data[group_name] == group].drop(columns=group_name)              
        values = []    
        for feature_name in df_group.columns:
            values = np.concatenate( (values, df_group[feature_name].values) )
        X_ = X_.append(pd.DataFrame([values]))
    
    X = transform_input_to_numpy(X_, n_lag)
    
    y = model.predict(X).squeeze()
    
    y = scaler_dict[output_features[0]].inverse_transform(y).squeeze()    
    
    df_y = pd.DataFrame()
    import scipy.stats as st
    IC_95 = st.norm.ppf(.95) * df_y_pred_stats['error_std'].values
    
    for i in range(len(groups)):
        group = groups[i]
        group_pred = y[i]
        df_group = pd.DataFrame({
            group_name : group,
            'data' : range_y,
            'pred' : group_pred,
            'pred_IC_95_inf' : group_pred - IC_95,
            'pred_IC_95_sup' : group_pred + IC_95
            })
        df_y = df_y.append(df_group)
        
    return df_y
