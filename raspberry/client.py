import paho.mqtt.client as mqtt
from ultrasonic import UltrasonicSensor
from adxl345 import Acceloremeter
import time
import json
from datetime import datetime
import threading
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io
from pydub.effects import speedup
from button import Button

def speak(text):
    global is_playing
    is_running = True
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio = AudioSegment.from_file(fp, format="mp3")
    faster_audio = speedup(audio, playback_speed=1.1)
    play(faster_audio)
    is_playing = False

is_playing = False
def on_message(client, userdata, msg):
    try:
        global right_ultrasonic_value
        global left_ultrasonic_value
        global is_playing
        data = json.loads(msg.payload.decode())
        print(f"Received message: {data}")
        severity = data.get("severity", None)
        
        label = data.get('label', None)
        
        distance = None
        direction = data.get('direction', None)
        if direction == 'LEFT':
            direction = 'on the left'
            distance = left_ultrasonic_value
        elif direction == 'RIGHT':
            direction = 'on the right'
            distance = right_ultrasonic_value
        elif direction == 'CENTER':
            direction = 'in the middle'
            distance = right_ultrasonic_value
        else:
            direction = None
    
        #if label and direction:
        if label and direction and severity == "HIGH":
            if not is_playing:
                speak(f"There is a {label} {int(distance)} {direction}.")
        else:
            print("JSON missing 'label' or 'direction'")
    except json.JSONDecodeError:
        print("Received invalid JSON message.")
    except Exception as e:
        print(f"Error processing message: {e}")


def on_connect(client, userdata, flags, rc):
    global is_connected_to_mqtt
    if rc == 0:
        print ("Connected to MQTT broker successfully.")
        is_connected_to_mqtt = True
    else:
        print(f"Failed to connect, return code {rc}")
        is_connected_to_mqtt = False

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker.") 



def check_every_seconds(client):
    global right_ultrasonic_value
    global left_ultrasonic_value

    global check_thread_running
    check_thread_running = True
    global check_thread

    threshold_1 =  right_ultrasonic_value
    threshold_2 = left_ultrasonic_value

    i = 0

    while i < 30 and check_thread_running:
        if right_ultrasonic_value - 2 < threshold_1 < right_ultrasonic_value + 2 and left_ultrasonic_value -2 < threshold_2 < left_ultrasonic_value + 2:
            print("========================================================================================================================")
            print(f"Check {i+1} time...")
            print(f"Right Ultrasonic Value: {right_ultrasonic_value} cm \nLeft Ultrasonic Value: {left_ultrasonic_value} cm")
            i += 1
            time.sleep(1)
        else:
            print("Values changed, stopping check.")
            client.publish(publish_topic2, json.dumps({"warning": "none", "device": "U8F-MKH-GJ6"}))
            return
    if check_thread_running:
        client.publish(publish_topic2, json.dumps({"warning": "unconscious", "device": "U8F-MKH-GJ6"}))
        print({"waring": "unconscious", "device": "U8F-MKH-GJ6"})
    check_thread_running = False
    

right_ultrasonic_value = 0
left_ultrasonic_value = 0
check_thread_running = True
check_thread = None
check_thread_running2 = False
is_connected_to_mqtt = False
device = "AAAA"
is_running = False

publish_topic = "blind_sunglasses/Calert"
publish_topic2 = "blind_sunglasses/warning"
subscribe_topic = "blind_sunglasses/notice"
subscribe_topic3 = "blind_sunglasses/call"

def press_button(button, client):
    while True:
        state = button.read_state_button()
        if state == 0:
            client.publish(subscribe_topic3, json.dumps({"isCall": True}))
            print({"isCall": True})
            time.sleep(0.5)
        time.sleep(0.05) 




def main():
    global is_connected_to_mqtt
    global right_ultrasonic_value
    global left_ultrasonic_value
    global check_thread_running
    global check_thread

    global check_thread_running2
    global left_ultrasonic_value
    global right_ultrasonic_value

    client = mqtt.Client(clean_session=True)
    client.connect("192.168.243.42", 1883)
    client.on_connect = on_connect 
    client.on_disconnect = on_disconnect
    client.loop_start()

    while not is_connected_to_mqtt:
        print("Waiting for MQTT connection...")
        print(is_connected_to_mqtt)
        time.sleep(2)

    client.on_message = on_message
    client.subscribe(subscribe_topic, qos=1)

    left_ultrasonic = UltrasonicSensor(24, 23)
    print("Ultrasonic Sensor 1 initialized.")
    right_ultrasonic_2 = UltrasonicSensor(27, 17)
    print("Ultrasonic Sensor 2 initialized.")
    adxl345 = Acceloremeter()  
    print("ADXL345 Accelerometer initialized.")
    button = Button(5)
    print("Button initialized.")
    print("All sensors initialized successfully.")

    #if not check_thread_running2:
    #check_thread_running2 = True
    check_thread2 = threading.Thread(target=press_button, args=(button,client,))
    check_thread2.start()

    while True:
        try:
            acceloremeter_value = adxl345.get_acceleration()
            left_ultrasonic_value = left_ultrasonic.get_distance()
            right_ultrasonic_value = right_ultrasonic_2.get_distance()
            left_ultrasonic_value = 200

            #left = False
            #right = False        
            #if 0 < left_ultrasonic_value < 100:
                #left = True
                #if not is_running:
                    #threading.Thread(target=speak, args=(f"Obstacle on the left at {int(left_ultrasonic_value)} centimeters.",)).start()
            #if 0 < right_ultrasonic_value < 100:
                #right = True  
                #if not is_running:
                    #threading.Thread(target=speak, args=(f"Obstacle on the right at {int(right_ultrasonic_value)} centimeters.",)).start()

            # if left and right:
            #     speak(f"Obstacles on the left and right at {int(left_ultrasonic_value)} and {int(right_ultrasonic_value)} centimeters.")
            # elif left:
            #     speak(f"Obstacle on the left at {int(left_ultrasonic_value)} centimeters.")
            # elif right:
            #     speak(f"Obstacle on the right at {int(right_ultrasonic_value)} centimeters.")
            print("========================================================================================================================")
            print(f"Left Ultrasonic Distance: {left_ultrasonic_value} cm\nRight Ultrasonic Distance: {right_ultrasonic_value} cm\nAcceleration: {acceloremeter_value:.2f} g")
            is_send_distance = False
            is_send_acceleration = False
            if left_ultrasonic_value > 0 and right_ultrasonic_value > 0 and (left_ultrasonic_value < 100 or right_ultrasonic_value < 100):
                is_send_distance = True
            else:
                is_send_distance = False
            
            if acceloremeter_value >= 1.3:
                is_send_acceleration = True
                print("Acceleration exceeds threshold, checking every second...")
                if check_thread_running:
                    check_thread_running = False
                    if check_thread is not None:
                        check_thread.join()
                
                check_thread = threading.Thread(target=check_every_seconds, args=(client,))
                check_thread.start() 
            else:
                is_send_acceleration = False 

            if is_send_distance or is_send_acceleration:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                payload = {
		    "device": "U8F-MKH-GJ6",
                    "timestamp": timestamp,
                    "left_distance": left_ultrasonic_value,
                    "right_distance2": right_ultrasonic_value,
                    "isFall": is_send_acceleration
                }
                print(f"Publishing payload: {payload}")
                payload_json = json.dumps(payload)
                client.publish(publish_topic, payload_json, qos=1)
            time.sleep(1)  # Adjust the sleep time as needed

        except Exception as e:
            print(f"Error in main loop: {e}")

if __name__ == "__main__":
    main()
