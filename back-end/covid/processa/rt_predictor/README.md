# Modelo Preditivo de RT   

# Instalação

1. Clone Repo

```bash
$ git clone https://git.ifsc.edu.br/andres.ferrero/ifc-covid19-rt_predictor.git
$ cd ifc-covid19-analytics
```

2. Configuração de acesso à base de dados no arquivo: `dao.py` (atualizar com os dados do servidor local)
   
```python
config = {
    "host" : "localhost",
    "port" : 5432,
    "dbname" : "covid",
    "user" : "postgres",
    "password" : "postgres"
}
```

3. Criar um ambiente virtual, ativar ele e instalar as dependências

```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

4. Executar o script `predict_store.py` para realizar as predições e criar uma tabela no banco de dados `rt_regionais_predictions`.