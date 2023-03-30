from otree.api import *
import random
import itertools
import time

doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    # Initial amount allocated to the dictator
    ENDOWMENT = cu(20)



class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    sexo = models.StringField(
        label="Selecciona tu género",
        choices=["Hombre", "Mujer", "Otro", "Prefiero no decir"]
    )
    edad = models.IntegerField(label="Introduce tu edad")
    carrera = models.StringField(
        label="Selecciona tu carrera",
        choices=["Administración", "Contabilidad", "Derecho", "Economía", "Finanzas", "Ingenieria de la Información", "Ingeniería Empresarial", "Marketing", "Negocios Internacionales"]
    )
    ciclo = models.IntegerField(label="Introduce en qué ciclo te encuentras (número)")
    distrito_de_residencia = models.StringField(label="Introduce tu distrito de residencia")


    treatment = models.StringField(initial='C')
    player_role = models.StringField(initial='dictator')

    donation = models.CurrencyField(
        doc="""Amount dictator decided to give""",
        min=0,
        max=C.ENDOWMENT,
        label="",
    )
    dictator_donation = models.CurrencyField(min=0,
        max=C.ENDOWMENT,)
    recipient_donation = models.CurrencyField(min=0,
        max=C.ENDOWMENT,)
    
    order_number = models.IntegerField()
    random_code = models.IntegerField()

# FUNCTIONS
def creating_session(subsession: Subsession):
    # Assign players to control, t1, t2 groups
    for i, player in enumerate(subsession.get_players()):
        if i<len(subsession.get_players())*1/3:
            player.treatment = 'C' #f't{i}_{player}'
        elif i<len(subsession.get_players())*2/3:
            player.treatment = 'T1' #f't{i}_{player}'
        else:
            player.treatment = 'T2' #f't{i}_{player}'
    
    # Generate unique ID
    for i, p in enumerate(subsession.get_players(), start=1):
        p.order_number = i
        p.random_code = random.randint(1,1000)
           
def set_payoffs(group: Group):
    for player in group.get_players():
        if player.player_role == "dictator": dictator=player
        if player.player_role == "recipient": recipient=player
    dictator.payoff = C.ENDOWMENT - dictator.donation
    recipient.payoff = dictator.donation

    dictator.dictator_donation = dictator.donation
    dictator.recipient_donation = recipient.donation 
    recipient.dictator_donation = dictator.donation
    recipient.recipient_donation = recipient.donation 


# PAGES
class WaitAssign(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():    
            if player.id_in_group==1: player.player_role = 'dictator'
            if player.id_in_group==2: player.player_role = 'recipient'

class ExposureControl(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'C'

class ExposureT1(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'T1'

class ExposureT2(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'T2'

class Decision(Page):
    form_model = 'player'
    form_fields = ['donation']

class Instructions(Page):
    pass

class TestPage(Page):
    pass

class TestPage2(Page):
    pass

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    pass

class _0_Formulario(Page):
    form_model = "player"
    form_fields = ["sexo", "edad", "carrera", "ciclo", "distrito_de_residencia"]

class _1_Instrucciones_1(Page):
    pass
class _2_Instrucciones_2(Page):
    pass
class _3_Exposure_0(Page):
    pass
class _4_ExposureControl(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'C'
    
class _5_ExposureT1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'T1'

class _6_ExposureT2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'T2'
    
class _7_Decision_C_T1(Page):
    form_model = 'player'
    form_fields = ['donation']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment in ['C','T1']
class _8_Decision_T2(Page):
    form_model = 'player'
    form_fields = ['donation']

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'T2'
    
class _9_Resultados(Page):
    @staticmethod
    def vars_for_template(player):
        dictator_donation = player.dictator_donation
        recipient_donation = player.recipient_donation

        player_payoff = player.payoff
        player_donation =  player.donation 
        return dict(
            player_payoff=player_payoff,
            player_donation=player_donation,
            player_finalpayoff = player_payoff+8,

            dictator_donation = dictator_donation,
            recipient_donation = recipient_donation
        )
class _10_Informacion_Final(Page):
    pass 
page_sequence = [
        #TestPage,TestPage2, 
        WaitAssign,
        _0_Formulario,
        _1_Instrucciones_1, _2_Instrucciones_2,
        _3_Exposure_0,
        _4_ExposureControl, _5_ExposureT1, _6_ExposureT2, 
        _7_Decision_C_T1,  _8_Decision_T2,
        ResultsWaitPage,
        _9_Resultados,
        _10_Informacion_Final]
