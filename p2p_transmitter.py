from sys import exit
from time import time
from rak811.rak811_v3 import Rak811

#base time to wait to send a message
BASE_WAIT_TIME = 5

#maigc key to recognise our messege
MAGIC_KEY = b'\xca\xfe'

lora = Rak811()

print("setup: ")

#conifuring it to work in p2p mode
response = lora.set_config("lora:work_mode:1")
for r in response:
    print(r)

#setting up the normal connection 
freq = 869.800 #frequency
sf = 7  # spread factor
bw = 0  # 125KHz
ci = 1  # 4/5
pre = 8  #preamble length
pwr = 16 # power in Dbm
lora.set_config(f'lorap2p:{int(freq*1000*1000)}:{sf}:{bw}:{ci}:{pre}:{pwr}')

print("entering send loop")
counter = 0
while True:
    counter += 1
    print("sending messege: counter {}".format(counter))
    msg = "count {}".format(counter)
    messege_to_send = MAGIC_KEY + msg.encode('utf-8')
    lora.set_config('lorap2p:transfer_mode:2')
    lora.send_p2p(messege_to_send)


    