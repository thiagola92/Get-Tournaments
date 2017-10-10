# Primeiro instalar python
# Instalar selenium com o comando 'pip install selenium'
# Baixar ChromeDriver
# (windows) Incluir nas variaveis do ambiente do windows a localização do ChromeDriver
# (linux) Trocar "webdriver.Chrome()" por "webdriver.Chrome(CHROME_DIR)"

import threading
import time
import datetime
from selenium import webdriver                               
from selenium.webdriver.common.keys import Keys

# Confira se TEXT_DIR e CHROME_DIR estão corretos

TEXT_DIR = "C:\\Users\\ThiagoLA92\\Downloads\\info.js"	
print("-Escrever no arquivo: " + TEXT_DIR)	

CHROME_DIR = "C:\\Users\\ThiagoLA92\\Downloads\\chromedriver.exe"
print("-Localizacao do chromedriver: " + CHROME_DIR)

# Opcional

WAIT_THIS_TIME = 5                                                                  # Esperar X segundos após a página terminar de carregar para pegar o codigo dela (isso existe pois já aconteceu de pegar o codigo antes da página terminar de carregar)
MAX_THREADS = 15                                                                    # Numero máximo de janelas que podem ficar abertar ao mesmo tempo (muitas janelas podem consumir muito do seu computador)

#.....##....##....#######.######.######.##..##.######..........
#.....###...##....#######.######.######.##..##.######..........
#.....####..##......##....##..##.##..##.##..##.##..............
#.....##.##.##......##....##..##.##..##.##..##.######..........
#.....##..####......##....##..##.##..##.##..##.##..............
#.....##...###......##....######.######.##..##.######..........
#.....##....##......##....######.######.######.######..........
#....................................##........................
#....................................##........................


eventsPage = "http://events.br.leagueoflegends.com/"                                # Link da página dos Eventos
i = 0                                                                               # Numero de Eventos
MAX_THREADS = 15                                                                    # Numero máximo de threads que esse programa rodar

getLink = []                                                                        # Lista dos Links
getDay = []							                                                # Dia do evento
getHour = []                                                                        # Horario do evento
getMap = []                                                                         # Mapa
getType = []                                                                        # Tipo do evento (online, presencial, misto)
getCreator = []                                                                     # Organizador do evento
getPick = []                                                                        # Tipo do evento (blind pick, draft pick...)


###############################################################################################################################

def read_page(page):
 global getLink
 global i
 
 print("-Abrindo navegador")
 browser = webdriver.Chrome()
 browser.get(page)
 
 #################################
 #try:
   #while (True):
 # element = browser.find_element_by_xpath("//a[@class='_2PXCVymucv8Msd5mFKsB4V']")      # Procurando um link que tenha o texto "Exibir mais"
 # print(element.text)
 # element.click()
 #except Exception as e:
 # print(str(e))
 #################################
 
 print("-Pegando o codigo da pagina")
 time.sleep(WAIT_THIS_TIME)                                                                      # Esse sleep é importante pois algumas vezes estava pegando o codigo antes da página terminar de carregar
 html = browser.page_source
 browser.quit()
 
 print("-Retirando characters fora do formato UTF-8")
 html = html.encode("ascii","ignore")
 
 print("-Convertendo para string, trocando characters que podem dar problema depois")
 html = str(html)
 html = html.replace('\\n','\n')
 html = html.replace("\"","\'")
 
 position = 1                                                                       # Posição no codigo HTML (note que essa variavel não é global)
 
 print("-Procurando eventos na pagina: " + page)
 while (html.find("href=\'/events/", position) != -1):
  
  print("--Pegando o link do evento")
  position = html.find("href=\'/events/", position) + 6
  position2 = html.find("\'", position)
  getEvent = html[position+1:position2]
  temp = eventsPage + getEvent 
  
  
  print("--Verificando se o link do evento já esta salvo")
  exist = False
  for num in range(0,i):
   if (temp == getLink[num]):
    print("---Link já existe")
    exist = True
    break
  
  if (exist == False):
   print("---Link não existia, salvando o link " + temp)
   getLink.append(temp)
   i = i + 1
  
  position = position+1
  # Pular o próximo link pois o mesmo link aparece duas vezes na mesma página
  position = html.find("/events/", position)
  position = position+1

 position = 1
 
 while (html.find("href=\'/search/", position) != -1):
  print("-Abrindo um link do \"VER TODOS OS EVENTOS\"")
 
  position = html.find("href=\'/search/", position) + 6
  position2 = html.find("\'", position)
  getMore = html[position+1:position2]
  
  print("--Pagina a ser aberta: " + (eventsPage + getMore))
  read_page(eventsPage + getMore)
  position = position + 1

##################################################################################################################################  

