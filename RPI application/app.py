# pscp app.py pi@192.168.2.12:/home/pi
import _thread
import threading
import collections
import RPi.GPIO as GPIO
import random
from flask import Flask
from flask import request
from time import sleep
from threading import Thread
from enum import Enum
import json

# Tipovi poruka koje se razmenjuju
class RPi_MSG_TYPE(Enum):
    RPi_MSG_INVALID = (-1),
    RPi_MSG_DIRECTION = 0,
    RPi_MSG_CONNECTING = 1,
    RPi_MSG_DISCONNECTING = 2,
    RPi_MSG_AUTO_MODE = 3,
    RPi_MSG_RESPONSE_OK = 4,
    RPi_MSG_RESPONSE_FAILURE = 5,
    RPi_MSG_RESPONSE_OBSTRACLE = 6,
    RPi_MSG_UNDEFINED = 7

# Moguci pravci kretanja
class RPi_DIRECTION(Enum):
    RPi_INVALID = (-1),
    RPi_STAND = 0,
    RPi_GO_AHEAD = 1,
    RPi_GO_AHEAD_SEMI_LEFT = 2,
    RPi_GO_AHEAD_SEMI_RIGHT = 3,
    RPi_GO_LEFT = 4,
    RPi_GO_RIGHT = 5,
    RPi_GO_BACK = 6,
    RPi_GO_BACK_SEMI_LEFT = 7,
    RPi_GO_BACK_SEMI_RIGHT = 8

# Rezim rada robota
class RPi_AUTO_MODE(Enum):
    RPi_AUTO_MODE_INVALID = (-1),
    RPi_AUTO_MODE_ENABLED = 0,
    RPi_AUTO_MODE_DISABLED = 1

# Moguci odgovori robota
class RPi_RESPONSE_OBSTRACLE(Enum):
    RPi_RESPONSE_INVALID = (-1),
    RPi_RESPONSE_OK = 0,
    RPi_FAILURE = 1,
    RPI_OBSTRACLE_DETECTED = 2,
    RPI_OBSTRACLE_PASSED = 3

# Moguce strane obilaska prepreke
class RPi_SIDE(Enum):
    RPi_SIDE_INVALID = (-1),
    RPi_SIDE_LEFT = 0,
    RPi_SIDE_RIGHT = 1,
    RPi_SIDE_CANNOT_DECIDE = 2


# -------------------------MODUL ZA KONTROLU HARDVERA BEGIN--------------------------
def checkSensors():
    # Ocitava distancu do prepreke za svaki senzor
    # sensor 1
    PIN_TRIGGER = 7
    PIN_ECHO = 11

    d_left = -1
    d_ahead = -1
    d_right = -1

    # sensor 2
    PIN_TRIGGER = 13
    PIN_ECHO = 15

    d_left1 = -1
    d_ahead1 = -1
    d_right1 = -1

    # sensor 3
    PIN_TRIGGER = 29
    PIN_ECHO = 31

    d_left2 = -1
    d_ahead2 = -1
    d_right2 = -1


    GPIO.setup(PIN_TRIGGER,GPIO.OUT)
    GPIO.setup(PIN_ECHO,GPIO.IN)
    
    GPIO.setup(PIN_TRIGGER1,GPIO.OUT)
    GPIO.setup(PIN_ECHO1,GPIO.IN)
    
    GPIO.setup(PIN_TRIGGER2,GPIO.OUT)
    GPIO.setup(PIN_ECHO2,GPIO.IN)
    
    GPIO.output(PIN_TRIGGER,GPIO.LOW)
    GPIO.output(PIN_TRIGGER1,GPIO.LOW)
    GPIO.output(PIN_TRIGGER2,GPIO.LOW)
    
    print("Calculate distance")
    
    # ------sensor ----------
    GPIO.output(PIN_TRIGGER,GPIO.HIGH) #signalizira senzoru da emituje signal
    
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER,GPIO.LOW)
    
    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time() # vreme slanja signala
        
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time() # vreme dobijanja odbijenog signala
    
    pulse_duration = pulse_end_time - pulse_end_time
    distance = round ( pulse_duration * 17150, 2)
    d_ahead = distance
    
    # ------sensor 1----------
    GPIO.output(PIN_TRIGGER1,GPIO.HIGH) #signalizira senzoru 1 da emituje signal
    
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER1,GPIO.LOW)
    
    while GPIO.input(PIN_ECHO1)==0:
        pulse_start_time1 = time.time() # vreme slanja signala
        
    while GPIO.input(PIN_ECHO1)==1:
        pulse_end_time1 = time.time() # vreme dobijanja odbijenog signala
    
    pulse_duration1 = pulse_end_time1 - pulse_end_time1
    distance1 = round ( pulse_duration1 * 17150, 2)
    d_left = distance1

    # ------sensor 2----------
    GPIO.output(PIN_TRIGGER2,GPIO.HIGH) #signalizira senzoru 2 da emituje signal
    
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER2,GPIO.LOW)
    
    while GPIO.input(PIN_ECHO2)==0:
        pulse_start_time2 = time.time() # vreme slanja signala
        
    while GPIO.input(PIN_ECHO2)==1:
        pulse_end_time2 = time.time() # vreme dobijanja odbijenog signala
    
    pulse_duration2 = pulse_end_time2 - pulse_end_time2
    distance2 = round ( pulse_duration2 * 17150, 2)
    d_right = distance2 
    
    print(" Razdaljina ahead: " ,distance/2, " cm ", " left: ",distance1/2," cm, right: ",distance2/2, "cm")
    
    return (d_left, d_ahead, d_right)

