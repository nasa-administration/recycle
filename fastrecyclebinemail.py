############################################################
# Simple Python program that repeatedly reads the Grove
# Ultrasonic Ranger connected to GrovePi port D4, which is suspended
# above a recycle bin, and writes to Pi Land whether the bin
# needs to be emptied, updating immediately.
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
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Email settings
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("lshsrecycling@gmail.com", "pickuppi")
 
msg = "YOUR MESSAGE!"
server.sendmail("lshsrecycling@gmail.com", "blaizingfireXD@gmail.com", msg)
server.quit()

# Write the value to a specific data slot in a Pi Land room

# Pi Land settings

room = 111                             # Pi land room number
slot = 1                              # Data slot number to use (1 through 30)
name = "Main+Office"                      # Room name

# Sensor settings
ranger = 4                             # Ultrasonic Ranger is connected to port D4

# Other global variables
baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/write/" + str(slot) + "?name=" + name + "&value="


while True:

  try:

    # Read the ultrasonic ranger distance

    distance_cm = grovepi.ultrasonicRead(ranger)

    if distance_cm < 10:            #Check if the bin is full
      url = baseurl + "Needs+to+be+emptied"
    else:
      url = baseurl + "Not+full"

    print url                       #Write data
    requests.get(url)

    time.sleep(1.0)      # 1 second delay

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

