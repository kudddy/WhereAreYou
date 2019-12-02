#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from ext.N2DChecker import MainScript
import argparse

bt = MainScript()




parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-t', type=str, help="token")

args = parser.parse_args()

token = str(args.t)

bt.login(token)

bt.start_pulling()


