import os
import time
import datetime
import requests
import bs4
#Pegar data do dia
data_atual = datetime.date.today().strftime('%d/%m/%Y')

#Fazer requisição da liturgia (https://liturgia.cancaonova.com/pb/json-liturgia)
url = "https://liturgia.cancaonova.com/pb/json-liturgia"
while True:
    def check_internet():
        try:
            requests.get(url)
            return True
        except requests.exceptions.ConnectionError:
            return False
    if not check_internet():
        print('TENTANDO CONEXÃO COM A INTERNET...')
        time.sleep(3)
        os.system('cls')
    else:
        request = requests.get(url)
        break

#Tratar para JSON a requisição
lista_liturgias = request.json()['liturgias']

#Verificar qual indice do dia atual
for c in range(0, len(lista_liturgias)):
    if lista_liturgias[c]['dia'] == data_atual:
        indice = c

#Verificar se tem 2º leitura
lista_leitura = ['leitura1', 'salmo', 'leitura2', 'evangelho']
if lista_liturgias[indice]['leitura2'] == "":
    lista_leitura = ['leitura1', 'salmo', 'evangelho']

#Pegar 1º e 2º Leitura, Salmo, e Evangelho
for item in lista_leitura:
    lista_textos = []

    html_doc = lista_liturgias[indice][item]
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    titulo = soup.find("p", {"style": "text-align: left;"}).text.strip()

    # Adicionando a resposta do Salmo e modificando "Responsório" para "Salmo"
    if item == 'salmo':
        resposta = soup.findAll("p", {"style": "text-align: left;"})[2].text.strip()
        resposta = titulo.replace("Responsório", "Salmo") + " " + resposta
        lista_textos.append(resposta)

    # Modificando "Anúncio do Evangelho" para "Evangelho"
    if item == 'evangelho':
        if titulo.find("Anúncio") != -1:
            titulo = titulo.replace("Anúncio do Evangelho", "Evangelho")
        lista_textos.append(titulo)

    else:
        lista_textos.append(titulo)
    print(lista_textos)

    # Loop para adicionar os títulos em arquivos de textos
    for item2 in lista_textos:
        with open(f'{item}.txt', 'w', encoding='utf-8') as arquivo:
            arquivo.write(f" {item2} ")