def checkObstracle():
    d_left, d_ahead, d_right = checkSensors()
    
    if d_ahead < 20:
        return True
    
    return False

def turnLeft5Degrees():
    # Desni motor pinovi
    motor_right_1A = 3 # Pinovi 2 i 3 odredjuju smer okretanja desnog motora
    motor_right_2A = 2
    motor_right_12EN = 4 # Pin za ukljucivanje i iskljucivanje desnog motora

    # Levi motor pinovi
    motor_left_3A = 20 # Pinovi 16 i 20 odredjuju smer okretanja levog motora
    motor_left_4A = 16
    motor_left_34EN = 21 # Pin za ukljucivanje i iskljucivanje levog motora

    # Skrece u levo pod uglom od 5 stepeni
    print("TURN LEFT 5 degrees")
    GPIO.output(motor_right_1A, GPIO.HIGH)
    GPIO.output(motor_right_2A, GPIO.LOW)
    GPIO.output(motor_left_34EN, GPIO.LOW)
    GPIO.output(motor_right_12EN, GPIO.HIGH)
    sleep(0.04)
    GPIO.output(motor_right_12EN, GPIO.LOW)

    return RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK
    
def turnRight5Degrees():
    # Skrece u desno pod uglom od 5 stepeni
    # Desni motor pinovi
    motor_right_1A = 3 # Pinovi 2 i 3 odredjuju smer okretanja desnog motora
    motor_right_2A = 2
    motor_right_12EN = 4 # Pin za ukljucivanje i iskljucivanje desnog motora

    # Levi motor pinovi
    motor_left_3A = 20 # Pinovi 16 i 20 odredjuju smer okretanja levog motora
    motor_left_4A = 16
    motor_left_34EN = 21 # Pin za ukljucivanje i iskljucivanje levog motora

    # Skrece u desno pod uglom od 5 stepeni
    print("TURN RIGHT 5 degrees")
    GPIO.output(motor_left_3A, GPIO.HIGH)
    GPIO.output(motor_left_4A, GPIO.LOW)
    GPIO.output(motor_right_12EN, GPIO.LOW)
    GPIO.output(motor_left_34EN, GPIO.HIGH)
    
    sleep(0.06)
    GPIO.output(motor_left_34EN, GPIO.LOW)
    
    return RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK

def turnLeft10Degrees():
    turnLeft5Degrees()
    turnLeft5Degrees()

    return RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK

