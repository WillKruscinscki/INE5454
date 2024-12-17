import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime


class AccuWeatherScraper:
    def __init__(self, url):
        self.url = url

    def coletar_dados(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            site = BeautifulSoup(response.content, "html.parser")

            # pega temperatura e limpa
            temperatura_info = site.find("div", class_="temp")
            temperatura = (
                temperatura_info.get_text(strip=True).replace("°", "").replace("C", "")
                if temperatura_info
                else "Não disponível"
            )

            # pega vvelocidade vento no formato "min - max"
            vento_valor, rajada_valor = "Não disponível", "Não disponível"
            for item in site.find_all("div", class_="spaced-content detail"):
                label = item.find("span", class_="label")
                value = item.find("span", class_="value")
                if label and value:
                    if "Vento" in label.get_text():
                        vento_valor = value.get_text(strip=True).split()[-2]
                    elif "Rajadas de vento" in label.get_text():
                        rajada_valor = (
                            value.get_text(strip=True).replace("km/h", "").strip()
                        )

            vento_formatado = (
                f"{vento_valor} - {rajada_valor}"
                if vento_valor != "Não disponível" and rajada_valor != "Não disponível"
                else "Não disponível"
            )

            # pega umidade
            umidade = "Não disponível"
            script_tag = site.find("script", text=lambda x: x and '"cuhd":"' in x)
            if script_tag:
                script_content = script_tag.string
                start_index = script_content.find('"cuhd":"') + len('"cuhd":"')
                end_index = script_content.find('"', start_index)
                umidade = script_content[start_index:end_index]

            # pega qualidade do ar
            qualidade_ar_info = None
            for item in site.find_all("div", class_="spaced-content detail"):
                label = item.find("span", class_="label")
                if label and "Qualidade do ar" in label.get_text():
                    qualidade_ar_info = item.find("span", class_="value").get_text(
                        strip=True
                    )
                    break
            qualidade_ar = (
                unidecode(qualidade_ar_info) if qualidade_ar_info else "Não disponível"
            )

            # pega sensação térmica
            real_feel_info = site.find("div", class_="real-feel")
            sensacao_termica = (
                real_feel_info.get_text(strip=True)
                .replace("RealFeel®", "")
                .replace("°", "")
                .strip()
                if real_feel_info
                else "Não disponível"
            )

            return {
                "temperatura": temperatura,
                "umidade": umidade,
                "vento": vento_formatado,
                "qualidade_do_ar": qualidade_ar,
                "sensacao_termica": sensacao_termica,
                "URL": self.url,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }

        except Exception as e:
            print(f"Ocorreu um erro ao coletar dados do AccuWeather: {e}")
            return None
