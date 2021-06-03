#Importando as bibliotecas necessárias [pip install requests], [pip install beautifulsoup4]
#Todas as outras bibliotecas são padrões do Python
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import requests
import datetime
import time

#Pegar localização do diretório atual
diretorio_atual = os.getcwd()

#Pegar as informações de data e dia da semana formatados
data_e_hora_atuais = datetime.datetime.now()
data_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
hora = data_e_hora_atuais.strftime('%H:%M')

#Verificar conexão com a Internet
cont = 1
while True:
    if cont == 1:
        print('Iniciando script...')
    cont += 1
    escrever = os.system('ping 172.217.6.36 > teste_conexao.txt')
    with open('teste_conexao.txt', 'r') as file:
        leitura = file.read()
    os.system('cls')
    print("Verificando conexão com a Internet.")
    time.sleep(1)
    os.system('cls')
    print("Verificando conexão com a Internet..")
    time.sleep(1)
    os.system('cls')
    print("Verificando conexão com a Internet...")
    if 'ms' in leitura:
        print('Conexão bem sucedida!')
        time.sleep(1)
        print('Recebendo informações necessárias...')
        time.sleep(3)
        break

#Faz a requisição ao site da Canção Nova
url_liturgia = "https://liturgia.cancaonova.com/pb/json-liturgia/"
dados = requests.get(url_liturgia)

# Verificar qual "i" se refere ao dia de hoje
i = 0
while True:
    elemento = dados.json()["liturgias"][i]["dia"]
    if elemento == data_em_texto:
        break
    i += 1

#Condição para transformar a liturgia de sábado a mesma de domingo
if "Sábado" in dados.json()["liturgias"][i]["titulo"] and hora > 12:
    i -= 1
#Lista das leituras da Santa Missa (Dia de semana não tem 2º Leitura)
lista = ["leitura1", "salmo", "leitura2", "evangelho"]
if dados.json()["liturgias"][i]["leitura2"] == "":
    lista = ["leitura1", "salmo", "evangelho"]


#Cria as pastas necessárias
if not os.path.exists("paginas_html"):
    os.mkdir("paginas_html")
if not os.path.exists("arquivos_txt"):
    os.mkdir("arquivos_txt")
for item in lista:
    

    #Criar para cada item da lista um arquivo .html somente com a leitura do dia
    with open(f"{diretorio_atual}/paginas_html/{item}.html", "w", encoding="utf-8") as arquivo:
        arquivo.write(dados.json()["liturgias"][i][f"{item}"])
    
    #Extrair do .html somente o título das leituras do dia
    url = f'file:///{diretorio_atual}/paginas_html/{item}.html'
    html = urlopen(url)
    bs = BeautifulSoup(html, 'lxml')
    titulo = bs.select('p strong')[0].text
    
    #Quando for o Salmo, adiciona a resposta.
    if item == "salmo":
        titulo = f"{bs.select('p strong')[0].text} {bs.select('p strong')[1].text} — "
    
    #Criar arquivos .txt para cada título das leituras do dia
    with open(f"{diretorio_atual}/arquivos_txt/{item}.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(str(titulo))
