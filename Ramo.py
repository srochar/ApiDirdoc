__author__ = 'srocha'


class Ramo:
    def __init__(self,diccionario):
        for k,v in diccionario.items():
            setattr(self,k,v)

    def __str__(self):
        return str(
            self.__dict__
        )

    def __repr__(self):

        return str(
            "ramo = {0} , nota_final = {1}".format(self.nombre,self.nota_final)
        )
