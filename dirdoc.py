
"""
Created on Thu Dec  4 22:49:37 2014

@author: srocha
"""

import requests
from bs4 import BeautifulSoup
import re
import logging

# create logger
logger = logging.getLogger('Dirdoc API')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatterencode(self.__encoding)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def requestpost(url,data,headers):
    write = "Post URL = {0}".format(url)
    logger.info(write)
    req = requests.post(url,data=data,headers=headers)
    return req
    
    
def requestget(url,cookies,headers):
    write = "Get URL = {0}".format(url)
    logger.info(write)
    req = requests.post(url,cookies=cookies,headers=headers)
    return req

class Dirdoc():
    
    def __login(self):
        url = self.__loginurl
        data = self.__logindata
        headers = self.__headers
        req = requestpost(url,data,headers)
        if "Bienvenido" not in req.text:
            logger.error("al realizar Login, password y/o rut")
            #raise LoginException("Error al hacer login")
            login = False
        else:
            logger.info("Login Correcto!")
            self.__cookies = req.cookies
            login = True
        return login
        
    def __repr__(self):
        return "API Dirdoc rut = {0}".format(self.rut)
        
    def __getInfo(self,html):
        info = html.select("html body table.pequena tr.centro td")
        rut = info[0].get_text()
        nombre = info[1].text
        estado = info[2].text
        carrera = info[3].text
        return (rut,nombre,estado,carrera)
    
    def __getRamos(self,html):
        reg_exp_link = r'(?<=p2=)\d+'
        ramos = html.select("html body table.pequena tr")[3:]
        todos_ramos = []
        for ramo in ramos:
            ramo = ramo.select("td")
            info_ramo = {}
            info_ramo['id_ramo'] = ramo[0].text.encode(self.__encoding) if ramo[0].text.encode(self.__encoding) is not u'' else None
            info_ramo['nombre'] = ramo[1].text if ramo[1].text is not u'' else None
            info_ramo['profesor'] = ramo[2].text if ramo[2].text is not u'' else None
            info_ramo['seccion ']= int(ramo[3].text) if ramo[3].text is not u'' else None
            info_ramo['estado'] = ramo[4].text if ramo[4].text  is not u'\xa0' else None
            info_ramo['nota_final'] = ramo[5].text.encode(self.__encoding) if ramo[5].text.encode(self.__encoding) is not u'' else None
            if ramo[6].a.get('onclick') > 0:
                id_link = int(re.findall(reg_exp_link, ramo[6].a.get('onclick'))[0])
            else:
                id_link = int(ramo[6].a.get("href").split("/")[-1])
            info_ramo['id_link'] = id_link
            info_ramo['notas'] = self.__getRamo(id_link)
            todos_ramos.append(info_ramo)
        return todos_ramos

    def __getRamo(self,id):
        url = self.__link_nota.format(id)
        cookies = self.__cookies
        headers = self.__headers
        req = requestget(url,cookies,headers)
        html = BeautifulSoup(req.text)
        tables = html.select("html body table.pequena tr")[4:]
        notas = []
        for por,nota in zip(tables[0].select("th"),tables[1].select("th")):
            por = int(re.findall(r'\d+', por.text)[0]) if len(re.findall(r'\d+', por.text)) else None
            nota = float(''.join(nota.text.split(",")[:1])) if len(re.findall(r'\d.\d+', nota.text)) else None
            notas.append({"nota":nota,"porcentaje":por})
        return notas
        
        
        
    
    def __init__(self,rut,password,cache = 100):
        self.__loginurl = "http://postulacion.utem.cl/valida.php"
        self.rut = rut
        self.info = {}
        self.__link_actual = []
        self.__link_antiguos = []
        self.__encoding = 'utf-8'
        self.__urls = dict(
            ramos_actual = 'http://postulacion.utem.cl/alumnos/notas.php', # Muestra los ramos tomados por el estudiante
            notas = 'http://postulacion.utem.cl/alumnos/acta.php', # URL donde se ven las notas, recibe el link del ramo como parametro
            info = 'http://postulacion.utem.cl/inscripcion/horario',
            ramos_ant = "http://postulacion.utem.cl/curricular/notas_anterior",
        )
        self.__link_nota = "http://postulacion.utem.cl/curricular/notas/{0}"
        self.__htmls = {}
        self.__encoding = 'utf-8'
        self.__logindata = dict(
            rut = rut, # Rut del estudiante
            password = password, # Su password
            tipo = 0 # El tipo de usuario es 0 para el estudiante
        )
        self.__headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:21.0) Gecko/20100101 Firefox/21.0'}
        if self.__login():
            logger.info("Obteniendo informacion")
            
            for url in self.__urls.items():
                req = requestget(url[1],self.__cookies,self.__headers)
                self.__htmls[url[0]] = BeautifulSoup(req.text)
            

            self.info['info'] = self.__getInfo(self.__htmls['info'])
            self.info['ramos_actual'] = self.__getRamos(self.__htmls['ramos_actual'])
            self.info['ramos_ant'] = self.__getRamos(self.__htmls['ramos_ant'])
                
        else:
            pass

