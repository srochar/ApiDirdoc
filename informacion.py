__author__ = 'srocha'

class Informacion():
    def __init__(self,diccionario):
        for k,v in diccionario.items():
            setattr(self,k,v)

    def __str__(self):
        return str(
            self.__dict__
        )

    def __repr__(self):
        return str(
            "nombre = {0} , rut = {1}".format(self.nombre,self.rut)
        )