#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from hermes_python.hermes import Hermes
import random

responses = ['hat heute sehr gute laune',
             'ist heute gut drauf',
             'will fliegen heute',
             'is ganz schön rollig',
             'ist geladen wie eine knallerbse']

unavailable = ['diese person ist als geheim eingestuft',
               'hier ist was schief gelaufen',
               'kein kommentar']


def action_wrapper(hermes, intent_message):
    result_sentence = "watt datt watt"

    current_session_id = intent_message.session_id
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("toby2018:getHowAreYou", action_wrapper).start()