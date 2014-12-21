##Dirdoc.py

Es una app realiza en **python** que obtiene los principales (hasta el momento) datos de la página postulacion.utem.cl, como usuario **estudiante**
Lo que realiza es un pequeño parser de html a un texto para manipular por medio de una un app. La idea es final es crear un API, en el cual se puedan
realizar algunas peticiones básicas.

Para utilizar dirdoc.py
=======================

se debe crear un Objecto de Dirdoc, enviando las credenciales del usuario

    import dirdoc
    m = dirdoc.Dirdoc(rut='TURUT',password='TUPASSWORD')

Comenzara a correr un logger que indica que ifnormacion de esta obteniendo por ejemplo mi caso es:

    m = dirdoc.Dirdoc(rut=rut,password=password)

Si todo sale correcto, se pueden acceder a los datos que obtuvo el parse, que son:
- info
	* nombre: Nombre del Estudiante
    * estado: Estado que se encuentra el estudiante (Matriculada,Elimindado,..)
    * carrera: Ultima carrera que tiene registrada
    * rut: Rut del estdudiante
- carrerass
	* Lista de carrera
    	- avance: Anvace de malla de la carrera
        - carrera:  nombre de la carrera
        - semestreIngreso: Semestre registrado registrado
        - semestreTermino: Semestre de termino registrado
- resultados
	* Lista de Asignatura
    	- codigo: codigo de la asignatura
        - estado: Resultado de la inscripcion (acpetado, rechazada)
        - horario: horario asignado, si el ramo es acpetad
        - nombreAsignatura: nombre de la asignatura
        - seccion: seccion a la que fue designado, en esa asignatura
- ramos_actual
	* Lista de Ramos
    	- estado: Si fue aprobado, reprobado, etc..
        - id_ramo: codigo que tiene el ramo
        - nombre: nombre del ramo
        - nota_final: nota final del ramo
        - notas:
        	- Lista de notas
            	* basicas: Lista de todas las nota principales
                	* Ejemplo: 
                    			notas = [{'nota': 5.5 'porcentaje': 15},...]
								notas.basicas[0].nota 5.5
                                notas.basica[0].porcentaje 15
                * examen1: nota del examen1
                * examen2: nota del examen2
                * nota_final: notal final del ramo
                * nota_presentacion: podenderado que tiene el ramo
- ramos_anterior
	* Mismo que ramos_actual
- rut
	* Rut del estudiante

Ejemplo:
	
    In [1]: import dirdoc

    In [2]: m = dirdoc.Dirdoc(rut='17958150',password='asdf123')

    In [3]: m.info
    Out[3]: nombre = SEBASTIAN IGNAC  ROCHA REYES , rut = 17.958.150-7

    In [4]: print m.info
    {'nombre': 'SEBASTIAN IGNAC  ROCHA REYES', 'estado': 'Transitorio', 'carrera': '21030 INGENIER\xc3\x8dA EN INFORM\xc3\x81TICA', 'rut': '17.958.150-7'}

    In [5]: c = m.carreras[0].avance

    In [6]: c[:5]
    Out[6]: 
    [asignatura = INTRODUCCIÓN A LA INGENIERÍA , nota = 5.0,
     asignatura = TÉCNICAS DE LA COMUNICACIÓN ORAL Y ESCRITA , nota = 4.0,
     asignatura = QUÍMICA GENERAL , nota = 4.5,
     asignatura = CÁLCULO I , nota = 6.3,
     asignatura = ÁLGEBRA , nota = 4.8]

    In [7]: c[0].nota
    Out[7]: 5.0

    In [8]: b = m.ramos_actual

    In [9]: b
    Out[9]: 
    [ramo = AUDITORÍA DE SISTEMAS , nota_final = 4.4,
     ramo = EFE: INTELIGENCIA ARTIFICIAL , nota_final = 5.1,
     ramo = EFE: LOGICA DIFUSA , nota_final = 4.9,
     ramo = PRACTICA PROFESIONAL , nota_final =  ,
     ramo = TRABAJO DE TITULACIÓN I , nota_final =  ]

    In [10]: auditoria = b[0]

    In [11]: auditoria.nombre, auditoria.estado, auditoria.notas
    Out[11]: 
    ('AUDITOR\xc3\x8dA DE SISTEMAS',
     'APROBADO',
     notas_basica = [{'nota': 4.5, 'porcentaje': 30}, {'nota': 4.0, 'porcentaje': 35}, {'nota': 4.7, 'porcentaje': 35}] examen1 = None examen2 = None nota_presentacion = 4.4 nota_final = 4.4)
