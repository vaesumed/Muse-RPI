#!/usr/bin/env python

"Raspberry Pi Radio"

import RPi.GPIO as GPIO

import os
import subprocess

from time import sleep

# this file is run using this command: "sudo python radio.py"
# python must be installed, and you must call the command while
# you are in the same folder as the file

# Raspberry Pi Wifi Internet Radio Player
# http://contractorwolf.wordpress.com/raspberry-pi-radio/

__author__ = u'David Muse'
__date__ = u'2014-04-17'
__version__ = u'0.0.1'

def main():
    """@brief Main"""
    
    # set up the pins

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.IN)
    GPIO.setup(24,GPIO.IN)

    # setup variables

    count = 0 

    up = False
    down = False

    print "Raspberry Pi Radio V1"

    # make sure the audio card is started, as well as MPD
    os.system("sudo modprobe snd_bcm2835")

    os.system("sudo mpd")

    os.system("sudo mpc clear")

    os.system("sudo mpc load mine")

    # "mine" is a playlist that has been created prior to starting this
    # to save a playlist just create a playlist and call "sudo mpc save mine" to save 

    #gets the playlist to count ans set the length of the list

    cmd = subprocess.Popen("sudo mpc playlist",shell=True, stdout=subprocess.PIPE)

    stations = cmd.stdout.readlines()

    channelCount = len(stations)

    # iterates through the playlist in order to get the names (instead of the URLs)
    os.system("sudo mpc volume 0")

    index = 1

    while(index<channelCount):

        os.system("sudo mpc play " + str(index))

        index = index + 1

        sleep(.75)


    os.system("sudo mpc volume 100")

    print "stations loaded: " + str(channelCount)

    # I prefer NPR to be the starting station, you can set it to be whatever you want, not needed
    if(channelCount>0):

        os.system("sudo mpc play 5")

        currentChannel = 5




    # main loop, looking for button presses
    # this looks more complicated because the loop will me fast, this way 
    # when you press the buttons it only move one station until you release the button

    while(True):

        if(down==True):

            if(GPIO.input(23)==False):

                #print "BUTTON UP PRESSED, SWITCHING TO: "

                if(currentChannel<channelCount):

                    currentChannel = currentChannel + 1

                else:

                    currentChannel = 1          



                cmd = subprocess.Popen("sudo mpc play " + str(currentChannel),shell=True, stdout=subprocess.PIPE)

                print str(currentChannel) + ": " + cmd.stdout.readline()

        down = GPIO.input(23)




        if(up==True):

            if(GPIO.input(24)==False):

                #print "BUTTON DOWN PRESSED, SWITCHING TO: "

                if(currentChannel>1):

                    currentChannel = currentChannel - 1

                else:

                    currentChannel = channelCount           



                cmd = subprocess.Popen("sudo mpc play " + str(currentChannel),shell=True, stdout=subprocess.PIPE)

                print str(currentChannel) + ": " + cmd.stdout.readline()


        up = GPIO.input(24)





        count = count +1



        sleep(.1)




    # this is never hit, but should be here to indicate if you plan on leaving the main loop
    print "done"
    


    
if __name__ == "__main__":
    main()    