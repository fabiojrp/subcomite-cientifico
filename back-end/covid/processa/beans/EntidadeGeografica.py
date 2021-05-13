
class EntidadeGeografica:
    
    def __init__(self):
        self.codigo_ibge_municipio = None
        self.media_movel = None
        self.data = None
        self.rt = None
        self.regional_saude = None

    def getRegional_saude(self):
        return self.regional_saude
    
    def setRegional_saude(self, regional_saude):
        self.regional_saude = regional_saude

    def getCodigo_ibge_municipio(self):
        return self.codigo_ibge_municipio

    def setCodigo_ibge_municipio(self, codigo_ibge_municipio):
        self.codigo_ibge_municipio = codigo_ibge_municipio

    def getMediaMovel(self):
        return self.media_movel

    def setMediaMovel(self, media_movel):
        self.media_movel = media_movel

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getRt(self):
        return self.rt

    def setRt(self, rt):
        self.rt = rt