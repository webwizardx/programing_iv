import pandas as pd


class DataAnalyser:

    def __init__(self):
        self.df: pd.DataFrame = None
        self.load_data()

    @property
    def shape(self):
        return self.df.shape

    @property
    def dtypes(self):
        return self.df.dtypes

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['Temperatura máxima (ºC)', 'Temperatura mínima (ºC)',
                   'Racha (km/h)', 'Velocidad máxima (km/h)']
        df = df.dropna().copy()
        for column in columns:
            df.loc[:, column] = df[column].apply(
                lambda value: value.split(' ')[0])
            df[column] = df[column].astype(float)
        return df

    def load_data(self):
        data_sets = []
        for i in range(1, 8):
            date = f'2019-01-0{i}'
            data_set = pd.read_excel(
                f'data/dm{date}.xls', skiprows=4)
            data_set['Fecha'] = date
            data_set = self._clean_data(data_set)
            data_sets.append(data_set)
        self.df = pd.concat(data_sets)

    def describe(self):
        return self.df.describe()

    def medianByProvinces(self):
        return self.df.groupby('Provincia').median()

    def maxTemperaturesByStation(self):
        return self.df.groupby('Estación')['Temperatura máxima (ºC)'].max()

    def minTemperaturesByStation(self):
        return self.df.groupby('Estación')['Temperatura máxima (ºC)'].min()

    def maxStreakByProvinceAndDate(self):
        return self.df.groupby(['Provincia', 'Fecha'])['Racha (km/h)'].max()

    def countStationsByProvince(self):
        return self.df.groupby('Provincia')['Estación'].count()

    def totalStationsByProvince(self):
        return self.df.groupby('Provincia')['Estación'].count().sum()


if __name__ == '__main__':
    data_analyser = DataAnalyser()
    print(f'Number of rows and columns: {data_analyser.shape}')
    print('=' * 100)
    print(f'Data types per columns: {data_analyser.dtypes}')
    print('=' * 100)
    print(f'Statistics per columns: {data_analyser.describe()}')
    print('=' * 100)
    print(f'Medians per provinces: {data_analyser.medianByProvinces()}')
    print('=' * 100)
    print(
        f'Max temperatures per stations: {data_analyser.maxTemperaturesByStation()}')
    print('=' * 100)
    print(
        f'Min temperatures per stations: {data_analyser.minTemperaturesByStation()}')
    print('=' * 100)
    print(
        f'Max wind streak per province: {data_analyser.maxStreakByProvinceAndDate()}')
    print('=' * 100)
    print(f'Stations per province: {data_analyser.countStationsByProvince()}')
    print('=' * 100)
    print(
        f'Total stations per province: {data_analyser.totalStationsByProvince()}')
