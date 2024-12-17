import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime


class ClimatempoScraper:
    def __init__(self, url):
        self.url = url

    def fetch_content(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                print(f"Conexão estabelecida com sucesso para {self.url}")
                return BeautifulSoup(response.content, "html.parser")
            else:
                print(f"Falha na conexão: {response.status_code}")
                return None
        except Exception as e:
            print(f"Erro ao acessar o site: {e}")
            return None

    def coletar_dados(self):
        site = self.fetch_content()
        if not site:
            return None

        # pega temperatura e limpa
        temperatura = site.find(
            "span", class_="-bold -gray-dark-2 -font-55 _margin-l-20 _center"
        )
        temperatura = (
            temperatura.text.strip().replace("º", "")
            if temperatura
            else "Nao disponivel"
        )

        # pega temperatura umidade e limpa
        umidade = site.find("span", class_="-gray-light")
        umidade = umidade.text.strip().replace("%", "") if umidade else "Nao disponivel"

        # pega velocidade vento no formato "min - max"
        vento = "Nao disponivel"
        vento_info = site.find_all("li", class_="item")
        for item in vento_info:
            if item.find("span", class_="variable", string="Vento"):
                vento_valor = item.find_all("div", class_="_flex")[1]
                if vento_valor:
                    vento_texto = (
                        vento_valor.get_text(separator="", strip=True)
                        .replace("km/h", "")
                        .strip()
                    )
                    partes_vento = [
                        part.strip()
                        for part in vento_texto.split("-")
                        if part.strip().isdigit()
                    ]
                    vento = " - ".join(partes_vento)
                break

        # pega qualidade do ar
        qualidade_ar_info = site.find(
            "li", class_="item", attrs={"data-id": "Card_Health_Item_AirQuality"}
        )
        qualidade_ar = (
            unidecode(qualidade_ar_info.find("p", class_="value").text.strip())
            if qualidade_ar_info
            else "Nao disponivel"
        )

        # pega sensação térmica
        sensacao_info = site.find(
            "div",
            class_="no-gutters -gray _flex _justify-center _margin-t-20 _padding-b-20 _border-b-light-1",
        )
        sensacao_termica = (
            sensacao_info.get_text(strip=True)
            .replace("Sensação:", "")
            .replace("°", "")
            .strip()
            if sensacao_info
            else "Nao disponivel"
        )

        return {
            "temperatura": temperatura,
            "umidade": umidade,
            "vento": vento,
            "qualidade_do_ar": qualidade_ar,
            "sensacao_termica": sensacao_termica,
            "URL": self.url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
