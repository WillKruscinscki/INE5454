import json
from climatempo import ClimatempoScraper
from accuweather import AccuWeatherScraper
from weather import WeatherScraper
from datetime import datetime


class WeatherDataCollector:
    def __init__(self, cidades):
        self.cidades = cidades
        self.dados_coletados = {}

    def coletar_dados(self):
        for cidade, info in self.cidades.items():
            scraper = info["scraper"](info["url"])
            dados = scraper.coletar_dados()
            self.exibir_dados(cidade, dados)
            if dados:
                dados["URL"] = info["url"]  # coloca a URL ao dicionário de dados
                self.dados_coletados[cidade] = dados

    def exibir_dados(self, cidade, dados):
        if dados:
            print(f"\nDados meteorológicos para {cidade}:")
            print(f"Temperatura: {dados.get('temperatura', 'Nao disponivel')}")
            print(f"Umidade: {dados.get('umidade', 'Nao disponivel')}")
            print(f"Vento: {dados.get('vento', 'Nao disponivel')}")
            print(f"Qualidade do Ar: {dados.get('qualidade_do_ar', 'Nao disponivel')}")
            print(
                f"Sensação Térmica: {dados.get('sensacao_termica', 'Nao disponivel')}"
            )
            print(f"URL: {dados.get('URL', 'Nao disponivel')}")
        else:
            print(f"Dados indisponíveis para {cidade}.")

    def salvar_dados_em_json(self):
        # gera arquivo com a data e hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        nome_arquivo = f"dados_meteorologicos_{timestamp}.json"

        try:
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(self.dados_coletados, arquivo, indent=4, ensure_ascii=False)
            print(f"Arquivo JSON '{nome_arquivo}' criado com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar os dados em JSON: {e}")