def turnRight10Degrees():
    turnRight5Degrees()
    turnRight5Degrees()

    return RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK
    
    
def goAhead():
    # Krece se napred
    print("GO AHEAD")
    GPIO.output(motor_left_3A, GPIO.HIGH)
    GPIO.output(motor_left_4A, GPIO.LOW)
    GPIO.output(motor_right_1A, GPIO.HIGH)
    GPIO.output(motor_right_2A, GPIO.LOW)

    obstracleDetected = False
    
    for i in range(0,10):
        obstracleDetected = checkObstracle()

        if obstracleDetected:
            break

        GPIO.output(motor_left_34EN, GPIO.HIGH)
        GPIO.output(motor_right_12EN, GPIO.HIGH)
        sleep(0.04)
        GPIO.output(motor_left_34EN, GPIO.LOW)
        sleep(0.01)
        GPIO.output(motor_right_12EN, GPIO.LOW)
    
    if obstracleDetected:
        print("Obstracle detected")
        return RPi_RESPONSE_OBSTRACLE.RPI_OBSTRACLE_DETECTED
        
    return RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK
    
def goBack():
    # Krece se nazad
    print("GO BACK")
    GPIO.output(motor_left_3A, GPIO.LOW)
    GPIO.output(motor_left_4A, GPIO.HIGH)
    GPIO.output(motor_right_1A, GPIO.LOW)
    GPIO.output(motor_right_2A, GPIO.HIGH)

    for i in range(0,10):
        GPIO.output(motor_left_34EN, GPIO.HIGH)
        GPIO.output(motor_right_12EN, GPIO.HIGH)
        sleep(0.04)
        GPIO.output(motor_left_34EN, GPIO.LOW)
        sleep(0.01)
        GPIO.output(motor_right_12EN, GPIO.LOW)
        
    return RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK
    
def stand():
    # Iskljucuje motore
    GPIO.output(motor_right_12EN, GPIO.LOW)
    GPIO.output(motor_left_34EN, GPIO.LOW)

    return RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK

def ControlGPIO():
    global lock
    global ContextRPi

    while True:
        print("CONTROL GPIO")

        lock.acquire()
        try:
            # Citanje vrednosti iz Context-a
            msg_type = ContextRPi.RPI_DROID_COMMAND_MSG_TYPE
            direction = ContextRPi.RPI_DROID_DIRECTION
        finally:
            lock.release()
        
        return_value = RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_INVALID

        if msg_type != RPi_DIRECTION.RPi_INVALID:
            if direction == RPi_DIRECTION.RPi_GO_AHEAD_SEMI_LEFT or direction == RPI_DIRECTION.RPi_GO_BACK_SEMI_RIGHT:
                return_value = turnLeft5Degrees()
            elif direction == RPi_DIRECTION.RPi_GO_AHEAD_SEMI_RIGHT or direction == RPI_DIRECTION.RPi_GO_BACK_SEMI_LEFT:
                return_value = turnRight5Degrees()
            elif direction == RPi_DIRECTION.RPi_GO_LEFT:
                return_value = turnLeft5Degrees()
                return_value = turnLeft5Degrees()
                return_value = turnLeft5Degrees()
            elif direction == RPi_DIRECTION.RPi_GO_RIGHT:
                return_value = turnRight5Degrees()
                return_value = turnRight5Degrees()
                return_value = turnRight5Degrees()
            elif direction == RPi_DIRECTION.RPi_GO_AHEAD:
                return_value = goAhead()
            elif direction == RPi_DIRECTION.RPi_GO_BACK:
                return_value = goBack()
            elif direction == RPi_DIRECTION.STAND or direction == RPi_DIRECTION.RPi_INVALID:
                return_value = stand()
        
        # Azuriranje Contexta
        ContextRPi.RPI_RESPONSE = return_value

        if return_value == RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_INVALID or return_value  == RPi_RESPONSE_OBSTRACLE.RPi_FAILURE:
            print("Command failure - send notification")
        elif return_value == RPi_RESPONSE_OBSTRACLE.RPI_OBSTRACLE_DETECTED:
            print("Obstracle detected - send notification")
        elif return_value == RPi_RESPONSE_OBSTRACLE.RPI_OBSTRACLE_PASSED:
            print("Obstracle passed")
        elif return_value == RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK:
            print("Command executed successfully")

        sleep(0.5)  # in seconds
