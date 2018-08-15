"""
This module is main module for server application which contains Flask application and routes.
"""
from flask import Flask
from flask import request
from time import sleep

import _thread
import threading
from threading import Thread

# RPI_DROID_COMMDAND is shared variable between threads to save command from user
# 1 - go ahead
# 2 - go ahead to the left
# 3 - go ahead to the right
# 4 - bo back
# 5 - go left back
# 6 - go left right
# 7 - enable auto mode
# 8 - disable auto mode
# 0 - stop
RPI_DROID_COMMAND = -1
lock = threading.Lock()



def FlaskApplication():
    app = Flask(__name__)

    @app.route('/',methods=['POST'])
    def index():
        data = request.data
        req_data = request.get_json()
        message_type = req_data['message_type']
        value = req_data['value']
        str_msg_type = str(message_type)
        #print("Dobijeno u zahtevu:"+str_msg_type+"  "+value)

        global RPI_DROID_COMMAND
        global lock

        LOCAL_RPI_DROID_COMMAND = RPI_DROID_COMMAND

        lock.acquire()
        try:
            if str_msg_type.find("RPi_MSG_DIRECTION") != -1:
                if value.find("stand") != -1:
                    print("KOMANDA ZA KRETANJE: STANI")
                    RPI_DROID_COMMAND = 0
                elif value.find("go_ahead") != -1:
                    RPI_DROID_COMMAND = 1
                    print("KOMANDA ZA KRETANJE: NAPRED")
                elif value.find("go_back") != -1:
                    RPI_DROID_COMMAND = 4
                    print("KOMANDA ZA KRETANJE: NAZAD")
                elif value.find("go_left") != -1:
                    RPI_DROID_COMMAND = 2
                    print("KOMANDA ZA KRETANJE: NAPRED U LEVO")
                elif value.find("go_right") != -1:
                    RPI_DROID_COMMAND = 3
                    print("KOMANDA ZA KRETANJE: NAPRED U DESNO")
                elif value.find("go_b_left") != -1:
                    RPI_DROID_COMMAND = 5
                    print("KOMANDA ZA KRETANJE: NAZAD U LEVO")
                elif value.find("go_b_right") != -1:
                    RPI_DROID_COMMAND = 6
                    print("KOMANDA ZA KRETANJE: NAZAD U DESNO")
            
            elif str_msg_type.find("RPi_MSG_CONNECTING") != -1:
                RPI_DROID_COMMAND = 0
                print("Uspostavljanje veze")

            elif str_msg_type.find("RPi_MSG_DISCONNECTING") != -1:
                RPI_DROID_COMMAND = 0
                print("Prekidanje veze")

            elif str_msg_type.find("RPi_MSG_AUTO_MODE") != -1:
                if value.find("enable_auto_mode") != -1:
                    RPI_DROID_COMMAND = 7
                    print("Enable auto mode")
                elif value.find("disable_auto_mode") != -1:
                    RPI_DROID_COMMAND = 8
                    print("Disable auto mode")
                elif value.find("target_coordinate") != -1:
                    RPI_DROID_COMMAND = 9
                    print("Target coordinate")
            
            #print("-----------------------------------SET RPI_DROID_COMMAND: ", RPI_DROID_COMMAND)
        finally:
            lock.release()


        if(message_type == 1):
            return "connected"
        else:
            return 'Hello, i am RPiDroid robot, can i help you? :)'+str(message_type)+" "+value+'toeto'


    try:
        app.run(debug=False, use_reloader=False, threaded=True, host='0.0.0.0')    
    except Exception:
        print("Pokretanje flask aplikacije za komunikaciju neuspesno")


def ControlGPIO():

    while True:
        global lock

        x = -2

        lock.acquire()
        try:
            print("-----------------------------------READ RPI_DROID_COMMAND: ", RPI_DROID_COMMAND)
            x = RPI_DROID_COMMAND            
        finally:
            lock.release()
        
        print("DEBUG_N ",x)


#        if x == 0: #stani
#        
#        elif x == 1: #napred
# 
#        elif x == 2: #levo
#
#        elif x == 3: #desno
#
#        elif x == 4: #nazad
#
#        elif x == 5: #nazad u levo
#
#        elif x == 6: #nazad u desno
#
#        elif x == 7: #ukljucio auto mod
#
#        elif x == 8: #iskljuci auto mod
#
#        elif x == 9: #postavi ciljne koordinate




        sleep(1) #in seconds        

if __name__ == '__main__':
    #Because we use 0.0.0.0 in app.run command the web server is accessible to any device on the same network, including other computers, tablets, and smartphones
    print("pokrenuta aplikacija") 
    #_thread.start_new_thread(ControlGPIO,())
    #tid = _thread.start_new_thread(FlaskApplication, ())
    t1 = Thread(target=ControlGPIO, args=())
    t1.start()
    #t1.join()

    #t = Thread(target=FlaskApplication, args=())
    #t.start()
    #t.join()
    FlaskApplication()

    #t1.join()