# url de cidades e o scrape
cidades = {
    "Florianopolis_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/377/florianopolis-sc",
        "scraper": ClimatempoScraper,
    },
    "Florianopolis_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/florian%C3%B3polis/35952/weather-forecast/35952",
        "scraper": AccuWeatherScraper,
    },
    "Florianopolis_Weather": {
        "url": "https://weather.com/weather/today/l/f136064ba28b472963a7ad219e64ce7ef8eb6cda4c4a59ec8c970f04935c3b12",
        "scraper": WeatherScraper,
    },
    "Rio Branco_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/6/riobranco-ac",
        "scraper": ClimatempoScraper,
    },
    "Rio Branco_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/rio-branco/31909/weather-forecast/31909",
        "scraper": AccuWeatherScraper,
    },
    "Rio Branco_Weather": {
        "url": "https://weather.com/weather/today/l/f0c338d561d8b63c6554b4c045714d8407e30bce71f9e73e8883f5d25d5f5335",
        "scraper": WeatherScraper,
    },
    "Maceio_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/8/maceio-al",
        "scraper": ClimatempoScraper,
    },
    "Maceio_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/macei%C3%B3/31913/weather-forecast/31913",
        "scraper": AccuWeatherScraper,
    },
    "Maceio_Weather": {
        "url": "https://weather.com/weather/today/l/27967df8965052eefe41ce886462ac62a51e7c9b825d61e2b66796cb94ffe108",
        "scraper": WeatherScraper,
    },
    "Macapa_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/39/macapa-ap",
        "scraper": ClimatempoScraper,
    },
    "Macapa_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/macap%C3%A1/64/weather-forecast/64",
        "scraper": AccuWeatherScraper,
    },
    "Macapa_Weather": {
        "url": "https://weather.com/weather/today/l/f9827cbb650b622e5350dffb389fbfcc8ea269ec422a956f31e3183886dcea11",
        "scraper": WeatherScraper,
    },
    "Manaus_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/25/manaus-am",
        "scraper": ClimatempoScraper,
    },
    "Manaus_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/manaus/42471/weather-forecast/42471",
        "scraper": AccuWeatherScraper,
    },
    "Manaus_Weather": {
        "url": "https://weather.com/weather/today/l/ebb70a47505c2e81f1fcd94e033f8772c66512a6f19efc3ed49152aede4c5aa3",
        "scraper": WeatherScraper,
    },
    "Salvador_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/56/salvador-ba",
        "scraper": ClimatempoScraper,
    },
    "Salvador_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/salvador/43080/weather-forecast/43080",
        "scraper": AccuWeatherScraper,
    },
    "Salvador_Weather": {
        "url": "https://weather.com/weather/today/l/4720afa14025b1e42377928acef9681e75073ea7e797901ebbe6eca20217d795",
        "scraper": WeatherScraper,
    },
    "Fortaleza_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/60/fortaleza-ce",
        "scraper": ClimatempoScraper,
    },
    "Fortaleza_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/fortaleza/43346/weather-forecast/43346",
        "scraper": AccuWeatherScraper,
    },
    "Fortaleza_Weather": {
        "url": "https://weather.com/weather/today/l/a8a5be4ff3cb2d667b3f96d88877af861f3cd39260fd1764ed6e144c93e05112",
        "scraper": WeatherScraper,
    },
    "Brasilia_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/61/brasilia-df",
        "scraper": ClimatempoScraper,
    },
    "Brasilia_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/bras%C3%ADlia/43348/weather-forecast/43348",
        "scraper": AccuWeatherScraper,
    },
    "Brasilia_Weather": {
        "url": "https://weather.com/weather/today/l/5b80e46d142343b74abb00becae2015ad3287f0019e945babb76970851501713",
        "scraper": WeatherScraper,
    },
    "Vitoria_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/84/vitoria-es",
        "scraper": ClimatempoScraper,
    },
    "Vitoria_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/vit%C3%B3ria/32929/weather-forecast/32929",
        "scraper": AccuWeatherScraper,
    },
    "Vitoria_Weather": {
        "url": "https://weather.com/weather/today/l/e0754c8c5daffd9a4e29b805b2e4a3369b40f7d3b1c7a78c586ed43e66cdcdcf",
        "scraper": WeatherScraper,
    },
    "Goiania_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/88/goiania-go",
        "scraper": ClimatempoScraper,
    },
    "Goiania_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/goi%C3%A2nia/43599/weather-forecast/43599",
        "scraper": AccuWeatherScraper,
    },
    "Goiania_Weather": {
        "url": "https://weather.com/weather/today/l/f9062d5dcb4e3d4b67bd7a5d00b91bf5bac6a2fe76dfc41dc2f18c97f73d751b",
        "scraper": WeatherScraper,
    },
    "Sao Luis_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/94/saoluis-ma",
        "scraper": ClimatempoScraper,
    },
    "Sao Luis_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/s%C3%A3o-lu%C3%ADs/44127/weather-forecast/44127",
        "scraper": AccuWeatherScraper,
    },
    "Sao Luis_Weather": {
        "url": "https://weather.com/weather/today/l/2ffbab3249f04aa731aaa65d2acca77fa5edae558e762dce2547bf8c8793982f",
        "scraper": WeatherScraper,
    },
    "Cuiaba_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/218/cuiaba-mt",
        "scraper": ClimatempoScraper,
    },
    "Cuiaba_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/cuiab%C3%A1/44281/weather-forecast/44281",
        "scraper": AccuWeatherScraper,
    },
    "Cuiaba_Weather": {
        "url": "https://weather.com/weather/today/l/9d1c089a429e61e2a21333531de27441fb655a94448d2caa02c5b3140fff5cbc",
        "scraper": WeatherScraper,
    },
    "Campo Grande_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/212/campogrande-ms",
        "scraper": ClimatempoScraper,
    },
    "Campo Grande_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/campo-grande/33738/weather-forecast/33738",
        "scraper": AccuWeatherScraper,
    },
    "Campo Grande_Weather": {
        "url": "https://weather.com/weather/today/l/6b88ebbca2977734a5989052721b85e8f59c7885d8967bddd0bd8a03bd30368f",
        "scraper": WeatherScraper,
    },
    "Belo Horizonte_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/107/belohorizonte-mg",
        "scraper": ClimatempoScraper,
    },
    "Belo Horizonte_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/belo-horizonte/44403/weather-forecast/44403",
        "scraper": AccuWeatherScraper,
    },
    "Belo Horizonte_Weather": {
        "url": "https://weather.com/weather/today/l/6e7a77b91a7ca5a864687e298cb47202240730a385f7cd1adf7227170935758f",
        "scraper": WeatherScraper,
    },
    "Belem_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/232/belem-pa",
        "scraper": ClimatempoScraper,
    },
    "Belem_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/bel%C3%A9m/44857/weather-forecast/44857",
        "scraper": AccuWeatherScraper,
    },
    "Belem_Weather": {
        "url": "https://weather.com/weather/today/l/529a77f7398a2247cdb7de32f626019c5ee4c43c40af706655f9f96652c72734",
        "scraper": WeatherScraper,
    },
    "Joao Pessoa_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/256/joaopessoa-pb",
        "scraper": ClimatempoScraper,
    },
    "Joao Pessoa_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/jo%C3%A3o-pessoa/34631/weather-forecast/34631",
        "scraper": AccuWeatherScraper,
    },
    "Joao Pessoa_Weather": {
        "url": "https://weather.com/weather/today/l/4a387b8e0e187f1d7c1984040cc57c8cfe0cd9494d15895aacad7109da999693",
        "scraper": WeatherScraper,
    },
    "Curitiba_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/271/curitiba-pr",
        "scraper": ClimatempoScraper,
    },
    "Curitiba_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/curitiba/44944/weather-forecast/44944",
        "scraper": AccuWeatherScraper,
    },
    "Curitiba_Weather": {
        "url": "https://weather.com/weather/today/l/1f41c866e4490de90170d663657c430eaa1a97bc6ed8d9d7a519df5389b08828",
        "scraper": WeatherScraper,
    },
    "Recife_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/259/recife-pe",
        "scraper": ClimatempoScraper,
    },
    "Recife_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/recife/45090/weather-forecast/45090",
        "scraper": AccuWeatherScraper,
    },
    "Recife_Weather": {
        "url": "https://weather.com/weather/today/l/3d85be48c4efa85f4332925e699b20e5e10357e9a6afd2e150704dd113faf786",
        "scraper": WeatherScraper,
    },
    "Teresina_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/264/teresina-pi",
        "scraper": ClimatempoScraper,
    },
    "Teresina_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/teresina/45253/weather-forecast/45253",
        "scraper": AccuWeatherScraper,
    },
    "Teresina_Weather": {
        "url": "https://weather.com/weather/today/l/ba888e306c69eb0078024aeb054844f7364a20e7a6aa065b555eb0e640eea974",
        "scraper": WeatherScraper,
    },
    "Rio de Janeiro_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/321/riodejaneiro-rj",
        "scraper": ClimatempoScraper,
    },
    "Rio de Janeiro_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/rio-de-janeiro/45449/weather-forecast/45449",
        "scraper": AccuWeatherScraper,
    },
    "Rio de Janeiro_Weather": {
        "url": "https://weather.com/weather/today/l/1ff5f708415c0675e9ddf27ec2c0fb81d235f4b1730d12b3c90879c0c16f7148",
        "scraper": WeatherScraper,
    },
    "Natal_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/334/natal-rn",
        "scraper": ClimatempoScraper,
    },
    "Natal_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/natal/35658/weather-forecast/35658",
        "scraper": AccuWeatherScraper,
    },
    "Natal_Weather": {
        "url": "https://weather.com/weather/today/l/19fd33420ee4c8b43e31f59094c09611edf1a68c9791aadab1fdc5428fbfe933",
        "scraper": WeatherScraper,
    },
    "Porto Alegre_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/363/portoalegre-rs",
        "scraper": ClimatempoScraper,
    },
    "Porto Alegre_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/porto-alegre/45561/weather-forecast/45561",
        "scraper": AccuWeatherScraper,
    },
    "Porto Alegre_Weather": {
        "url": "https://weather.com/weather/today/l/03b1148e398c4397d9c274ecd99b1477eea4dc2c4f382bc6b7cdd51c9f4c2226",
        "scraper": WeatherScraper,
    },
    "Porto Velho_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/343/portovelho-ro",
        "scraper": ClimatempoScraper,
    },
    "Porto Velho_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/porto-velho/35941/weather-forecast/35941",
        "scraper": AccuWeatherScraper,
    },
    "Porto Velho_Weather": {
        "url": "https://weather.com/weather/today/l/2768f085da99b32e071341a2441d2620a549b05a06d130c0d1a1f125a07e0eb4",
        "scraper": WeatherScraper,
    },
    "Boa Vista_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/347/boavista-rr",
        "scraper": ClimatempoScraper,
    },
    "Boa Vista_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/boa-vista/35950/weather-forecast/35950",
        "scraper": AccuWeatherScraper,
    },
    "Boa Vista_Weather": {
        "url": "https://weather.com/weather/today/l/21e58e59f8d6a87c1e91e0e55fbc8bb89a25f0ffe7f4f8039e42c8729c013fbd",
        "scraper": WeatherScraper,
    },
    "Sao Paulo_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/558/saopaulo-sp",
        "scraper": ClimatempoScraper,
    },
    "Sao Paulo_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/s%C3%A3o-paulo/45881/weather-forecast/45881",
        "scraper": AccuWeatherScraper,
    },
    "Sao Paulo_Weather": {
        "url": "https://weather.com/weather/today/l/ebe93c0e09d0cfe19844d4281461901cd8f083c310e64255954758c8dcab784b",
        "scraper": WeatherScraper,
    },
    "Aracaju_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/384/aracaju-se",
        "scraper": ClimatempoScraper,
    },
    "Aracaju_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/aracaju/36757/weather-forecast/36757",
        "scraper": AccuWeatherScraper,
    },
    "Aracaju_Weather": {
        "url": "https://weather.com/weather/today/l/43d4fbadd7efbf4316f9bc45f7141e2b6f1e495e6f9c16c9f558f59615448d9a",
        "scraper": WeatherScraper,
    },
    "Palmas_Climatempo": {
        "url": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/593/palmas-to",
        "scraper": ClimatempoScraper,
    },
    "Palmas_AccuWeather": {
        "url": "https://www.accuweather.com/pt/br/palmas/36879/weather-forecast/36879",
        "scraper": AccuWeatherScraper,
    },
    "Palmas_Weather": {
        "url": "https://weather.com/weather/today/l/3e1f452d6f504871e31b028827eed2b4d9ca68dfb5cb5719bd979a2721eebfc5",
        "scraper": WeatherScraper,
    },
}

# Inicia coleta e salva os dados no JSON
coletor = WeatherDataCollector(cidades)
coletor.coletar_dados()
coletor.salvar_dados_em_json()