# --------------------------MODUL ZA KONTROLU HARDVERA END---------------------------
    
# -------------------------MODUL ZA AUTONOMNO KRETANJE BEGIN-------------------------
def checkTarget():
    # provera da li je cilj dostignut odn prepreka zaobidjena
    if Y_coordinate > 0 and X_coordinate == 0:
        ContextRPi.RPI_RESPONSE = RPi_RESPONSE_OBSTRACLE.RPI_OBSTRACLE_PASSED
        return True
    else:
        return False
        

def chooseTheSide(flag):
    # Proverava senzore i analizom rezoltata bira stranu sa koje zaobilazi prepreku
    d_left_curr, d_ahead_curr, d_right_curr = checkSensors()

    # Pravi mali zaokret u levo i ponovo proverava senzore
    turnLeft10Degrees()
    d_left_curr_l1, d_ahead_curr_l1, d_right_curr_l1 = checkSensors()
    # Pravi jos jedan mali zaokret u levo i ponovo proverava senzore
    turnLeft10Degrees()
    d_left_curr_l2, d_ahead_curr_l2, d_right_curr_l2 = checkSensors()
    
    # Vraca se u prvobitan polozaj
    turnRight10Degrees()
    turnRight10Degrees()
    
    # Pravi mali zaokret u desno i ponovo proverava senzore
    turnRight10Degrees()
    d_left_curr_r1, d_ahead_curr_r1, d_right_curr_r1 = checkSensors()

    # Pravi jos jedan mali zaokret u desno i ponovo proverava senzore
    turnRight10Degrees()
    d_left_curr_r2, d_ahead_curr_r2, d_right_curr_r2 = checkSensors()

    # Vraca se u prvobitan polozaj
    turnLeft10Degrees()
    turnLeft10Degrees()
    
    sum_left = d_left_curr + d_left_curr_l1 + d_ahead_curr_l1 + d_left_curr_l2 + d_ahead_curr_l2 + d_left_curr_r1 + d_left_curr_r2
    sum_right = d_right_curr + d_right_curr_l1 + d_right_curr_l2 + d_ahead_curr_r1 + d_right_curr_r1 + d_ahead_curr_r2 + d_right_curr_r2
    
    sum_left1 =  d_ahead_curr_l1 + d_ahead_curr_l2 + d_left_curr_r2
    sum_right1 = d_ahead_curr_r1 + d_ahead_curr_r2 + d_right_curr_l2
    
    if ContextRPi.prevSide != RPi_SIDE.RPi_SIDE_INVALID and flag == False:
        return ContextRPi.prevSide
    elif ContextRPi.prevSide != RPi_SIDE.RPi_SIDE_INVALID and flag == True:
        if sum_left1 >= sum_right1:
            return RPi_SIDE.RPi_SIDE_LEFT
        else:
            return RPi_SIDE.RPi_SIDE_RIGHT
    elif ContextRPi.prevSide == RPi_SIDE.RPi_SIDE_INVALID:
        if sum_left == sum_right:
            return RPi_SIDE.RPi_SIDE_CANNOT_DECIDE
        elif sum_left > sum_right:
            return RPi_SIDE.RPi_SIDE_LEFT
        elif sum_left < sum_right:
            return RPi_SIDE.RPi_SIDE_RIGHT
            
        
    return RPi_SIDE.RPi_SIDE_CANNOT_DECIDE

    
