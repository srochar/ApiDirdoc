# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 22:49:37 2014

@author: srocha
"""
import requests
from bs4 import BeautifulSoup
import re
import logging
import urlparse

class Dirdoc():

    def __requestpost(self,url):
        write = "Post URL = {0}".format(url)
        self.logger.info(write)
        req = requests.post(url,data=self.__logindata,headers=self.__headers)
        self.__cookies = req.cookies
        html = BeautifulSoup(req.text)
        return html


    def __requestget(self,url):
        write = "Get URL = {0}".format(url)
        self.logger.info(write)
        req = requests.get(url,cookies=self.__cookies,headers=self.__headers)
        html = BeautifulSoup(req.text)
        return html
    
    def __login(self):
        url = self.__loginurl
        html = self.__requestpost(url)
        if "Bienvenido" not in html.text:
            self.logger.error("al realizar Login, password y/o rut")
            login = False
        else:
            self.logger.info("Login Correcto!")
            login = True
        return login
        
    def __repr__(self):
        return "API Dirdoc rut = {0}".format(self.rut)
        
    def __getInfo(self):
        html = self.__htmls['info']
        info = html.select("html body table.pequena tr.centro td")
        rut = info[0].get_text()
        nombre = info[1].text
        estado = info[2].text
        carrera = info[3].text
        return (rut,nombre,estado,carrera)
        
    def __getIdramo(self,ramo):
        id_ramo = ramo[0].text#.encode(self.__encoding)
        write = "id_ramo = {0}".format(id_ramo)
        #logger.debug(write)
        if len(unicode(id_ramo.split('\n'))) > 0:
            id_ramo.replace('\n','').replace('\r','')
        return id_ramo
    
    def __getRamos(self,html):
        reg_exp_link = r'(?<=p2=)\d+'
        ramos = html.select("html body table.pequena tr")[3:]
        todos_ramos = []
        write = "Ramos = {0}".format(ramos)
        #logger.debug(write)
        for ramo in ramos:
            ramo = ramo.select("td")
            info_ramo = {}
            info_ramo['id_ramo'] = self.__getIdramo(ramo)
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
        html = self.__requestget(url)
        tables = html.select("html body table.pequena tr")[4:]
        notas = []
        for por,nota in zip(tables[0].select("th"),tables[1].select("th")):
            por = int(re.findall(r'\d+', por.text)[0]) if len(re.findall(r'\d+', por.text)) else None
            nota = float(''.join(nota.text.split(",")[:1])) if len(re.findall(r'\d,\d+', nota.text)) else None
            notas.append({"nota":nota,"porcentaje":por})
        return notas

    def __getLinkCarrera(self,datos):
        link_carrera = datos.a.get("href")
        query = urlparse.urlparse(link_carrera)[4]
        #logger.debug("link_ramo = {0}".format(query))
        return query

    def __getPlanCarrera(self,malla):
        plan = None
        plan = int(malla.select("html body table.pequena tr")[5].select("td")[1].text)
        return plan

    def __getMalla(self,link_malla):
        url = self.__link_malla.format(link_malla)
        html = self.__requestget(url)
        avance = []
        #avance['plan'] = self.__getPlanCarrera(html)
        todos_ramos = html.select("tr")[7:]
        info_tab = html.select("tr")[6].select("th")
        ramos = [ l.select("td") for l in todos_ramos ]
        #self.logger.info('info_tab = {0}'.format(info_tab))
        #self.logger.info("ramos = {0}".format(ramos))
        for ramo in ramos:
            l = {}
            for i,info in enumerate(info_tab):
                if len(ramo) is 7:
                    l[info.text] = ramo[i].text
            avance.append(l)

        return avance
    
        
    def __getCarreras(self):
        html = self.__htmls['carreras']
        info_table = html.select("html body table.pequena")[1].select("tr")[0].select("th")#info de la tabla
        carreras = html.select("html body table.pequena")[1].select("tr")[1:]#todas las carreras
        #logger.debug("info_table = {0}".format(info_table))
        #logger.debug("carreras = {0}".format(carreras))
        carreras_parse = []
        for carrera in carreras:
            carrera = carrera.select("td")
            carrera_parse = {}
            for (i,info) in enumerate(info_table):
                dato = carrera[i]
                if i is 0:
                    link_malla = self.__getLinkCarrera(dato)
                    carrera_parse['link'] = link_malla
                    carrera_parse['avance'] = self.__getMalla(link_malla)
                carrera_parse[info.text] = carrera[i].text
            carreras_parse.append(carrera_parse)
        return carreras_parse

    def __getResultadoIns(self):
        html = self.__htmls['resultado']
        info_table = [i.text for i in html.select("html body table.pequena")[1].select("tr.titulo_fila th")]
        ramos = html.select("html body table.pequena")[1].select("tr.centro")
        #logger.debug("info_table ={0}".format(info_table))
        #logger.debug("ramos = {0}".format(ramos))
        resultados = []
        for ramo in ramos:
            res = {}
            dat = [i.text for i in ramo.select("td")]
            for (i,info) in enumerate(info_table):
                res[info] = dat[i]
            resultados.append(res)
        return resultados

    def __logout(self):
        url = self.__logouturl
        html = self.__requestpost(url)

    
    def __init__(self,rut,password,cache = 100,debug=False):
        self.debug = debug
        self.__loginurl = "http://postulacion.utem.cl/valida.php"
        self.__logouturl = "http://postulacion.utem.cl/alumnos/desconexion.php"
        self.rut = rut
        self.info = {}
        self.__encoding = 'utf-8'
        self.__urls = dict(
            ramos_actual = 'http://postulacion.utem.cl/alumnos/notas.php', # Muestra los ramos tomados por el estudiante
            notas = 'http://postulacion.utem.cl/alumnos/acta.php', # URL donde se ven las notas, recibe el link del ramo como parametro
            info = 'http://postulacion.utem.cl/inscripcion/horario',
            ramos_ant = "http://postulacion.utem.cl/curricular/notas_anterior",
            carreras = 'http://postulacion.utem.cl/curricular',
            resultado = 'http://postulacion.utem.cl/inscripcion/resultado',
        )
        self.__link_nota = "http://postulacion.utem.cl/curricular/notas/{0}"
        self.__link_malla = "http://postulacion.utem.cl/curricular/avance?{0}"#esta url ya no se usa pero me alimento de ella
        self.__htmls = {}
        self.__encoding = 'utf-8'
        self.__logindata = dict(
            rut = rut, # Rut del estudiante
            password = password, # Su password
            tipo = 0 # El tipo de usuario es 0 para el estudiante
        )
        self.__headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:21.0) Gecko/20100101 Firefox/21.0'}
        #Logger
        self.logger = logging.getLogger('Dirdoc API')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        if self.__login():
            self.logger.info("Obteniendo informacion")
            
            for tupl in self.__urls.items():
                key,url = tupl[0],tupl[1]
                self.__htmls[key] = self.__requestget(url)
            

            self.info['info'] = self.__getInfo()
            self.info['ramos_actual'] = self.__getRamos(self.__htmls['ramos_actual'])
            self.info['ramos_ant'] = self.__getRamos(self.__htmls['ramos_ant'])
            self.info['carreras'] = self.__getCarreras()
            self.info['resultado'] = self.__getResultadoIns()

            self.__logout()
                
        else:
            pass

