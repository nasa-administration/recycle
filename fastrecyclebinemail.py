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

#set the email ID where you want to send the email 
To_Email_ID = "darchdekin0505@lsr7.net"

# Other variables

sent = False

while True:
  try:

    # Read the ultrasonic ranger distance

    distance_cm = grovepi.ultrasonicRead(ranger)

    if distance_cm < 10 and not sent:            #Check if the bin is full and the email hasn't been sent already
      # Send Plain Text Email 
      email = Class_eMail()
      email.send_Text_Mail(To_Email_ID, 'Plain Text Mail Subject', 'This is sample plain test email body.')
      del email

      sent = True
      print "Email sent"
    elif distance_cm < 10 and sent:
      print "Email not sent"
    else:
      print "Email not sent"
      sent = False
      
    time.sleep(1.0)      # 1 second delay

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

