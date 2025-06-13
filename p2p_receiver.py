from sys import exit
from time import time
from rak811.rak811_v3 import Rak811

#base time to wait for messege before timing out
BASE_WAIT_TIME = 10

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

print("receive loop")
counter = 0
try:
    while True:      #i want to change this to leave when i tell it to, instead of manually shutting it off every time
        timeout_time = time() + BASE_WAIT_TIME
    #setting the module to receive messeges
        lora.set_config("lorap2p:transfer_mode:1")

        while (time() + 1) < timeout_time:
            wait_time = timeout_time - time()
            print('waiting for {} seconds'.format(wait_time))
            lora.receive_p2p(wait_time)
            while lora.nb_downlinks() > 0:
                message = lora.get_downlink()
                messeage_data = message['data']
            ##checking if the first part of the messege is the magic key
                if messeage_data[:len(MAGIC_KEY)] == MAGIC_KEY:
                    print('received messege: {}'.format(messeage_data.decode('utf-8')))
                    print('RSSI: {}, SNR: {}'.format(message['rssi'], message['snr']))
                else:
                    print('Foreign messege detected')
except:
    pass

print("\nAll done!")
exit(0)

