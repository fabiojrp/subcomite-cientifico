import datetime


class Utils:

    @staticmethod
    def datetime_format(date):
        saida = date
        if date == "1899-12-31 00:00:00" or date == "1961-12-21 00:00:00" or date == "1966-01-04 00:00:00":
            ##print(saida)
            return datetime.datetime.strptime("2020-01-01 00:00", '%Y-%m-%d %H:%M')
     

        if len(date) > 16:
            exp = date.split('.')
            saida = exp[0][:-3]
            saida_exp = saida.split('-')

            ##print(saida)

            if len(saida_exp) > 2:
                return datetime.datetime.strptime(saida, '%Y-%m-%d %H:%M')

        return datetime.datetime.strptime(saida, '%d/%m/%Y %H:%M').strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def date_format(date):
        if date == "2002-11-24 00:00:00":
            return datetime.datetime.strptime("2020-11-24", '%Y-%m-%d')

        if date == "2000-08-11 00:00:00":
            return datetime.datetime.strptime("2020-08-11", '%Y-%m-%d')

        if date == "2002-07-20 00:00:00":
            return datetime.datetime.strptime("2020-07-20", '%Y-%m-%d')

        if date == "2002-07-29 00:00:00":
            return datetime.datetime.strptime("2020-07-29", '%Y-%m-%d')

        if date == "2002-11-24 00:00:00":
            return datetime.datetime.strptime("2020-11-24", '%Y-%m-%d')

        if date == "1899-12-31 00:00:00" or date == "1961-12-21 00:00:00" or date == "1966-01-04 00:00:00" or date == "1991-04-19 00:00:00":
            ##print(saida)
            return datetime.datetime.strptime("2020-01-01", '%Y-%m-%d')

        if date == None:
            return -1

        exp = date.split(' ')
        ##return datetime.datetime.strptime(exp[0], '%d/%m/%Y').strftime("%Y-%m-%d")
        return datetime.datetime.strptime(exp[0], '%Y-%m-%d')
        

