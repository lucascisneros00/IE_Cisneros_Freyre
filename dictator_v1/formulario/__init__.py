from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'formulario'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sexo = models.StringField(
        label="Seleccione su género",
        choices=["Hombre", "Mujer", "Otro", "Prefiero no decir"]
    )
    edad = models.IntegerField(label="Introduzca su edad")
    carrera = models.StringField(
        label="Seleccione su carrera",
        choices=["Administración", "Contabilidad", "Derecho", "Economía", "Finanzas", "Ingenieria de la Información", "Ingeniería Empresarial", "Marketing", "Negocios Internacionales"]
    )
    ciclo = models.IntegerField(label="Introduzca en qué ciclo se encuentra (número)")
    distrito_de_residencia = models.StringField(label="Introduzca su distrito de residencia")
    pass


# PAGES
class Formulario(Page):
    form_model = "player"
    form_fields = ["sexo", "edad", "carrera", "ciclo", "distrito_de_residencia"]
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Formulario]
