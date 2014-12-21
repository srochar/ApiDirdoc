__author__ = 'srocha'

class Carrera:
    def __init__(self,diccionario):
        for k,v in diccionario.items():
            setattr(self,k,v)

    def __str__(self):
        return str(
            self.__dict__
        )

    def __repr__(self):
        return str(
            "carrera = {0} , estado = {1}".format(self.carrera,self.estado)
        )