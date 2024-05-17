import pandas as pd

# Виняток для обробки помилок зчитування файлу
class FileReadError(Exception):
    pass

# Ітератор для списку країн
class CountryIterator:
    def __init__(self, countries):
        self.__countries = countries
        self.__index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index < len(self.__countries):
            result = self.__countries[self.__index]
            self.__index += 1
            return result
        else:
            raise StopIteration

class CountryDataProcessor:
    def __init__(self, file_path, delimiter=',', header=True):
        try:
            self.__df = pd.read_csv(file_path, delimiter=delimiter, header    =0 if header else None)
        except Exception as e:
            raise FileReadError(f"Cannot read file: {e}")

    def get_all_countries(self):
        countries = self.__df['Country'].str.strip().tolist()
        return CountryIterator(countries)

    def get_countries_larger_than_ukraine(self):
        try:
            ukraine_area = self.__df[self.__df['Country'].str.strip() == 'Ukraine']['Area (sq. mi.)'].values[0]
        except IndexError:
            raise ValueError("Ukraine not found in the dataset.")

        countries = self.__df[self.__df['Area (sq. mi.)'] > ukraine_area]['Country'].str.strip().tolist()
        return CountryIterator(countries)

    def get_countries_population_over_10m_and_larger_than_ukraine(self):
        try:
            ukraine_area = self.__df[self.__df['Country'].str.strip() == 'Ukraine']['Area (sq. mi.)'].values[0]
        except IndexError:
            raise ValueError("Ukraine not found in the dataset.")

        filtered_countries = self.__df[(self.__df['Population'] > 10000000) & (self.__df['Area (sq. mi.)'] > ukraine_area)]
        countries = filtered_countries['Country'].str.strip().tolist()
        return CountryIterator(countries)

    def get_top_10_countries_by_gdp(self):
        top_10_gdp_countries = self.__df.nlargest(10, 'GDP ($ per capita)')
        countries = top_10_gdp_countries['Country'].str.strip().tolist()
        return CountryIterator(countries)

    def get_landlocked_countries(self):
        landlocked_countries = self.__df[self.__df['Coastline (coast/area ratio)'] == 0]
        countries = landlocked_countries['Country'].str.strip().tolist()
        return CountryIterator(countries)

# Функція для друку списку країн
def print_countries(title, country_iterator):
    print(f"{title}:")
    for country in country_iterator:
        print(f"- {country}")
    print()

# Приклад використання та тестування
if __name__ == "__main__":
    processor = CountryDataProcessor('countries_of_the_world.csv', delimiter=',', header=True)

    print_countries("All countries", processor.get_all_countries())
    print_countries("Countries larger than Ukraine", processor.get_countries_larger_than_ukraine())
    print_countries("Countries with population over 10 million and larger than Ukraine", processor.get_countries_population_over_10m_and_larger_than_ukraine())
    print_countries("Top 10 countries by GDP", processor.get_top_10_countries_by_gdp())
    print_countries("Landlocked countries", processor.get_landlocked_countries())
