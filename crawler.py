import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import psutil
import plataform
import os, platform, subprocess, re

def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ="sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""

r = requests.get("https://raw.githubusercontent.com/divinity76/intel-cpu-database/master/databases/intel_cpu_database.json")

print("---------------" + os.getcwd())

arquivos = os.listdir(os.getcwd() + "/")

isFound = False;

for arq in arquivos:
    if arq == "data.json":
        print('--------------achei')
        isFound = True
    else: 
        print('ainda n')

if isFound != True:
    open('data.json', 'wb').write(r.content)

conteudo = r.json()

escolha = str(input("Insira o nome do seu processador: "))

dados = []
nomes = []
pr = 0
achou = False

while achou == False:
    for content in conteudo:
        try:
            if(escolha.lower() in conteudo[content]["name"].lower()):
                achou = True
                print(conteudo[content]["Performance"])
                nomes.append(conteudo[content]["name"])
                dados.append(conteudo[content]["Performance"])
        except:
            pr += 1  
            print("algo deu errado")
    if achou == False:
        print("Não encontrado")
        print("Buscaremos as informações na base do seu Computador")
        with open('data.json', 'r') as arquivo, \
             tempfile.NamedTemporaryFile('w', delete=False) as out:
             tempCount = 0
            for linha in arquivo:
                fim = linha[len(arquivo) - 1]
                if tempCount == (len(arquivo) - 2):
                    linha = '   },'
                if tempCount == (len(arquivo) - 1):
                    if fim == '}':
                        print("ACHOU, CODIGO: " + codigo)
                        linha = '   "' + tempCount + '": {\n'
                        linha += '       "name:": "' + get_processor_name() + '", \n'
                        linha += '''        "Performance": {
            "# of Cores": "{psutil.cpu_count(logical=False)}",
            "# of Threads": "{psutil.cpu_count()}",
            "Processor Base Frequency": "${psutil.cpu_freq(percpu=False)['max']}",
            "Max Turbo Frequency": "1.90 GHz",
            "Cache": "2 MB",
            "Bus Speed": "8 GT/s DMI3",
            "TDP": "25 W"
        },
                        '''
                else:
                    print("NÃO ACHOU, CÓDIGO: " + codigo)

                    out.write(linha) # escreve no arquivo temporário

                tempCont += 1
        escolha = str(input("Insira o nome do seu processador: "))





for dado in dados:
    print("Dados: ")
    print("Quantidade de Cores: " + dado["# of Cores"])
    print("Frequencia máxima: " + dado["Max Turbo Frequency"])
    print("Frequencia Base: " + dado["Processor Base Frequency"])
    
header = ['QtdCores', 'MaxFreq', 'baseFreq']
with open(f"{nomes[0]}.csv", 'w') as file:
    count = 0
    for h in header:
        if count < (len(header) - 1):
            file.write(str(h)+', ')
            count += 1
        else:
            file.write(str(h))
    file.write('\n')
    for dado in dados:
        file.write(str(dado["# of Cores"]) + ', ' + '"' +str(dado["Max Turbo Frequency"])+ '"' +', ' + '"' + str(dado["Processor Base Frequency"]) + '"')
    

