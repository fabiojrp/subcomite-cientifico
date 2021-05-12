from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime
from .processaRegião import processaRegiao
from .dao.Dao_RT import Dao_RT
from .dao.Database import Database


class atualizaPlanilhaRT:

    def __init__(self):
        self.db = Database.get_instance()
        self.dados = []
        self.dao_rt = Dao_RT()

    def processaDatas(self, regional):
        dados = []
        rows = self.dao_rt.buscaDatas()

        dados.append(processaRegiao.buscaNomeRegiaoPlanilha(regional))
        dados.append(processaRegiao.buscaCampusRegiaoPlanilha(regional))

        for i in rows:
            dados.append(i[0].strftime("%-m/%-d/%Y"))

        return dados

    @staticmethod
    def processaRegionais(self):

        self.dados.append(self.processaDatas(0))

        for regional in range(1, 18):
            dados_aux = []

            dados_aux.append(processaRegiao.buscaNomeRegiaoPlanilha(regional))
            dados_aux.append(
                processaRegiao.buscaCampusRegiaoPlanilha(regional))

            dados_regional = self.dao_rt.buscaDadosRegionais((regional,))

            for dia in dados_regional:
                try:
                    dados_aux.append(float("{:.5f}".format(dia[2])))
                except Exception as error:
                    dados_aux.append(None)

            self.dados.append(dados_aux)

    def carregaPlanilhaRt(self):

        self.processaRegionais(self)

        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1b10MGhVllH0derU31KoldkQ6LyGjhWGdKm_6KBr_xIU'
        SAMPLE_RANGE_NAME = 'rt_regioes!a1'

        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/subcomite-cientifico/back-end/covid/processa/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

        value_input_option = 'USER_ENTERED'

        value_range_body = {
            'values': list(self.dados),
            'majorDimension': 'COLUMNS',
            'range': ''
        }

        request = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                         range=SAMPLE_RANGE_NAME, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()

        SAMPLE_RANGE_NAME = 'rt_regioes2!A1'

        value_range_body = {
            'values': list(self.dados),
            'majorDimension': 'ROWS',
            'range': ''
        }

        request = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                         range=SAMPLE_RANGE_NAME, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()


att = atualizaPlanilhaRT()

att.carregaPlanilhaRt()
