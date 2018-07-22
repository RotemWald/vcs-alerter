#!/bin/bash

ps axf | grep python3 | grep -v grep | awk '{print "kill " $1}' | sh