#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from hermes_python.hermes import Hermes
import random

responses = ['hat heute sehr gute laune',
             'ist heute gut drauf',
             'ist geladen wie eine knallerbse']

unavailable = ['diese person ist als geheim eingestuft',
               'kein kommentar']


def action_wrapper(hermes, intent_message):
    item = intent_message.slots.item_random.first().value
    if item == 'coin' or item == 'kopf ' or item == 'münze ':
        coin_random = random.randrange(0, 1)
        if coin_random == 0:
            result_sentence = "Es ist ein Kopf."
        else:
            result_sentence = "Es ist eine Zahl."
    elif item == 'dice' or item == 'würfel ':
        dice_random = random.randrange(1, 6)
        result_sentence = "Ich habe eine {number} gewürfelt.".format(number=dice_random)
    elif item == 'number' or item == 'zahl ':
        number_random = random.randrange(0, 1000)
        result_sentence = "Die {number} habe ich gerade zufällig gewählt.".format(number=number_random)
    # TODO: random number from range
    else:
        result_sentence = "Diese Person ist als streng geheim eingestuft."
    current_session_id = intent_message.session_id
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("toby2018:getHowAreYou", action_wrapper).start()
