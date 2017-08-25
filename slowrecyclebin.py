############################################################
# Simple Python program that repeatedly reads the Grove
# Ultrasonic Ranger connected to GrovePi port D4, which is suspended
# above a recycle bin, and writes to Pi Land whether the bin
# needs to be emptied, updating after 30 seconds.
#
# Edited from:
# Simple Python program that repeatedly reads the Grove
# Ultrasonic Ranger connected to GrovePi port D4 and
# writes the current value to Pi Land. 
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-ultrasonic-piland.py
#
############################################################

import time
import requests
import grovepi
import sys

# Write the value to a specific data slot in a Pi Land room

# NOTE:  Change the room, dataslot, and devicename below to something
#        different for your own use so that everyone isn't using
#        the same data slot and overwriting each other's data.

# Pi Land settings
room = 111                             # Room number to use (1 through 999)
slot = 1                              # Data slot number to use (1 through 30)
name = "Main+Office"                      # Descriptive name for your device, put '+' for space char

# Sensor settings
ranger = 4                             # Ultrasonic Ranger is connected to port D4

# Other global variables
baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/write/" + str(slot) + "?name=" + name + "&value="

timer = 30    # How long to wait after the bin has been full to update the status, in seconds
pickup_timer = 0
delay = 2

while True:
  
  try:

    # Read the ultrasonic ranger distance

    distance_cm = grovepi.ultrasonicRead(ranger)


    if distance_cm < 30:            #Check if the bin is full
      pickup_timer += 1             #Add to timer
      
      if pickup_timer >= timer/delay:         #Check that the bin has been full for (timer) amount of seconds
        url = baseurl + "Needs+to+be+emptied"
      else:
        url = baseurl + "Not+full"
        
    else:
      pickup_timer = 0
      url = baseurl + "Not+full"

    print url
    requests.get(url)
    

    time.sleep(delay)      # 1 second delay

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

