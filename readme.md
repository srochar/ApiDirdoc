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
    2014-12-21 02:35:34,865 - Dirdoc API - INFO - Post URL = http://postulacion.utem.cl/valida.php
    2014-12-21 02:35:34,967 - Dirdoc API - INFO - Autentificacion Correcta
    2014-12-21 02:35:34,967 - Dirdoc API - INFO - Obteniendo informacion
    2014-12-21 02:35:34,967 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/inscripcion/horario
    2014-12-21 02:35:35,248 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/inscripcion/resultado
    2014-12-21 02:35:35,512 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas_anterior
    2014-12-21 02:35:35,799 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/alumnos/acta.php
    2014-12-21 02:35:35,901 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/alumnos/notas.php
    2014-12-21 02:35:36,005 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular
    2014-12-21 02:35:36,206 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/114736
    2014-12-21 02:35:36,483 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/114737
    2014-12-21 02:35:36,773 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/114739
    2014-12-21 02:35:37,039 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/114741
    2014-12-21 02:35:37,326 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/114598
    2014-12-21 02:35:37,601 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/115431
    2014-12-21 02:35:37,877 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/117117
    2014-12-21 02:35:38,159 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/116603
    2014-12-21 02:35:38,457 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/116605
    2014-12-21 02:35:38,729 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/116949
    2014-12-21 02:35:39,006 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/notas/117227
    2014-12-21 02:35:39,301 - Dirdoc API - INFO - Get URL = http://postulacion.utem.cl/curricular/avance?p2=21&p3=3&p4=113&p6=0
    2014-12-21 02:35:40,122 - Dirdoc API - INFO - Post URL = http://postulacion.utem.cl/alumnos/desconexion.php


Si todo sale correcto, se pueden acceder a los datos que obtuvo el parse, que son:
- info
- carreras
- resultados
- ramos_actual
- ramos_anterior
- rut

Por lo que si usuamos el objeto de Dirdoc:
    

    m.rut
    Out[14]: nombre = SEBASTIAN IGNAC  ROCHA REYES , rut = 17.958.150-7
    m.carreras
    Out[15]: [carrera = 21030 INGENIERÍA EN INFORMÁTICA , estado = Transitorio]
    In [16]: m.resultado
    Out[16]:
    [asignatura: EFE: INTELIGENCIA ARTIFICIAL estado: Aceptado,
     asignatura: EFE: LOGICA DIFUSA estado: Aceptado,
     asignatura: AUDITORÍA DE SISTEMAS estado: Aceptado,
     asignatura: AUDITORÍA DE SISTEMAS estado: Cambia Sección p/memo Escuela,
     asignatura: TRABAJO DE TITULACIÓN I estado: Cambia Sección p/memo Escuela,
     asignatura: TRABAJO DE TITULACIÓN I estado: Aceptado,
     asignatura: TRABAJO DE TITULACIÓN II estado: Curso Rechazado por Requisitos,
     asignatura: PRACTICA PROFESIONAL estado: Aceptado]

También:

    print m.ramos_anterior
    [ramo = COMUNICACIÓN DE DATOS , nota_final = 4.7, ramo = DESEMPEÑO DE SISTEMAS COMPUTACIONALES , nota_final = 5.4, ramo = GESTIÓN DE PERSONAL INFORMÁTICO , nota_final = 5.4, ramo = GESTIÓN INFORMÁTICA , nota_final = 5.6, ramo = GESTIÓN MEDIO AMBIENTAL , nota_final = 5.3, ramo = TALLER DE SISTEMAS DE INFORMACIÓN , nota_final = 6.2]
    In [24]: r = m.ramos_anterior[0]
    In [25]: r.seccion
    Out[25]: 30411