def BUGAlgorithm():
    flagGo = False
    side = RPi_SIDE.RPi_SIDE_INVALID
    obstracleDetected = RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_INVALID
    targetReached = False
    X_coordinate = 0
    Y_coordinate = 0
    Angle = 0


    while(ContextRPi.RPI_AUTO_MODE_ENABLED == RPi_AUTO_MODE.RPi_AUTO_MODE_ENABLED):
        
        # Provera da li je cilj dostignut
        targetReached = checkTarget()
        if targetReached == True:
            turns = Angle/5
            turns = int(turns)
            if turns < 0:
                turns = -turns
            
            for i in range(0,turns):
                if Angle < 0:
                    turnRight5Degrees()
                else:
                    turnLeft5Degrees()

            print("Cilj dostignut(prepreka zaobidjena) -> nastavljam dalje napred")
            break

        # Kretanje napred
        obstracleDetected = goAhead()
        while obstracleDetected == RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK: # ide napred sve dok moze
            flagGo = True
            Y_coordinate = 8.9
            obstracleDetected = goAhead()
            
        if obstracleDetected == RPi_RESPONSE_OBSTRACLE.RPI_OBSTRACLE_DETECTED:
            # Bira stranu sa koje obilazi prepreku
            ContextRPi.prevSide = side
            side = chooseTheSide(flagGo)
    
            if side == RPi_SIDE.RPi_SIDE_LEFT:  # Pokusava obilazak sa leve strane
                flagGo = False 
                turnLeft5Degrees()
                Angle = Angle - 5
            elif side == RPi_SIDE.RPi_SIDE_RIGHT: # pokusava obilazak sa desne strane
                flagGo = False
                turnRight5Degrees()
                Angle = Angle + 5
            elif side == RPi_SIDE.RPi_SIDE_CANNOT_DECIDE:
                print("Ne mogu da odlucim sa koje strane da obidjem prepreku, biram random")
                randNumber = random.random()
                if randNumber < 0.5:
                    side = RPi_SIDE.RPi_SIDE_LEFT
                    flagGo = False # Pokusava obilazak sa leve strane
                    turnLeft5Degrees()
                    Angle = Angle - 5
                else:
                    side = RPi_SIDE.RPi_SIDE_RIGHT
                    flagGo = False # Pokusava obilazak sa leve strane
                    turnRight5Degrees()
                    Angle = Angle + 5
            elif side == RPi_SIDE.RPi_SIDE_INVALID:
                print("ERROR chooseSide")
                
# -------------------------_MODUL ZA AUTONOMNO KRETANJE END-_------------------------
    
