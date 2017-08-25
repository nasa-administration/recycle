############################################################
# Simple Python program that repeatedly reads the Grove
# Ultrasonic Ranger connected to GrovePi port D4, which is suspended
# above a recycle bin, and sends an email if there is something
# 10 cm away from it.
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

from email_handler import Class_eMail

# Sensor settings
ranger = 4                             # Ultrasonic Ranger is connected to port D4

# Pi Land settings
room = 111                             # Pi land room number
slot = 1                              # Data slot number to use (1 through 30)
name = "Main+Office"                      # Room name

#set the email ID where you want to send the email 
To_Email_ID = "darchdekin0505@lsr7.net"

# Other variables

timer = 10            # How long to wait before sending the email
delay = 2             # How long to wait between checking the sensor
pickup_distance = 10

sent = False
pickup_timer = 0

baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/write/" + str(slot) + "?name=" + name + "&value="

while True:
  try:

    # Read the ultrasonic ranger distance

    distance_cm = grovepi.ultrasonicRead(ranger)

    if distance_cm < 10 and not sent:            #Check if the bin is full and the email hasn't been sent already
      if pickup_timer * delay < (timer - delay):
        pickup_timer += 1
        print("Sensor has been obstructed for %d seconds" % (pickup_timer * delay))
      else:
        # Send Plain Text Email 
        email = Class_eMail()
        email.send_Text_Mail(To_Email_ID, 'Plain Text Mail Subject', 'This is sample plain test email body.')
        del email

        sent = True
        pickup_timer = 0
        print "Email sent"

        url = baseurl + "Needs+to+be+emptied"

    elif distance_cm < 10 and sent:
      print "Email not sent"
    else:
      print "Email not sent"
      sent = False
      pickup_timer = 0

      url = baseurl + "Not+full"

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

