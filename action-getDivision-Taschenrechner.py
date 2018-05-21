#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import math

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 

    Refer to the documentation for further details. 
    """ 
    first = int(intentMessage.slots.firstTerm.first().value)
    second = int(intentMessage.slots.secondTerm.first().value)
    if second != 0:
        calc = first / float(second)
        if str(calc)[-2:] == ".0":
            calc = int(calc)
        if "." in str(calc):
            calc_part1, calc_part2 = str(calc).split(".")
            result_sentence = "{0} geteilt durch {1} ergibt {2} komma {3} .".format(first, second,
                                                                                   calc_part1, calc_part2)
        else:
            result_sentence = "{} geteilt durch {} ergibt {} .".format(first, second, calc)
    else:
        result_sentence = "Ich kann leider nicht durch Null teilen."

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("domi:getDivision", subscribe_intent_callback) \
.start()