# ----------------------------MODUL ZA KOMUNIKACIJU BEGIN----------------------------
def FlaskApplication():
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def index():
        data = request.data
        req_data = request.get_json()
        message_type = req_data['message_type']
        value = req_data['value']
        str_msg_type = str(message_type)
        print("Dobijeno u zahtevu:"+str_msg_type+"  "+value)

        global ContextRPi
        global lock

        lock.acquire()
        try:
            # ########### RPi_MSG_DIRECTION BEGIN #########
            if str_msg_type.find("RPi_MSG_DIRECTION") != -1:

                # Samo ako auto mod nije ukljucen zahtev sa aplikacije
                # moze da menja Context u suprotnom to moze samo BUGAlgorithm funkcija
                if ContextRPi.RPI_AUTO_MODE_ENABLED == RPi_AUTO_MODE.RPi_AUTO_MODE_INVALID:
                    # ContextRPi.RPI_DROID_COMMAND_MSG_TYPE = RPi_MSG_TYPE.RPi_MSG_DIRECTION

                    if value.find("0 stand") != -1:
                        print("KOMANDA ZA KRETANJE: STANI")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_STAND)
                    elif value.find("1 go_ahead") != -1:
                        print("KOMANDA ZA KRETANJE: IDI NAPRED")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_GO_AHEAD)
                    elif value.find("2 semi_left") != -1:
                        print("KOMANDA ZA KRETANJE: IDI POLU LEVO")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_GO_AHEAD_SEMI_LEFT)
                    elif value.find("3 semi_right") != -1:
                        print("KOMANDA ZA KRETANJE: IDI POLU DESNO")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_GO_AHEAD_SEMI_RIGHT)
                    elif value.find("4 left") != -1:
                        print("KOMANDA ZA KRETANJE: IDI LEVO")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_GO_LEFT)
                    elif value.find("5 right") != -1:
                        print("KOMANDA ZA KRETANJE: IDI DESNO")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_GO_RIGHT)
                    elif value.find("6 back") != -1:
                        print("KOMANDA ZA KRETANJE: IDI NAZAD")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_GO_BACK)
                    elif value.find("7 back semi left") != -1:
                        print("KOMANDA ZA KRETANJE: IDI NAZAD POLU LEVO")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_GO_BACK_SEMI_LEFT)
                    elif value.find("8 back semi right") != -1:
                        print("KOMANDA ZA KRETANJE: IDI NAZAD POLU DESNO")
                        ContextRPi.update_context_direction(RPi_MSG_TYPE.RPi_MSG_DIRECTION, RPi_DIRECTION.RPi_GO_BACK_SEMI_RIGHT)
                elif ContextRPi.RPI_AUTO_MODE_ENABLED == True:
                    print("AUTO MOD ukljucen - ignorisem naredbe za smer")
            # ########### RPi_MSG_DIRECTION END ###########

            # ########### RPi_MSG_CONNECTING BEGIN ############
            elif str_msg_type.find("RPi_MSG_CONNECTING") != -1:
                ContextRPi.update_context_conn(RPi_MSG_TYPE.RPi_MSG_CONNECTING, True)
                print("Uspostavljanje veze")
                ContextRPi.threadControlGPIO.start()
            # ######### RPi_MSG_CONNECTING END ############

            # ########## RPi_MSG_DISCONNECTING BEGIN ############
            elif str_msg_type.find("RPi_MSG_DISCONNECTING") != -1:
                ContextRPi.update_context_conn(RPi_MSG_TYPE.RPi_MSG_DISCONNECTING, False)
                print("Prekidanje veze")
                ContextRPi.threadControlGPIO.join()
            # ############ RPi_MSG_DISCONNECTING END #############

            # ############## RPi_MSG_AUTO_MODE BEGIN #############
            elif str_msg_type.find("RPi_MSG_AUTO_MODE") != -1:
                if value.find("enable_auto_mode") != -1:
                    ContextRPi.update_context_auto_mode(RPi_MSG_TYPE.RPi_MSG_AUTO_MODE, RPi_AUTO_MODE.RPi_AUTO_MODE_ENABLED)
                    ContextRPi.threadBUG.start()
                    print("Enable auto mode")
                elif value.find("disable_auto_mode") != -1:
                    ContextRPi.update_context_auto_mode(RPi_MSG_TYPE.RPi_MSG_AUTO_MODE, RPi_AUTO_MODE.RPi_AUTO_MODE_DISABLED)
                    print("Disable auto mode")
                    ContextRPi.threadBUG.join()
            # ########## RPi_MSG_AUTO_MODE END ##############
        finally:
            lock.release()
            
            print("-----DUMP CONTEXT------")
            print("-----SET RPI_DROID_COMMAND TYPE: ",
                  ContextRPi.RPI_DROID_COMMAND_MSG_TYPE)
            print("-----SET RPI_DROID_COMMAND: DIRECTION: ",
                  ContextRPi.RPI_DROID_DIRECTION)
            print("-----SET RPI_DROID_COMMAND: CONNECTED: ",
                   ContextRPi.RPI_DRОID_CONNECTED)
            print("-----SET RPI_DROID_COMMAND: RPI_AUTO_MODE_ENABLED: ",
                  ContextRPi.RPI_AUTO_MODE_ENABLED)
            print("-----SET RPI_DROID_COMMAND: RPI_RESPONSE: ",
                  ContextRPi.RPI_RESPONSE)

        sResponse = json.dumps({"response_status": ContextRPi.getStringResponse(), "aditional_info": ContextRPi.aditionalResponseInfo}, sort_keys=False)
        print(sResponse)
        return sResponse

    try:
        app.run(debug=False, use_reloader=False, threaded=True, host='0.0.0.0')
    except Exception:
        print("Pokretanje flask aplikacije za komunikaciju neuspesno")

# ----------------------------MODUL ZA KOMUNIKACIJU END----------------------------

