__author__ = 'srocha'


class Nota():
    def __init__(self,diccionario):
        for k,v in diccionario.items():
            setattr(self,k,v)

    def __str__(self):
        return str(
            self.__dict__
        )

    def __repr__(self):
        return str(
            dict(
                nota = self.nota,
                porcentaje = self.porcentaje
            )
        )
class NotaEstable():
    def __init__(self,nota):
        self.nota  = nota

    def __str__(self):
        return str(
            self.__dict__
        )

    def __repr__(self):
        return str(
            dict(
                nota = self.nota,
                estado = self.estado
            )
        )

class NotasParciales():
    def __init__(self,basicas,nota_presentacion,examen1,examen2,nota_final):
        self.basicas = basicas
        self.examen1 = examen1
        self.examen2 = examen2
        self.nota_presentacion = nota_presentacion
        self.nota_final = nota_final

    def __str__(self):
        return str(
            self.__dict__
        )

    def __repr__(self):
        return str(
            "notas_basica = {0} "
            "examen1 = {1} "
            "examen2 = {2} "
            "nota_presentacion = {3} "
            "nota_final = {4}".format(self.basicas,self.examen1,self.examen2,self.nota_presentacion,self.nota_final)
        )