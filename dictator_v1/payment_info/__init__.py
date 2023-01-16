from otree.api import *
import datetime


doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""
## OTHER FUNCTIONS
def get_completion_code():
    # Get the current date and time
    now = datetime.datetime.now()
    # Get the date for the beginning of the year
    year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    # Calculate the difference between the two dates
    time_delta = now - year_start
    # Convert the difference to minutes and print the result
    time_delta_in_minutes = time_delta.days
    # Get the completion code
    completion_code = time_delta_in_minutes # hash(time_delta_in_minutes)%1000+1
    return str(completion_code)



class C(BaseConstants):
    NAME_IN_URL = 'payment_info'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    completion_code =  get_completion_code()

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS
# PAGES
class PaymentInfo(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(redemption_code=participant.label or participant.code)


page_sequence = [PaymentInfo]