# Klasa Context je deljeni resurs preko koje komuniciraju svi moduli
class Context:
    def __init__(self):
        self.RPI_DROID_COMMAND_MSG_TYPE = RPi_MSG_TYPE.RPi_MSG_INVALID
        self.RPI_DROID_DIRECTION = RPi_DIRECTION.RPi_INVALID
        self.RPI_DRОID_CONNECTED = False
        self.RPI_AUTO_MODE_ENABLED = RPi_AUTO_MODE.RPi_AUTO_MODE_INVALID
        self.RPI_RESPONSE = RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_INVALID
        self.aditionalResponseInfo = ""
        self.prevSide = RPi_SIDE.RPi_SIDE_INVALID
        self.threadControlGPIO = Thread(target=ControlGPIO, args=())
        self.threadBUG = Thread(target=BUGAlgorithm, args=())

    def update_context_direction(self, msg_type, direction):
        print("update_context_direction called")
        self.RPI_DROID_COMMAND_MSG_TYPE = msg_type
        self.RPI_DROID_DIRECTION = direction

    def update_context_conn(self, conn):
        print("update_context_direction called")
        self.RPI_DRОID_CONNECTED = conn
        
    def update_context_auto_mode(self, am):
        print("update_context_conn called")
        self.RPI_AUTO_MODE_ENABLED = am
    
    def update_context_response(self, response):
        print("update_context_response called")
        self.RPI_RESPONSE = response
        
    def update_context_aditional_info(self, ad_info):
        print("update_context_aditional_info called")
        self.aditionalResponseInfo = ad_info
        
    def update_context_prev_side(self, prev):
        print("update_context_prev_side called")
        self.prevSide = prev
    
    def get_current_msg_type(self):
        print("get_current_msg_type called")
        return self.RPI_DROID_COMMAND_MSG_TYPE

    def get_current_direction(self):
        print("get_current_direction called")
        return self.RPI_DROID_DIRECTION
        
    def get_connection(self):
        print("get_connection called")
        return self.RPI_DRОID_CONNECTED
    
    def get_auto_mode(self):
        print("get_auto_mode called")
        return self.RPI_AUTO_MODE_ENABLED
        
    def get_curr_response(self):
        print("get_curr_response called")
        return self.RPI_RESPONSE
        
    def get_aditional_indo(self):
        print("get_aditional_indo called")
        return self.aditionalResponseInfo
        
    def get_prev_side(self):
        print("get_prev_side called")
        return self.prevSide
    
    def getStringResponse(self):
        
        response = ""
        
        if self.RPI_RESPONSE == RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_INVALID or self.RPI_RESPONSE == RPi_RESPONSE_OBSTRACLE.RPi_FAILURE:
            response = "FAILURE"
        elif self.RPI_RESPONSE == RPi_RESPONSE_OBSTRACLE.RPi_RESPONSE_OK:
            response = "OK"
        elif self.RPI_RESPONSE == RPi_RESPONSE_OBSTRACLE.RPI_OBSTRACLE_DETECTED:
            response = "OBSTRACLE_DETECTED"
        elif self.RPI_RESPONSE == RPi_RESPONSE_OBSTRACLE.RPI_OBSTRACLE_PASSED:
            response = "OBSTRACLE_PASSED"
        else:
            response = "UNDEFINED"

        return response
        
# Azuriranje i citanje vrednosti iz objekta klase Context se stiti ovim mutexom
lock = threading.Lock()
ContextRPi = Context()

if __name__ == '__main__':
    # Potrebno je koristiti 0.0.0.0 u app.run da bi web server
    # bio dostupan bilo kom uredjaju u istoj mrezi
    print("pokrenuta aplikacija")
    # _thread.start_new_thread(ControlGPIO,())
    # tid = _thread.start_new_thread(FlaskApplication, ())

    # t1.join()
    # t1 = Thread(target=ControlGPIO, args=())
    # t1.start()

    # t = Thread(target=FlaskApplication, args=())
    # t.start()
    # t.join()
    FlaskApplication()

    # t1.join()