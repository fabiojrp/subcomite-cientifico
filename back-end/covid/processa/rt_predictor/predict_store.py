import pandas as pd
import numpy as np
import datetime
import pickle
import os
from tensorflow import keras
from covid.processa.rt_predictor.dao import get_ml_data, get_engine
from covid.processa.rt_predictor.helper import predict_from_date
from covid.processa.dados.tabelas import Tabelas
# from tabelas import Tabelas


class predict_store:
    def __init__(self):
        # ------------------------------------------------------------------------------------------
        # Carregar modelo, dicionário e estatísticas
        # ------------------------------------------------------------------------------------------
        model_dir = os.getcwd() + '/covid/processa/rt_predictor/'
        model = keras.models.load_model(model_dir + '/keras_model.h5', compile=False)

        scaler_dict = pickle.load(open(model_dir + 'model/scalers.dict', "rb"))
        encoder_dict = pickle.load(open(model_dir + 'model/encoders.dict', "rb"))
        df_y_pred_stats = pd.read_csv(model_dir + 'model/df_y_pred_stats.csv')

        # ------------------------------------------------------------------------------------------
        # Obter os dados
        # ------------------------------------------------------------------------------------------

        P_df = get_ml_data()
        max_data = P_df.data.max().strftime('%Y-%m-%d')

        # ------------------------------------------------------------------------------------------
        # Realizar a predição
        # ------------------------------------------------------------------------------------------

        df_y = predict_from_date(
            model, scaler_dict, encoder_dict, P_df, max_data, df_y_pred_stats)

        # ------------------------------------------------------------------------------------------
        # Escreve em uma tabela da base de dados
        # ------------------------------------------------------------------------------------------
        table_name = 'rt_regional_prediction'
        df_y['created_at'] = pd.to_datetime(
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        # print(df_y)

        tabelas = Tabelas()
        # Busca na listas os munícipios e substitui pelo código do IBGE
        df_y['regional_saude'] = df_y['regional_saude'].replace(
            tabelas.regionais_rt)

        df_y.to_sql(table_name, get_engine(), if_exists="replace", index=False)


if __name__ == "__main__":
    predict_store()
