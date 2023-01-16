from otree.api import *
import random
import itertools


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
    INSTRUCTIONS_TEMPLATE = 'app_v1/instructions.html'
    # Initial amount allocated to the dictator
    ENDOWMENT = cu(100)



class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField(initial='C')
    player_role = models.StringField(initial='dictator')

    donation = models.CurrencyField(
        doc="""Amount dictator decided to give""",
        min=0,
        max=C.ENDOWMENT,
        label="Decido donar al recipiente",
    )


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
           
def set_payoffs(group: Group):
    for player in group.get_players():
        if player.player_role == "dictator": dictator=player
        if player.player_role == "recipient": recipient=player
    dictator.payoff = C.ENDOWMENT - dictator.donation
    recipient.payoff = dictator.donation


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

class Donation(Page):
    form_model = 'player'
    form_fields = ['donation']

class TestPage(Page):
    pass

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    pass

page_sequence = [WaitAssign, 
        # TestPage,
        ExposureControl, ExposureT1, ExposureT2,
        Donation,
        ResultsWaitPage, Results]