def get_info(i):
 global getLink
 
 print("-Abrindo navegador")
 browser = webdriver.Chrome()
 browser.get(getLink[i])
 
 print("-Pegando codigo da pagina")
 time.sleep(WAIT_THIS_TIME)                                                                      # Esse sleep é importante pois algumas vezes estava pegando o codigo antes da página terminar de carregar
 html = browser.page_source
 browser.quit()
 
 print("-Retirando characters fora do formato UTF-8")
 html = html.encode("ascii","ignore")
 
 print("-Convertendo para string, trocando characters que podem dar problema depois")
 html = str(html)
 html = html.replace('\\n','\n')
 html = html.replace("\"","\'")
 
 # Importante que para cada informação que queremos do codigo, precisamos achar uma caracteristica unica então a maneira de pegar cada informação vai ser diferente da outra
 # Note que se ele encontrar em algum lugar da página escrito "Torneio online</span>" ele vai achar que é torneio online (isso vale para todas as opções). Não pensei em uma maneira melhor de saber o que é o evento.
 print("-Pegando o tipo do evento")
 temp = html.find("Torneio online</span>")
 if (temp != -1):
  getType[i] = "Torneio online"
 else:
  temp = html.find("Torneio Misto</span>")
  if (temp != -1):
   getType[i] = "Torneio Misto"
  else:
   temp = html.find("Torneio presencial</span>")
   if (temp != -1):
    getType[i] = "Torneio presencial"
   else:
    getType[i] = "Não é torneio"
 
 print("-Pegando o dia do evento")
 temp = html.find("Incio do evento:")
 temp = html.find("<span", temp)
 temp = html.find(">", temp+1) + 1
 temp1 = html.find(" ", temp)
 getDay[i] = html[temp:temp1]
 
 print("-Pegando o horario do evento")
 temp = html.find(" ",temp1+1)
 temp = html.find(" ",temp+1) + 1
 temp1 = html.find(" ",temp)
 getHour[i] = html[temp:temp1]
 
 print("-Pegando o mapa do evento")
 temp = html.find("Mapa")
 temp =  html.find("<div", temp)
 temp = html.find(">", temp+1) + 1
 temp1 = html.find("<", temp)
 temp = (html[temp:temp1]).replace("\\'","\'")
 getMap[i] = temp

 print("-Pegando o organizador do evento")
 temp = html.find("Organizador:")
 temp = html.find("\'>", temp) + 2
 temp1 = html.find("<", temp)
 getCreator[i] = html[temp:temp1]
 
 print("-Se tiver link para o battlefy tentar pegar as informacoes dele")
 temp = html.find("href=\'https://battlefy.com/")
 if (temp != -1):
  
  temp = temp + 6                                      # Passando pelo href='
  temp1 = html.find("\'", temp)
  tournamentWebsite = html[temp:temp1]
  
  print("--Se tiver um link maior do battlefy, assumir que ele eh o link do torneio")
  while(1==1):
  
   temp = html.find("href=\'https://battlefy.com/", temp)
   
   if (temp == -1):
    break
    
   temp = temp + 6                                      # Passando pelo href='
   temp2 = html.find("\'", temp)
   tempWebsite = html[temp:temp2]
   
   if (len(tournamentWebsite) < len(tempWebsite)):
    tournamentWebsite = tempWebsite
   
  print("--Abrindo com navegador o site do torneio")
  browser = webdriver.Chrome()
  browser.get(tournamentWebsite)
  time.sleep(WAIT_THIS_TIME)
  html2 = browser.page_source
  browser.quit()
  
  print("--Retirando characters fora do formato UTF-8")
  html2 = html2.encode("ascii","ignore")
  
  print("-Convertendo para string, trocando characters que podem dar problema depois")
  html2 = str(html2)
  html2 = html2.replace('\\n','\n')
  html2 = html2.replace("\"","\'")
 
  temp = html2.find("Game Map")
  if (temp != -1):
   temp = html2.find("<h4>", temp) + 4
   temp2 = html2.find("</h4>", temp)
   getPick[i] = html2[temp:temp2]
  else:
   getPick[i] = "null"
   
 else:
  getPick[i] = "null"
  
##################################################################################################################################

print("#### Abrindo a pagina que deve ser lida ####")
read_page(eventsPage)

#######################################################################################################################################

print("#### Pegando as informacoes de todos os " + str(i) + " eventos ####")
for num in range(0,i):

 print("-Criando os locais no vetor")
 getDay.append(None)
 getHour.append(None)
 getMap.append(None)
 getType.append(None)
 getCreator.append(None)
 getPick.append(None)

 print("-Criando um thread para cuidar do evento " + str(num))
 t = threading.Thread(target=get_info, args=(num,))
 t.start()

 # Limitando o numero de threads em execução para evitar problemas com o computador
 while (threading.active_count() > MAX_THREADS):
  time.sleep(1)

# Enquanto existir mais que a thread do programa rodando, esperar as outras threads terminarem
while (threading.active_count() != 1):
  time.sleep(1)

#######################################################################################################################################

print("#### Mostrando no terminal toda informacao pega")
for num in range(0,i):
 print("---" + str(num) + "---")
 print(getLink[num])
 print("Tipo: " + getType[num])
 print("Dia: " + getDay[num])
 print("Hora: " + getHour[num])
 print("Mapa: " + getMap[num])
 print("Organizador: " + getCreator[num])
 print("Pick: " + getPick[num])

########################################################################################################################################

print("#### Escrevendo a pagina javascript ####")
file = open(TEXT_DIR,"w")

file.write("\tvar eventInfo = []\n")
file.write("\tvar eventNumb = " + str(i) + " \n")
for num in range(0,i):
 file.write("\teventInfo[" + str(num) + "] = {link: \"" + getLink[num] + "\", type: \"" + getType[num] + "\", day: " + getDay[num] + ", hour: " + (getHour[num])[:2] + ", min: " + (getHour[num])[3:] + ", map: \"" + getMap[num] + "\", pick: \"" + getPick[num] + "\", creator: \"" + getCreator[num] + "\"}\n")
file.write("\tvar lastUpdate = \'" + str(datetime.date.today()) + "\'")
file.close()

#########################################################################################################################################

print("#### END ####")