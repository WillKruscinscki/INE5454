import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime


class WeatherScraper:
    def __init__(self, url):
        self.url = url

    def fetch_content(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            print(f"Conexão estabelecida com sucesso para {self.url}")
            return BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            print(f"Erro ao acessar o site: {e}")
            return None

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        return round((fahrenheit - 32) * 5.0 / 9.0)

    def coletar_dados(self):
        site = self.fetch_content()
        if not site:
            return None

        # pega temperatura e converet fahrenheit - celsius
        temperatura_info = site.find("span", {"data-testid": "TemperatureValue"})
        temperatura = (
            str(
                self.fahrenheit_to_celsius(
                    int(temperatura_info.get_text(strip=True).replace("°", ""))
                )
            )
            if temperatura_info
            else "Não disponível"
        )

        # pega umidade
        umidade_info = site.find("span", {"data-testid": "PercentageValue"})
        umidade = (
            umidade_info.get_text(strip=True).replace("%", "")
            if umidade_info
            else "Não disponível"
        )

        # pega velocidade vento e converte mph - kmh
        vento_info = site.find("span", {"data-testid": "Wind"})
        if vento_info and len(vento_info.find_all("span")) > 1:
            vento_mph = vento_info.find_all("span")[1].get_text(strip=True)
            try:
                vento_valor = str(int(round(int(vento_mph) * 1.60934)))
            except ValueError:
                vento_valor = "Não disponível"
        else:
            vento_valor = "Não disponível"

        # ppega qualidade do ar
        qualidade_ar_info = site.find("span", {"data-testid": "AirQualityCategory"})
        qualidade_do_ar = (
            unidecode(qualidade_ar_info.get_text(strip=True))
            if qualidade_ar_info
            else "Não disponível"
        )

        # pega sensação terminica e converte fahrenheit - celsius
        sensacao_termica_info = site.find(
            "span",
            {"data-testid": "TemperatureValue"},
            class_="TodayDetailsCard--feelsLikeTempValue--8WgHV",
        )
        sensacao_termica = (
            str(
                self.fahrenheit_to_celsius(
                    int(sensacao_termica_info.get_text(strip=True).replace("°", ""))
                )
            )
            if sensacao_termica_info
            else "Não disponível"
        )

        return {
            "temperatura": temperatura,
            "umidade": umidade,
            "vento": vento_valor,
            "qualidade_do_ar": qualidade_do_ar,
            "sensacao_termica": sensacao_termica,
            "URL": self.url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
