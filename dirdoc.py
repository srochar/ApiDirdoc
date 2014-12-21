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

from resultadosInscripciones import ResultadoInscripcion
from informacion import Informacion
from Carreras import Carrera
from AnvanceMalla import  AvanceMalla
from Ramo import Ramo
import jsonpickle
from Nota import Nota,NotaEstable,NotasParciales

class Dirdoc():

    def __parseText(self,data):
        result = data.text.encode(self.__encoding)
        if result == '':
            result = None
        else:
            try:
                result = int(result)
            except:
                if result.find(',') is 1:
                    result = result.replace(',','.')
                    try:
                        result = float(result)
                    except:
                        result = result.rstrip()

        return result

    def __loggerInfo(self,write):
        if self.loggerinfo is True:
            self.logger.info(write)
        else:
            pass

    def __requestpost(self,url):
        write = "Post URL = {0}".format(url)
        self.__loggerInfo(write)
        req = requests.post(url,data=self.__logindata,headers=self.__headers)
        self.__cookies = req.cookies
        html = BeautifulSoup(req.text)
        return html


    def __requestget(self,url):
        write = "Get URL = {0}".format(url)
        self.__loggerInfo(write)
        req = requests.get(url,cookies=self.__cookies,headers=self.__headers)
        html = BeautifulSoup(req.text)
        return html
    
    def __login(self):
        url = self.__loginurl
        html = self.__requestpost(url)
        if "Bienvenido" in html.text:
            write = "Autentificacion Correcta"
            login = True
        elif "Base de datos" in html.text:
            write = "Base de datos de Dirdoc Bajada"
            login = False
        else:
            write = "Usuario y/o contraseña incorrecta"
            login = False
        self.__loggerInfo(write)
        return login
        
    def __getInfo(self):
        html = self.__htmls['info']
        data = html.select("html body table.pequena tr.centro td")
        info_table = ['rut','nombre','estado','carrera']
        info_data = map(self.__parseText,data)
        return Informacion(
            dict(
                zip(info_table,info_data)
            )
        )
        
    def __getIdramo(self,ramo):
        id_ramo = ramo[0].text#.encode(self.__encoding)
        #write = "id_ramo = {0}".format(id_rself.logger.info(write)amo)
        #logger.debug(write)
        if len(unicode(id_ramo.split('\n'))) > 0:
            id_ramo.replace('\n','').replace('\r','')
        return id_ramo

    def __parseRamo(self,ramo):
        reg_exp_link = r'(?<=p2=)\d+'
        ramo = ramo.select("td")
        if ramo[6].a.get('onclick') > 0:
            id_link = int(re.findall(reg_exp_link, ramo[6].a.get('onclick'))[0])
        else:
            id_link = int(ramo[6].a.get("href").split("/")[-1])
        table = ['nombre','profesor','seccion','estado','nota_final','id_link']
        info = map(self.__parseText,ramo)[1:]
        info_ramo = dict(
            #id_ramo = self.__getIdramo(ramo),
            #nombre = ramo[1].text.encode(self.__encoding),
            #profesor = ramo[2].text.encode(self.__encoding),
            #seccion = int(ramo[3].text),
            #estado = ramo[4].text.encode(self.__encoding),
            #nota_final= parseNota(ramo[5]),
            #id_link = id_link,
            #notas = self.__getRamo(id_link)
            zip(table,info),
            id_ramo = self.__getIdramo(ramo),
            notas = self.__getRamo(id_link)

        )
        return info_ramo
    
    def __getRamos(self,html):
        ramos = html.select("html body table.pequena tr")[3:]

        todos_ramos = [
            Ramo(
                dict(
                    self.__parseRamo(ramo)
                )
            )for ramo in ramos
        ]

            #map(self.__parseramo,ramos)

        return todos_ramos


    def __getRamo(self,id):
        url = self.__link_nota.format(id)
        html = self.__requestget(url)
        tables = html.select("html body table.pequena tr")[4:]
        fila_porcentajes = tables[0].select("th")
        fila_notas = tables[1].select('th')
        notas = map(self.__parseText,fila_notas)
        porcentajes = map(self.__parseText,fila_porcentajes)

        list_notas = [
            Nota(dict(
                nota = nota,
                porcentaje = int(re.findall(r'\d+',porcentaje)[0])
            )) for nota,porcentaje in zip(notas,porcentajes)[:-6]
        ]
        notas_representativas = notas[-6:-2] #nota_presentacion,examen1,examen2,notafinal

        n = NotasParciales(list_notas,*notas_representativas)
        return n

    def __getLinkCarrera(self,datos):
        link_carrera = datos.a.get("href")
        query = urlparse.urlparse(link_carrera)[4]
        #logger.debug("link_ramo = {0}".format(query))
        return query

    def __getPlanCarrera(self,malla):
        plan = None
        plan = int(malla.select("html body table.pequena tr")[5].select("td")[1].text)
        return plan

    def __parseAsignaturaMalla(self,asignatura):
        asignatura = asignatura.select('td')
        return map(self.__parseText,asignatura)

    def __getMalla(self,link_malla):
        url = self.__link_malla.format(link_malla)
        html = self.__requestget(url)
        #info_table = [r.text for r in html.select("tr")[6].select("th")] #informacion de la tabla
        info_table = ['nivel','asignatura','tipo','op','estado','seccion','nota']
        asignatura = [asig for asig in  html.select("tr")[7:] if len(asig.select("td")) == 7 ] #todas las asignaturas


        avance = [
            AvanceMalla(
                dict(
                    zip(info_table,self.__parseAsignaturaMalla(asig))
                )
            ) for asig in asignatura
        ]
        #self.logger.info("AVANCE = {0}".format(avance))

        return avance

    def __getAvance(self,carrera):
        carrera = carrera.select("td")[0]
        link_malla = self.__getLinkCarrera(carrera)
        return self.__getMalla(link_malla)

    def __parseInfoCarrera(self,carrera):
        carrera = carrera.select('td')
        return map(self.__parseText,carrera)

    def __getCarreras(self):
        html = self.__htmls['carreras']
        carreras = html.select("html body table.pequena")[1].select("tr")[1:]#todas las carreras
        info_table = ['carrera','estado','semestreIngreso','semestreTermino']
        return [
           Carrera(
               dict(
                   zip(info_table,self.__parseInfoCarrera(carrera)),
                   avance = self.__getAvance(carrera)
               )) for carrera in carreras
        ]


    def __parseResultado(self,ramo):
        ramo = ramo.select('td')
        return map(self.__parseText,ramo)

    def __getResultadoInscritos(self):
        html = self.__htmls['resultado']

        info_table = ['codigo','nombreAsignatura','seccion','estado','horario']
        ramos = html.select("html body table.pequena")[1].select("tr.centro")

        resultados = [
            ResultadoInscripcion(dict(
                zip(info_table,self.__parseResultado(ramo))
            ))  for ramo in ramos
        ]

        return resultados


    def __logout(self):
        url = self.__logouturl
        html = self.__requestpost(url)

    
    def __init__(self,rut,password,cache = 100,loggerinfo = False,debug=False):
        self.debug = debug
        self.loggerinfo = False
        self.__loginurl = "http://postulacion.utem.cl/valida.php"
        self.__logouturl = "http://postulacion.utem.cl/alumnos/desconexion.php"
        self.rut = rut
        self.__encoding = 'utf-8'
        self.__urls = dict(
            ramos_actual = 'http://postulacion.utem.cl/alumnos/notas.php', # Muestra los ramos tomados por el estudiante
            notas = 'http://postulacion.utem.cl/alumnos/acta.php', # URL donde se ven las notas, recibe el link del ramo como parametro
            info = 'http://postulacion.utem.cl/inscripcion/horario', #URL donde se obtiene los horarios de los ramos aceptados
            ramos_anterior = "http://postulacion.utem.cl/curricular/notas_anterior", #URL de los ramos del semestre anterior
            carreras = 'http://postulacion.utem.cl/curricular', #URL donde se encuentre las carreras inscritas por el estudiante
            resultado = 'http://postulacion.utem.cl/inscripcion/resultado', #URL resultados de los ramos inscritos
        )
        self.__link_nota = "http://postulacion.utem.cl/curricular/notas/{0}"# URL para para obtener la informacion de un ramo
        self.__link_malla = "http://postulacion.utem.cl/curricular/avance?{0}"# Formato de la url de la malla de una carrera
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

        self.__htmls = {}
        if self.__login():
            write = "Obteniendo informacion"
            self.__loggerInfo(write)
            
            for key,url in self.__urls.items():
                self.__htmls[key] = self.__requestget(url)


            self.ramos_anterior = self.__getRamos(self.__htmls['ramos_anterior'])
            self.info = self.__getInfo()
            self.ramos_actual = self.__getRamos(self.__htmls['ramos_actual'])
            self.carreras = self.__getCarreras()
            self.resultado = self.__getResultadoInscritos()

            self.__logout()
                
        else:
            self.ramos_anterior = self.info = self.ramos_actual = self.carreras = self.resultado = None


    def to_JSON(self):
        return jsonpickle.encode(
            (
                dict(
                    ramos_anterior = self.ramos_anterior,
                    info = self.info,
                    ramos_actual = self.ramos_actual,
                    carreras = self.carreras,
                    resultado = self.resultado,
                )
            )
        )


    def __repr__(self):
        return "API Dirdoc rut = {0}".format(self.rut)

    def __str__(self):
        return str(
            'ramos_anterior: {0} , info: {1} , ramos_actual: {2} , '
            'carreras: {3} , resultado: {4}'.format(
                self.ramos_anterior,self.info,
                self.ramos_actual,self.carreras,
                self.resultado)
        )