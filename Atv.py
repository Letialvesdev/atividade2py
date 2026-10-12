import datetime
import requests


def cotar():
    hoje = datetime.date.today()
    dias = [hoje - datetime.timedelta(days=i) for i in range(365)]

    cotacoes = []
    ultima = None

    for dia in dias:
        data = dia.strftime("%m-%d-%Y")
        url = (
            "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
            f"CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data}'&$format=json"
        )
        try:
            resposta = requests.get(url, timeout=10)
            dados = resposta.json().get("value", [])
        except (requests.RequestException, ValueError):
            dados = []

        if dados:
            ultima = dados[0]["cotacaoCompra"]
        cotacoes.append(ultima)

    primeiro = next((c for c in cotacoes if c is not None), None)
    return [primeiro if c is None else c for c in cotacoes]


resultado = cotar()
print(len(resultado))
print(resultado)