##Dirdoc.py

Es una app realiza en **python** que obtiene los principales (hasta el momento) datos de la página postulacion.utem.cl, como usuario **estudiante**
Lo que realiza es un pequeño parser de html a un texto para manipular por medio de una un app. La idea es final es crear un API, en el cual se puedan
realizar algunas peticiones básicas.

Para utilizar dirdoc.py
=======================

se debe crear un Objecto de Dirdoc, enviando las credenciales del usuario
>import dirdoc
>m = dirdoc.Dirdoc(rut='TURUT',password='TUPASSWORD')

Comenzara a correr un logger que indica que ifnormacion de esta obteniendo por ejemplo mi caso es:
>m = dirdoc.Dirdoc(rut=rut,password=password)

Si todo sale correcto, se pueden acceder a los datos que obtuvo el parse, que son:
- info
- carreras
- resultados
- ramos_actual
- ramos_anterior
- rut


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
>print m.ramos_anterior
>[ramo = COMUNICACIÓN DE DATOS , nota_final = 4.7, ramo = DESEMPEÑO DE SISTEMAS COMPUTACIONALES , nota_final = 5.4, ramo = GESTIÓN DE PERSONAL INFORMÁTICO , nota_final = 5.4, ramo = GESTIÓN INFORMÁTICA , nota_final = 5.6, ramo = GESTIÓN MEDIO AMBIENTAL , nota_final = 5.3, ramo = TALLER DE SISTEMAS DE INFORMACIÓN , nota_final = 6.2]
>r = m.ramo
>m.ramos_actual    m.ramos_anterior
>In [24]: r = m.ramos_anterior[0]
>In [25]: r.seccion
>Out[25]: 30411
