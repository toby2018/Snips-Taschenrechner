#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from hermes_python.hermes import Hermes
from matrix_lite import led
import random

responses = [' hat heute sehr gute laune',
             ' ist heute gut drauf',
             ' will fliegen heute',
             ' is ganz schön rollig',
             ' ist geladen wie eine knallerbse',
             ' braucht urlaub!',
             ' will heute raus hier!']

unavailable = ['diese person ist als geheim eingestuft',
               'hier ist was schief gelaufen',
               'kein kommentar']


def action_wrapper(hermes, intent_message):
    # Sets each LED to blue
    led.set('blue')  # color name

    item = intent_message.slots.family_member.first().value

    if item == 'Sabine' or item == 'Steffen':
        result_sentence = item + random.choice(responses)
        # result_sentence = 'watt dat watt?'
    else:
        result_sentence = random.choice(unavailable)
        # result_sentence = 'keiner will die else'

    current_session_id = intent_message.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

    # Turns off each LED
    led.set('black')  # color name


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("toby2018:getHowAreYou", action_wrapper).start()
