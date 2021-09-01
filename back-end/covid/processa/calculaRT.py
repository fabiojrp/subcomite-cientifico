from scipy.stats import gamma
from covid.processa.dao.TestadorBD import TestadorBD
from covid.processa.dao.Database import Database
from covid.processa.db.create import Create
from covid.processa.processaRegiao import processaRegiao
import time
# from salvarDataframe import salvarDataframe


class calculaRT:

    def __init__(self):
        # CLASSE COM MÉTODOS PARA CRIAÇÃO, INSERÇÃO E SELEÇÃO DE VALORES
        self.bd = TestadorBD()
        create = Create()
        create.create_rt()

        # CODIGO REGIONAL, MUNICIPIO
        self.regional_saude = 0
        self.codigo_ibge_municipio = 0

        # DEMAIS VARIAVEIS
        self.StartEstimateDate = 0
        self.MeanSI = 0
        self.sdSI = 0
        self.aPrior = 0
        self.bPrior = 0
        self.TimeMax = 0
        self.TimePeriodNb = 0
        self.MeanPrior = 0
        self.StdPrior = 0
        self.CVThreshold = 0
        self.CumulIncThreshold = 0
        self.NbTimePeriods = 0
        self.MeanSIFinal = 0.0
        self.sdSIFinal = 0.0
        self.SampleSizeSI = 0
        self.SampleSizeR = 0

        self.TimeMin = 1

        self.CustomTimeSteps = ''

        self.StopNow = False
        self.isCompletlyRT = True

        # CONFIGURAÇÕES
        self.SIuncertainty = "N"
        self.parametricSI = "Y"

        # CONSTANTES
        self.sdtandard_deviation_SI = 2.9
        self.mean_SI = 4.7

        # LISTAS
        self.startTime = []
        self.endTime = []
        self.SIDistr = []
        self.Res = []
        self.aPosterior = []
        self.bPosterior = []
        self.Incidence = []
        self.RMedian = []

        # OBJETOS COM DADOS DO BANCO
        self.municipio = 0
        self.regional = 0

    # CHAMADA DE MÉTODO PARA MUNICIPIO
    def estimar_R_Municipio(self, cod):
        self.codigo_igbe_municipio = cod
        self.estimR(True, cod)

    # CHAMADA DE MÉTODO PARA REGIONAL
    def estimar_R_Regional(self, cod):
        self.regional_saude = cod
        self.estimR(False, cod)

    # ESTIMAR TAXA DE TRANSMISSIBILIDADE (IMPERIAL COLLEGE LONDON), SEJA MUNICIPIO OU REGIONAL
    def estimR(self, isMunicipio, codigo):
        if isMunicipio:
            self.municipio = self.ReadIncidencePorMunicipioBD()
            self.TimeMax = len(self.municipio)
        else:
            self.regional = self.ReadIncidencePorRegionalBD()
            self.TimeMax = len(self.regional)

        self.ReadPrior()

        self.ReadTimeSteps()

        if self.SIuncertainty == "N":

            if self.parametricSI == "Y":

                self.MeanSI = self.mean_SI
                self.sdSI = self.sdtandard_deviation_SI

                SumPi = 0
                SumPiXi = 0
                SumPiXi2 = 0

                for t in range(self.TimeMin, self.TimeMax + 1):

                    value = self.DiscreteShiftedGammaSIDistr(
                        t - self.TimeMin, self.MeanSI, self.sdSI)

                    if (0 > value):
                        self.SIDistr.insert(t - self.TimeMin, 0)
                    else:
                        self.SIDistr.insert(t - self.TimeMin, value)

                    SumPi = SumPi + self.SIDistr[t - self.TimeMin]
                    SumPiXi = SumPiXi + (t - self.TimeMin) * \
                        self.SIDistr[t - self.TimeMin]
                    SumPiXi2 = SumPiXi2 + \
                        (t - self.TimeMin) * (t - self.TimeMin) * \
                        self.SIDistr[t - self.TimeMin]

                self.MeanSIFinal = SumPiXi
                self.sdSIFinal = ((SumPiXi2 - SumPiXi * SumPiXi) ** 2)

            if (self.StartEstimateDate > self.MeanSIFinal):
                self.StartEstimateDate = int(self.StartEstimateDate)

            else:
                self.StartEstimateDate = int(self.MeanSIFinal)

            # ESTIMAR R
            self.TimePeriodNb = 1

            for i in range(self.endTime[self.TimePeriodNb - 1] - 1, self.TimeMax):

                posicaoRT = ((len(self.municipio) - self.NbTimePeriods - 1) + self.TimePeriodNb) if (
                    isMunicipio) else ((len(self.regional) - self.NbTimePeriods - 1) + self.TimePeriodNb)

                Res = self.CalculatePosterior(
                    self.MeanSI, self.sdSI, self.SIDistr, self.TimePeriodNb)

                self.aPosterior.insert(self.TimePeriodNb - 1, Res[0])
                self.bPosterior.insert(self.TimePeriodNb - 1, Res[1])

                mediana = self.GammaInv(
                    0.5, self.aPosterior[self.TimePeriodNb - 1], self.bPosterior[self.TimePeriodNb - 1])

                self.RMedian.insert(self.TimePeriodNb - 1, mediana)

                if isMunicipio:
                    self.municipio[posicaoRT].setRt(
                        self.RMedian[self.TimePeriodNb - 1])
                else:
                    self.regional[posicaoRT].setRt(
                        self.RMedian[self.TimePeriodNb - 1])

                # print(self.RMedian[self.TimePeriodNb - 1])
                #   , self.municipio[posicaoRT].getData() if (isMunicipio)
                #   else self.regional[posicaoRT].getData(), "   ", self.TimePeriodNb - 1, self.endTime[self.TimePeriodNb - 1])

                self.TimePeriodNb = self.TimePeriodNb + 1

        if isMunicipio:
            pass
            # self.bd.salvarOutputsMunicipioNoBD(self.municipio, self.isCompletlyRT)
        else:
            self.bd.salvarOutputsRegionalNoBD(
                self.regional, self.isCompletlyRT, codigo)

    def GammaInv(self, probabilidade, alfa, beta):

        inverseCumulative = gamma.ppf(probabilidade, alfa, 0, beta)
        return inverseCumulative

    def CalculatePosterior(self, MeanSI, sdSI, SIDistr, TimePeriodNb):
        Temp = []

        SumI = 0
        SumLambda = 0

        for i in range(self.startTime[TimePeriodNb - 1], self.endTime[TimePeriodNb - 1]+1):
            SumI += self.Incidence[i - self.TimeMin]
            SumLambda += self.Lambda(i, MeanSI, sdSI, SIDistr)

        # aPosterior
        Temp.insert(0, self.aPrior + float(SumI))
        # print(Temp[0], TimePeriodNb -1)

        # bPosterior
        Temp.insert(1, 1 / (1 / self.bPrior + SumLambda))
        # print(Temp[1], TimePeriodNb - 1)

        return Temp

    def Lambda(self, t, MeanSI, sdSI, SIDistr):
        Lambda = 0

        if (self.SIuncertainty == "N" and self.parametricSI == "N"):
            for i in range(1, t):
                Lambda += self.Incidence[t - i - self.TimeMin] * SIDistr[i]

        else:
            for i in range(1, t):
                Lambda += float(self.Incidence[t - i - self.TimeMin]) * \
                    self.DiscreteShiftedGammaSIDistr(i, MeanSI, sdSI)

        return Lambda

    def ReadIncidencePorRegionalBD(self):

        sql_data = """SELECT MAX(data)::DATE as MAX_DATE FROM rt_regional where regional= %s;"""

        sql_dados_totais = """SELECT casos.regional,
                                CASOS.DATA,
                                SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL
                            FROM CASOS
                            WHERE CASOS.REGIONAL = %s 
                                AND CASOS.DATA > '2020-04-02'
                            GROUP BY casos.regional,CASOS.DATA
                            ORDER BY CASOS.DATA;"""

        sql_dados_parciais = """SELECT REGIONAIS.ID,
                                CASOS.DATA,
                                SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL
                            FROM REGIONAIS, CASOS
                            WHERE CASOS.DATA BETWEEN %s::DATE - INTERVAL '29 DAYS' AND NOW()
                                AND CASOS.REGIONAL = %s
                                AND CASOS.REGIONAL = REGIONAIS.ID
                            GROUP BY REGIONAIS.ID, REGIONAIS.REGIONAL_SAUDE, CASOS.DATA
                            ORDER BY REGIONAIS.ID, CASOS.DATA;"""

        data = self.bd.getMaxData(sql_data, self.regional_saude)

        if data[0] is None:
            self.isCompletlyRT = True
            params = (self.regional_saude,)
            regional = self.bd.getCasosPorRegional(sql_dados_totais, params)

        else:
            self.isCompletlyRT = False
            params = (data, self.regional_saude,)
            regional = self.bd.getCasosPorRegional(sql_dados_parciais, params)

        self.TimeMin = 1
        self.TimeMax = len(regional)

        for t in range(1, (self.TimeMax)+1):
            self.Incidence.insert(
                t-self.TimeMin, regional[t-self.TimeMin].getMediaMovel())
            # print("Incidence[", t-self.TimeMin, "] = ",
            #       self.Incidence[t-self.TimeMin])

        return regional

    def ReadIncidencePorMunicipioBD(self):

        sql_data = """SELECT MAX(data)::DATE as MAX_DATE FROM rt_municipio where codigo_ibge_municipio= %s;"""

        sql_dados_totais = """SELECT CASOS.regional,
                                CASOS.codigo_ibge_municipio,
								CASOS.DATA,
                                CASOS.CASOS_MEDIAMOVEL
                            FROM CASOS
                            WHERE CASOS.codigo_ibge_municipio = %s
                            ORDER BY CASOS.DATA;"""

        sql_dados_parciais = """SELECT CASOS.regional,
								CASOS.codigo_ibge_municipio,
                                CASOS.DATA,
                                CASOS.CASOS_MEDIAMOVEL AS CASOS_MEDIAMOVEL
                            FROM CASOS
                            WHERE CASOS.codigo_ibge_municipio = %s
                                AND CASOS.DATA BETWEEN %s::DATE - INTERVAL '29 days' AND NOW()
                            ORDER BY CASOS.codigo_ibge_municipio, CASOS.DATA;"""

        data = self.bd.getMaxData(sql_data, self.codigo_ibge_municipio)

        if data is None:
            self.isCompletlyRT = True
            params = (self.codigo_ibge_municipio, )
            municipio = self.bd.getCasosPorMunicipio(
                sql_dados_totais, params=params)

        else:
            self.isCompletlyRT = False
            params = (self.codigo_ibge_municipio, data)
            municipio = self.bd.getCasosPorMunicipio(
                sql_dados_parciais, params=params)

        self.TimeMin = 1
        self.TimeMax = len(municipio)

        for t in range(1, (self.TimeMax)+1):
            self.Incidence.insert(
                t-self.TimeMin, municipio[t-self.TimeMin].getMediaMovel())

            # print("Incidence[", t-self.TimeMin, "] = ",
            #       self.Incidence[t-self.TimeMin])

        return municipio

    def ReadPrior(self):

        self.MeanPrior = 5
        self.StdPrior = 5

        self.aPrior = (self.MeanPrior * self.MeanPrior) / \
            (self.StdPrior * self.StdPrior)
        self.bPrior = ((self.StdPrior * self.StdPrior) / self.MeanPrior)

    def ReadTimeSteps(self):

        self.CVThreshold = 0.3
        self.CumulIncThreshold = 1 / \
            (self.CVThreshold * self.CVThreshold) - self.aPrior

        self.CumulInc = 0
        t = self.TimeMin + 1

        while ((self.CumulInc < self.CumulIncThreshold) and (t < self.TimeMax)):
            t = t + 1
            self.CumulInc = self.CumulInc + \
                (int)(self.Incidence[t - self.TimeMin])

        self.StartEstimateDate = t

        self.CustomTimeSteps = "N"

        if self.CustomTimeSteps == "N":
            Length = 7

            Step = 1

            if self.StartEstimateDate > Length:
                self.StartEstimateDate = self.StartEstimateDate
            else:
                self.StartEstimateDate = int(Length)

            t = int(self.StartEstimateDate)

            self.TimePeriodNb = 1

            self.endTime.insert(self.TimePeriodNb - 1, t)
            self.startTime.insert(self.TimePeriodNb - 1, t - int(Length) + 1)

            while (t <= self.TimeMax - Step):
                t = int(t + Step)
                self.TimePeriodNb = self.TimePeriodNb + 1
                self.endTime.insert(self.TimePeriodNb - 1, t)
                self.startTime.insert(
                    self.TimePeriodNb - 1, t - int(Length) + 1)

            self.NbTimePeriods = self.TimePeriodNb

    def DiscreteShiftedGammaSIDistr(self, k, MeanSI, sdSI):
        a = (MeanSI - 1) * (MeanSI - 1) / (sdSI * sdSI)
        b = sdSI * sdSI / (MeanSI - 1)

        if k >= 2:
            return k * self.GammaDist(k, a, b) + (k - 2) * self.GammaDist(k - 2, a, b) - 2 * (k - 1) * self.GammaDist(k - 1, a, b) + a * b * (2 * self.GammaDist(k - 1, a + 1, b) - self.GammaDist(k - 2, a + 1, b) - self.GammaDist(k, a + 1, b))
        elif k == 1:
            return k * self.GammaDist(k, a, b) - a * b * self.GammaDist(k, a + 1, b)
        elif k == 0:
            return 0

        return 0

        # // a=alfa, b=beta, k=cumulativo
    def GammaDist(self, k, a, b):

        cumulativeProvability = gamma.cdf(k, a, 0, b)
        return cumulativeProvability

    def gerarRTRegionais(self):
        for i in range(1, 18):

            print("Calculando RT Regional ", processaRegiao.buscaNomeRegiao(
                i), "...", end='', flush=True)

            self.estimar_R_Regional(i)

            print("Ok")
