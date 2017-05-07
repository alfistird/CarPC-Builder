#!/usr/bin/python

import lcddriver
from time import *
 
lcd = lcddriver.lcd()
lcd.lcd_clear()
lcd.lcd_display_string("                ", 1)
lcd.lcd_display_string("                ", 2)

