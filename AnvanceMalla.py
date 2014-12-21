__author__ = 'srocha'

class AvanceMalla():
    def __init__(self,diccionario):
        for k,v in diccionario.items():
            setattr(self,k,v)

    def __str__(self):
        return str(
            self.__dict__
        )

    def __repr__(self):
        return str(
            "asignatura = {0} , nota = {1}".format(self.asignatura,self.nota)
        )
