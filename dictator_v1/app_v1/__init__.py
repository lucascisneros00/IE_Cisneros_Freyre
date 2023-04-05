from otree.api import *
import random
import itertools
import time
import random

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
        choices=["Administración", "Contabilidad", "Derecho", "Economía", "Finanzas", "Ingenieria de la Información", "Ingeniería Empresarial", "Marketing", "Negocios Internacionales", "Otra"]
    )
    ciclo = models.StringField(
        label="Selecciona el ciclo en el que estás",
        choices=["1","2","3","4","5","6","7","8","9","10","11","12"]
    )
    distrito_de_residencia = models.StringField(
        label="Selecciona tu zona de residencia",
        choices=["Zona 1 (Puente Piedra, Comas, Carabayllo)",
                 "Zona 2 (Independencia, Los Olivos, San Martín de Porres)",
                 "Zona 3 (San Juan de Lurigancho)",
                 "Zona 4 (Cercado, Rímac, Breña, La Victoria)",
                 "Zona 5 (Ate, Chaclacayo, Lurigancho, Santa Anita, San Luis, El Agustino)",
                 "Zona 6 (Jesús María, Lince, Pueblo Libre, Magdalena, San Miguel)",
                 "Zona 7 (Miraflores, San Isidro, San Borja, Surco, La Molina)",
                 "Zona 8 (Surquillo, Barranco, Chorrillos, San Juan de Miraflores)",
                 "Zona 9 (Villa El Salvador, Villa María del Triunfo, Lurín, Pachacamác)",
                 "Zona 10 (Callao, Bellavista, La Perla, La Punta, Carmen de la Legua, Ventanilla",
                 "Otros"])


    treatment = models.StringField(initial='C')
    player_role = models.StringField(initial='dictator')

    donation = models.IntegerField(
        min=0, max=C.ENDOWMENT, label=""
    )

    dictator_donation = models.CurrencyField(min=0,
        max=C.ENDOWMENT,)
    recipient_donation = models.CurrencyField(min=0,
        max=C.ENDOWMENT,)
    
    order_number = models.IntegerField()
    random_code = models.IntegerField()

# FUNCTIONS
def creating_session(subsession: Subsession): 

    # Shuffle players
    players = list(subsession.get_players())
    random.shuffle(players)

    # Give each player an ID
    for i, p in enumerate(players, start=1):
        p.order_number = i
        p.random_code = random.randint(1,1000)

    # Shuffle again
    random.shuffle(players)

    # Give players shuffled IDs
    for i, p in enumerate(players, start=1):
        # Assign players to control, t1, t2 groups
        p.order_number_reshuffled = i
        if p.order_number_reshuffled<len(players)*1/3:
            p.treatment = 'C' 
        elif p.order_number_reshuffled<len(players)*2/3:
            p.treatment = 'T1' 
        else:
            p.treatment = 'T2' 
        
           
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


# PAGES (test)
class WaitAssign(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():    
            if player.id_in_group==1: player.player_role = 'dictator'
            if player.id_in_group==2: player.player_role = 'recipient'

class TestPage(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(endowment=C.ENDOWMENT)

class TestPage2(Page):
    pass

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


## PAGES 
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
    @staticmethod
    def vars_for_template(player):

        player_payoff = player.payoff
        player_donation =  player.donation 
        return dict(
            player_payoff=player_payoff,
            player_donation=player_donation,
            player_finalpayoff = player_payoff+8,
        )
     
page_sequence = [
        # TestPage,TestPage2, 
        WaitAssign,
        _0_Formulario,
        _1_Instrucciones_1, _2_Instrucciones_2,
        _3_Exposure_0,
        _4_ExposureControl, _5_ExposureT1, _6_ExposureT2, 
        _7_Decision_C_T1,  _8_Decision_T2,
        ResultsWaitPage,
        _9_Resultados,
        _10_Informacion_Final]
