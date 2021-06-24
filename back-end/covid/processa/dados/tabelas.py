class Tabelas:

    def __init__(self):
        municipios = {
            420005: 12, 420010: 17, 420020: 3, 420030: 3, 420040: 12, 420050: 14, 420055: 14, 420060: 9, 420070: 9, 420075: 2, 420080: 6, 420090: 9, 420100: 16, 420110: 9,
            420120: 9, 420125: 11, 420127: 2, 420130: 13, 420140: 7, 420150: 10, 420160: 4, 420165: 14, 420170: 11, 420180: 3, 420190: 3, 420195: 7, 420205: 13, 420200: 8,
            420207: 7, 421280: 8, 422000: 5, 420208: 6, 420209: 6, 420210: 13, 420213: 15, 420215: 6, 420220: 11, 420230: 9, 420240: 11, 420243: 16, 420250: 16, 420253: 17,
            420257: 6, 420260: 16, 420245: 8, 420270: 11, 420280: 10, 420285: 3, 420287: 12, 420290: 11, 420300: 4, 420310: 14, 420315: 4, 420320: 8, 420330: 15, 420340: 16,
            420350: 17, 420360: 12, 420370: 9, 420380: 15, 420325: 16, 420390: 12, 420395: 10, 420400: 12, 420410: 14, 420415: 12, 420417: 16, 420419: 3, 420420: 14, 420425: 5,
            420430: 2, 420435: 14, 420440: 14, 420445: 17, 420455: 16, 420450: 13, 420460: 5, 420470: 14, 420475: 14, 420480: 4, 420490: 6, 420500: 6, 420510: 3, 420515: 11,
            420517: 17, 420519: 7, 420520: 12, 420530: 17, 420535: 6, 420540: 9, 420543: 14, 420545: 5, 420550: 4, 420555: 4, 420560: 17, 420570: 9, 420580: 13, 420590: 11,
            420600: 9, 420610: 10, 420620: 10, 420630: 11, 420640: 6, 420650: 13, 420660: 6, 420665: 14, 420670: 12, 420675: 4, 420680: 12, 420690: 3, 420700: 5, 420710: 8,
            420720: 10, 420730: 10, 420740: 3, 420750: 11, 420757: 4, 420760: 2, 420765: 6, 420768: 17, 420770: 2, 420775: 6, 420780: 2, 420785: 14, 420790: 15, 420800: 2,
            420810: 15, 420820: 8, 420830: 8, 420840: 6, 420845: 13, 420850: 3, 420860: 12, 420870: 7, 420880: 10, 420890: 13, 420895: 14, 420900: 12, 420910: 13, 420915: 3,
            420917: 17, 420920: 12, 420930: 16, 420940: 10, 420945: 17, 420950: 3, 420960: 5, 420970: 4, 420980: 9, 420985: 2, 420990: 3, 421000: 8, 421003: 12, 421005: 4,
            421010: 15, 421020: 9, 421030: 15, 421040: 7, 421050: 6, 421055: 17, 421060: 13, 421070: 4, 421080: 7, 421085: 3, 421090: 6, 421100: 6, 421105: 12, 421110: 15,
            421120: 5, 421125: 7, 421130: 8, 421140: 14, 421145: 14, 421150: 9, 421160: 5, 421165: 17, 421170: 5, 421175: 16, 421180: 12, 421185: 17, 421187: 2, 421189: 16,
            421190: 9, 421200: 6, 421205: 16, 421210: 14, 421220: 15, 421223: 6, 421225: 7, 421227: 17, 421230: 9, 421240: 10, 421250: 8, 421260: 2, 421265: 10, 421270: 3,
            421290: 14, 421300: 4, 421310: 2, 421315: 14, 421320: 11, 421330: 16, 421335: 4, 421340: 17, 421350: 8, 421360: 15, 421370: 3, 421380: 7, 421390: 2, 421400: 3,
            421410: 3, 421415: 6, 421420: 14, 421430: 9, 421440: 4, 421450: 3, 421460: 3, 421480: 3, 421470: 11, 421490: 10, 421500: 15, 421505: 16, 421507: 14, 421510: 11,
            421520: 6, 421530: 3, 421535: 6, 421540: 4, 421545: 10, 421550: 4, 421555: 6, 421560: 10, 421565: 7, 421567: 3, 421568: 6, 421569: 14, 421570: 9, 421580: 15,
            421575: 17, 421590: 9, 421600: 14, 421605: 4, 421610: 17, 421620: 13, 421630: 9, 421635: 13, 421625: 6, 421640: 7, 421650: 16, 421660: 9, 421670: 6, 421680: 16,
            421690: 17, 421700: 10, 421710: 10, 421715: 6, 421720: 6, 421725: 9, 421730: 6, 421740: 13, 421750: 2, 421755: 14, 421760: 5, 421770: 7, 421775: 14, 421780: 3,
            421790: 4, 421795: 6, 421800: 9, 421810: 7, 421820: 11, 421825: 4, 421830: 15, 421835: 5, 421840: 10, 421850: 12, 421860: 3, 421870: 10, 421875: 6, 421880: 7,
            421885: 14, 421890: 16, 421895: 16, 421900: 5, 421910: 17, 421915: 12, 421917: 12, 421920: 3, 421930: 4, 421935: 3, 421940: 3, 421950: 17, 421960: 2, 421970: 17,
            421985: 12, 0: 1
        }

        self.regional = {
            'Ignorado': 0,
            'NULL': 1,
            'ALTO URUGUAI CATARINENSE': 2,
            'ALTO VALE DO ITAJAI': 3,
            'ALTO VALE DO RIO DO PEIXE': 4,
            'CARBONIFERA': 5,
            'EXTREMO OESTE': 6,
            'EXTREMO SUL CATARINENSE': 7,
            'FOZ DO RIO ITAJAI': 8,
            'GRANDE FLORIANOPOLIS': 9,
            'LAGUNA': 10,
            'MEDIO VALE DO ITAJAI': 11,
            'MEIO OESTE': 12,
            'NORDESTE': 13,
            'OESTE': 14,
            'PLANALTO NORTE': 15,
            'SERRA CATARINENSE': 16,
            'XANXERE': 17
        }

        self.regionais_rt = {
            'Ignorado': 0,
            'OUTROS ESTADOS': 1,
            'Alto Uruguai Catarinense': 2,
            'Alto Vale do Itajaí': 3,
            'Alto Vale do Rio do Peixe': 4,
            'Carbonífera': 5,
            'Extremo Oeste': 6,
            'Extremo Sul Catarinense': 7,
            'Foz do Rio Itajaí': 8,
            'Grande Florianópolis': 9,
            'Laguna': 10,
            'Médio Vale do Itajaí': 11,
            'Meio Oeste': 12,
            'Nordeste': 13,
            'Oeste': 14,
            'Planalto Norte': 15,
            'Serra Catarinense': 16,
            'Xanxerê': 17,
        }

        self.municipios = {
            420005: 12, 420010: 17, 420020: 3, 420030: 3, 420040: 12, 420050: 14, 420055: 14, 420060: 9, 420070: 9, 420075: 2, 420080: 6, 420090: 9, 420100: 16, 420110: 9,
            420120: 9, 420125: 11, 420127: 2, 420130: 13, 420140: 7, 420150: 10, 420160: 4, 420165: 14, 420170: 11, 420180: 3, 420190: 3, 420195: 7, 420205: 13, 420200: 8,
            420207: 7, 421280: 8, 422000: 5, 420208: 6, 420209: 6, 420210: 13, 420213: 15, 420215: 6, 420220: 11, 420230: 9, 420240: 11, 420243: 16, 420250: 16, 420253: 17,
            420257: 6, 420260: 16, 420245: 8, 420270: 11, 420280: 10, 420285: 3, 420287: 12, 420290: 11, 420300: 4, 420310: 14, 420315: 4, 420320: 8, 420330: 15, 420340: 16,
            420350: 17, 420360: 12, 420370: 9, 420380: 15, 420325: 16, 420390: 12, 420395: 10, 420400: 12, 420410: 14, 420415: 12, 420417: 16, 420419: 3, 420420: 14, 420425: 5,
            420430: 2, 420435: 14, 420440: 14, 420445: 17, 420455: 16, 420450: 13, 420460: 5, 420470: 14, 420475: 14, 420480: 4, 420490: 6, 420500: 6, 420510: 3, 420515: 11,
            420517: 17, 420519: 7, 420520: 12, 420530: 17, 420535: 6, 420540: 9, 420543: 14, 420545: 5, 420550: 4, 420555: 4, 420560: 17, 420570: 9, 420580: 13, 420590: 11,
            420600: 9, 420610: 10, 420620: 10, 420630: 11, 420640: 6, 420650: 13, 420660: 6, 420665: 14, 420670: 12, 420675: 4, 420680: 12, 420690: 3, 420700: 5, 420710: 8,
            420720: 10, 420730: 10, 420740: 3, 420750: 11, 420757: 4, 420760: 2, 420765: 6, 420768: 17, 420770: 2, 420775: 6, 420780: 2, 420785: 14, 420790: 15, 420800: 2,
            420810: 15, 420820: 8, 420830: 8, 420840: 6, 420845: 13, 420850: 3, 420860: 12, 420870: 7, 420880: 10, 420890: 13, 420895: 14, 420900: 12, 420910: 13, 420915: 3,
            420917: 17, 420920: 12, 420930: 16, 420940: 10, 420945: 17, 420950: 3, 420960: 5, 420970: 4, 420980: 9, 420985: 2, 420990: 3, 421000: 8, 421003: 12, 421005: 4,
            421010: 15, 421020: 9, 421030: 15, 421040: 7, 421050: 6, 421055: 17, 421060: 13, 421070: 4, 421080: 7, 421085: 3, 421090: 6, 421100: 6, 421105: 12, 421110: 15,
            421120: 5, 421125: 7, 421130: 8, 421140: 14, 421145: 14, 421150: 9, 421160: 5, 421165: 17, 421170: 5, 421175: 16, 421180: 12, 421185: 17, 421187: 2, 421189: 16,
            421190: 9, 421200: 6, 421205: 16, 421210: 14, 421220: 15, 421223: 6, 421225: 7, 421227: 17, 421230: 9, 421240: 10, 421250: 8, 421260: 2, 421265: 10, 421270: 3,
            421290: 14, 421300: 4, 421310: 2, 421315: 14, 421320: 11, 421330: 16, 421335: 4, 421340: 17, 421350: 8, 421360: 15, 421370: 3, 421380: 7, 421390: 2, 421400: 3,
            421410: 3, 421415: 6, 421420: 14, 421430: 9, 421440: 4, 421450: 3, 421460: 3, 421480: 3, 421470: 11, 421490: 10, 421500: 15, 421505: 16, 421507: 14, 421510: 11,
            421520: 6, 421530: 3, 421535: 6, 421540: 4, 421545: 10, 421550: 4, 421555: 6, 421560: 10, 421565: 7, 421567: 3, 421568: 6, 421569: 14, 421570: 9, 421580: 15,
            421575: 17, 421590: 9, 421600: 14, 421605: 4, 421610: 17, 421620: 13, 421630: 9, 421635: 13, 421625: 6, 421640: 7, 421650: 16, 421660: 9, 421670: 6, 421680: 16,
            421690: 17, 421700: 10, 421710: 10, 421715: 6, 421720: 6, 421725: 9, 421730: 6, 421740: 13, 421750: 2, 421755: 14, 421760: 5, 421770: 7, 421775: 14, 421780: 3,
            421790: 4, 421795: 6, 421800: 9, 421810: 7, 421820: 11, 421825: 4, 421830: 15, 421835: 5, 421840: 10, 421850: 12, 421860: 3, 421870: 10, 421875: 6, 421880: 7,
            421885: 14, 421890: 16, 421895: 16, 421900: 5, 421910: 17, 421915: 12, 421917: 12, 421920: 3, 421930: 4, 421935: 3, 421940: 3, 421950: 17, 421960: 2, 421970: 17,
            421985: 12, 0: 1
        }

    def getRegionalCiasc(self, indice):
        # Tabela de regionais
        return self.regional[indice]

    def getRegionalMunicipio(self, indice):
        return self.municipios[indice]

    def getRegionalMunicipioBrasil(self, indice):
        municipios = {
            420005: 12, 420010: 17, 420020: 3, 420030: 3, 420040: 12, 420050: 14, 420055: 14, 420060: 9, 420070: 9, 420075: 2, 420080: 6, 420090: 9, 420100: 16, 420110: 9,
            420120: 9, 420125: 11, 420127: 2, 420130: 13, 420140: 7, 420150: 10, 420160: 4, 420165: 14, 420170: 11, 420180: 3, 420190: 3, 420195: 7, 420205: 13, 420200: 8,
            420207: 7, 421280: 8, 422000: 5, 420208: 6, 420209: 6, 420210: 13, 420213: 15, 420215: 6, 420220: 11, 420230: 9, 420240: 11, 420243: 16, 420250: 16, 420253: 17,
            420257: 6, 420260: 16, 420245: 8, 420270: 11, 420280: 10, 420285: 3, 420287: 12, 420290: 11, 420300: 4, 420310: 14, 420315: 4, 420320: 8, 420330: 15, 420340: 16,
            420350: 17, 420360: 12, 420370: 9, 420380: 15, 420325: 16, 420390: 12, 420395: 10, 420400: 12, 420410: 14, 420415: 12, 420417: 16, 420419: 3, 420420: 14, 420425: 5,
            420430: 2, 420435: 14, 420440: 14, 420445: 17, 420455: 16, 420450: 13, 420460: 5, 420470: 14, 420475: 14, 420480: 4, 420490: 6, 420500: 6, 420510: 3, 420515: 11,
            420517: 17, 420519: 7, 420520: 12, 420530: 17, 420535: 6, 420540: 9, 420543: 14, 420545: 5, 420550: 4, 420555: 4, 420560: 17, 420570: 9, 420580: 13, 420590: 11,
            420600: 9, 420610: 10, 420620: 10, 420630: 11, 420640: 6, 420650: 13, 420660: 6, 420665: 14, 420670: 12, 420675: 4, 420680: 12, 420690: 3, 420700: 5, 420710: 8,
            420720: 10, 420730: 10, 420740: 3, 420750: 11, 420757: 4, 420760: 2, 420765: 6, 420768: 17, 420770: 2, 420775: 6, 420780: 2, 420785: 14, 420790: 15, 420800: 2,
            420810: 15, 420820: 8, 420830: 8, 420840: 6, 420845: 13, 420850: 3, 420860: 12, 420870: 7, 420880: 10, 420890: 13, 420895: 14, 420900: 12, 420910: 13, 420915: 3,
            420917: 17, 420920: 12, 420930: 16, 420940: 10, 420945: 17, 420950: 3, 420960: 5, 420970: 4, 420980: 9, 420985: 2, 420990: 3, 421000: 8, 421003: 12, 421005: 4,
            421010: 15, 421020: 9, 421030: 15, 421040: 7, 421050: 6, 421055: 17, 421060: 13, 421070: 4, 421080: 7, 421085: 3, 421090: 6, 421100: 6, 421105: 12, 421110: 15,
            421120: 5, 421125: 7, 421130: 8, 421140: 14, 421145: 14, 421150: 9, 421160: 5, 421165: 17, 421170: 5, 421175: 16, 421180: 12, 421185: 17, 421187: 2, 421189: 16,
            421190: 9, 421200: 6, 421205: 16, 421210: 14, 421220: 15, 421223: 6, 421225: 7, 421227: 17, 421230: 9, 421240: 10, 421250: 8, 421260: 2, 421265: 10, 421270: 3,
            421290: 14, 421300: 4, 421310: 2, 421315: 14, 421320: 11, 421330: 16, 421335: 4, 421340: 17, 421350: 8, 421360: 15, 421370: 3, 421380: 7, 421390: 2, 421400: 3,
            421410: 3, 421415: 6, 421420: 14, 421430: 9, 421440: 4, 421450: 3, 421460: 3, 421480: 3, 421470: 11, 421490: 10, 421500: 15, 421505: 16, 421507: 14, 421510: 11,
            421520: 6, 421530: 3, 421535: 6, 421540: 4, 421545: 10, 421550: 4, 421555: 6, 421560: 10, 421565: 7, 421567: 3, 421568: 6, 421569: 14, 421570: 9, 421580: 15,
            421575: 17, 421590: 9, 421600: 14, 421605: 4, 421610: 17, 421620: 13, 421630: 9, 421635: 13, 421625: 6, 421640: 7, 421650: 16, 421660: 9, 421670: 6, 421680: 16,
            421690: 17, 421700: 10, 421710: 10, 421715: 6, 421720: 6, 421725: 9, 421730: 6, 421740: 13, 421750: 2, 421755: 14, 421760: 5, 421770: 7, 421775: 14, 421780: 3,
            421790: 4, 421795: 6, 421800: 9, 421810: 7, 421820: 11, 421825: 4, 421830: 15, 421835: 5, 421840: 10, 421850: 12, 421860: 3, 421870: 10, 421875: 6, 421880: 7,
            421885: 14, 421890: 16, 421895: 16, 421900: 5, 421910: 17, 421915: 12, 421917: 12, 421920: 3, 421930: 4, 421935: 3, 421940: 3, 421950: 17, 421960: 2, 421970: 17,
            421985: 12, 0: 1
        }
        try:
            codigo_ibge = municipios[indice]
        except KeyError as ex:
            codigo_ibge = 0

        return codigo_ibge

    def getPopulacaoMunicipio(self, indice):
        populacao = {
            4200051: 2563, 4200101: 17904, 4200200: 10864, 4200309: 5448, 4200408: 7145, 4200507: 6486, 4200556: 2366, 4200606: 6469, 4200705: 10036, 4200754: 1937, 4200804: 5638, 4200903: 4801, 4201000: 7133, 4201109: 3232, 4201208: 8513, 4201257: 10743, 4201273: 4267,
            4201307: 38129, 4201406: 68228, 4201505: 8674, 4201604: 3550, 4201653: 2240, 4201703: 7934, 4201802: 3210, 4201901: 5679, 4201950: 13071, 4202008: 142295, 4202057: 10795, 4202073: 10979, 4202081: 2678, 4202099: 1677, 4202107: 29168, 4202131: 6337,
            4202156: 2706, 4202206: 11652, 4202305: 68481, 4202404: 357199, 4202438: 3474, 4202453: 19769, 4202503: 4743, 4202537: 3010, 4202578: 2142, 4202602: 9966, 4202701: 5246, 4202800: 33450, 4202859: 3743, 4202875: 2420, 4202909: 134723, 4203006: 78595,
            4203105: 6148, 4203154: 3346, 4203204: 82989, 4203253: 2525, 4203303: 11978, 4203402: 7016, 4203501: 8526, 4203600: 36244, 4203709: 12240, 4203808: 54401, 4203907: 22848, 4203956: 24871, 4204004: 10861, 4204103: 3642, 4204152: 2728, 4204178: 3124, 4204194: 2988,
            4204202: 220367, 4204251: 16684, 4204301: 74641, 4204350: 4453, 4204400: 9981, 4204459: 2549, 4204509: 15909, 4204558: 12795, 4204608: 215186, 4204707: 11086, 4204756: 1962, 4204806: 39745, 4204905: 8250, 4205001: 15498, 4205100: 4146, 4205159: 4064, 4205175: 3203,
            4205191: 2063, 4205209: 4412, 4205308: 10667, 4205357: 1582, 4205407: 500973, 4205431: 2510, 4205456: 26793, 4205506: 36443, 4205555: 2023, 4205605: 2873, 4205704: 23078, 4205803: 18145, 4205902: 69639, 4206009: 14471, 4206108: 6569, 4206207: 11501, 4206306: 23832,
            4206405: 10090, 4206504: 44819, 4206603: 5160, 4206652: 4704, 4206702: 22606, 4206751: 1957, 4206801: 3202, 4206900: 18950, 4207007: 56421, 4207106: 14184, 4207205: 10135, 4207304: 44853, 4207403: 6197, 4207502: 69425, 4207577: 2945, 4207601: 4446, 4207650: 8996,
            4207684: 7514, 4207700: 7593, 4207759: 3976, 4207809: 10419, 4207858: 1930, 4207908: 11222, 4208005: 6169, 4208104: 21669, 4208203: 219536, 4208302: 65312, 4208401: 16872, 4208450: 20576, 4208500: 25086, 4208609: 3936, 4208708: 10416, 4208807: 20024, 4208906: 177697,
            4208955: 1570, 4209003: 30118, 4209102: 590466, 4209151: 4997, 4209177: 2101, 4209201: 2246, 4209300: 157544, 4209409: 45814, 4209458: 1427, 4209508: 6970, 4209607: 15244, 4209706: 12107, 4209805: 3041, 4209854: 4563, 4209904: 12130, 4210001: 12859, 4210035: 5685,
            4210050: 1775, 4210100: 56292, 4210209: 3442, 4210308: 8103, 4210407: 7293, 4210506: 25762, 4210555: 1797, 4210605: 16916, 4210704: 2520, 4210803: 7015, 4210852: 2309, 4210902: 4209, 4211009: 11742, 4211058: 9866, 4211108: 8275, 4211207: 17796, 4211256: 2893,
            4211306: 81475, 4211405: 5019, 4211454: 4331, 4211504: 14549, 4211603: 15166, 4211652: 2442, 4211702: 22912, 4211751: 18744, 4211801: 7295, 4211850: 2217, 4211876: 1505, 4211892: 2359, 4211900: 171797, 4212007: 7423, 4212056: 2627, 4212106: 16169, 4212205: 19320,
            4212239: 3437, 4212254: 8823, 4212270: 4147, 4212304: 7494, 4212403: 3976, 4212502: 32531, 4212601: 2787, 4212650: 10091, 4212700: 5937, 4212809: 23147, 4212908: 20313, 4213005: 3555, 4213104: 3854, 4213153: 2870, 4213203: 33447, 4213302: 4682, 4213351: 3414,
            4213401: 11593, 4213500: 21388, 4213609: 35398, 4213708: 17453, 4213807: 7319, 4213906: 1568, 4214003: 17471, 4214102: 2287, 4214151: 2924, 4214201: 9887, 4214300: 2878, 4214409: 6205, 4214508: 5940, 4214607: 7489, 4214706: 11676, 4214805: 71061, 4214904: 4611, 4215000: 42302,
            4215059: 2483, 4215075: 4598, 4215109: 11551, 4215208: 4786, 4215307: 7642, 4215356: 3781, 4215406: 4718, 4215455: 12678, 4215505: 16830, 4215554: 2223, 4215604: 2142, 4215653: 8358, 4215679: 8787, 4215687: 2428, 4215695: 1260, 4215703: 23245, 4215752: 2336,
            4215802: 84507, 4215901: 2838, 4216008: 11281, 4216057: 5549, 4216107: 9445, 4216206: 52721, 4216255: 6381, 4216305: 37424, 4216354: 3733, 4216404: 7297, 4216503: 26952, 4216602: 246586, 4216701: 13829, 4216800: 8295, 4216909: 24076, 4217006: 13410, 4217105: 3180,
            4217154: 1820, 4217204: 40482, 4217253: 5823, 4217303: 9745, 4217402: 21365, 4217501: 17541, 4217550: 3263, 4217600: 14007, 4217709: 30374, 4217758: 2461, 4217808: 18395, 4217907: 8676, 4217956: 1633, 4218004: 38407, 4218103: 5348, 4218202: 44238, 4218251: 7877,
            4218301: 19275, 4218350: 3929, 4218400: 7081, 4218509: 7840, 4218608: 7360, 4218707: 105686, 4218756: 4543, 4218806: 12899, 4218855: 2464, 4218905: 11235, 4218954: 2465, 4219002: 21268, 4219101: 3573, 4219150: 2477, 4219176: 4492, 4219200: 6338, 4219309: 53065, 4219358: 4979,
            4219408: 3965, 4219507: 50982, 4219606: 3933, 4219705: 28706, 4219853: 3363, 4220000: 12760, 0: 100000
        }

        try:
            populacao = populacao[indice]
        except KeyError as ex:
            populacao = 1

        return populacao

    def getDataLetalidadeRegional(self, regional):
        data_letalidade = {
            1: '2020-04-27', 2: '2020-04-15', 3: '2020-05-15', 4: '2020-05-18', 5: '2020-03-20', 6: '2020-05-17',
            7: '2020-04-27', 8: '2020-03-18', 9: '2020-03-14', 10: '2020-03-20', 11: '2020-03-25', 12: '2020-05-05',
            13: '2020-03-26', 14: '2020-04-23', 15: '2020-05-13', 16: '2020-05-03', 17: '2020-05-09'
        }

        return data_letalidade[regional]
