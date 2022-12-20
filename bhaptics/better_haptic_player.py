#--------------------------------------------------
#import json, socket, websocket, threading libraries
#--------------------------------------------------
import json
import socket
from websocket import create_connection, WebSocket
import threading

ws = None

active_keys = set([])
connected_positions = set([])

#--------------------------------------------------
#create WebSocketReceiver class
#--------------------------------------------------
class WebSocketReceiver(WebSocket):
    
    #--------------------------------------------------
    #create conection with the vest
    #--------------------------------------------------
    def recv_frame(self):
        global active_keys
        global connected_positions
        frame = super().recv_frame()
        try:
            frame_obj = json.loads(frame.data)
            active = frame_obj['ActiveKeys']

            # if len(active) > 0:
            #     print (active)
            active_keys = set(active)
            connected_positions = set(frame_obj['ConnectedPositions'])
        except:
            active_keys = set([])
            connected_positions = set([])
        #print(connected_positions)

        return frame


def thread_function(name):
    while True:
        if ws is not None:
            ws.recv_frame()


#--------------------------------------------------
#connect with the vest
#--------------------------------------------------
def initialize():
    global ws
    try:
        ws = create_connection("ws://localhost:15881/v2/feedbacks",
                               sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),),
                               class_=WebSocketReceiver)

        x = threading.Thread(target=thread_function, args=(1,))
        x.start()
    except:
        print("Couldn't connect")
        return

#--------------------------------------------------
#close the WebSocket connection
#--------------------------------------------------
def destroy():
    if ws is not None:
        ws.close()

#--------------------------------------------------
#return if there are any active keys
#--------------------------------------------------
def is_playing():
    return len(active_keys) > 0

#--------------------------------------------------
#return which keys are active
#--------------------------------------------------
def is_playing_key(key):
    return key in active_keys

#--------------------------------------------------
#return which device ins connected
#position: Vest Head ForeamrL ForearmR HandL HandR FootL FootR
#--------------------------------------------------
def is_device_connected(position):
    return position in connected_positions

#--------------------------------------------------
#register tactile pattern form the .tact file
#--------------------------------------------------
def register(key, file_directory):
    json_data = open(file_directory).read()

    print(json_data)

    data = json.loads(json_data)
    project = data["project"]

    layout = project["layout"]
    tracks = project["tracks"]

    request = {
        "Register": [{
            "Key": key,
            "Project": {
                "Tracks": tracks,
                "Layout": layout
            }
        }]
    }
    #convert to json 
    json_str = json.dumps(request)

    __submit(json_str)

#--------------------------------------------------
#simple submit tactile pattern and play it through the vest
#--------------------------------------------------
def submit_registered(key):
    request = {
        "Submit": [{
            "Type": "key",
            "Key": key,
        }]
    }

    json_str = json.dumps(request)

    __submit(json_str)

#--------------------------------------------------
#submit tactile pattern with specific features (altKey, rotation, scale) and play it through the vest
#--------------------------------------------------
def submit_registered_with_option(
        key, alt_key,
        scale_option,
        rotation_option):
    # scaleOption: {"intensity": 1, "duration": 1}
    # rotationOption: {"offsetAngleX": 90, "offsetY": 0}
    request = {
        "Submit": [{
            "Type": "key",
            "Key": key,
            "Parameters": {
                "altKey": alt_key,
                "rotationOption": rotation_option,
                "scaleOption": scale_option,
            }
        }]
    }

    json_str = json.dumps(request);

    __submit(json_str)

#--------------------------------------------------
#create and submit tactile pattern
#--------------------------------------------------
def submit(key, frame):
    request = {
        "Submit": [{
            "Type": "frame",
            "Key": key,
            "Frame": frame
        }]
    }

    json_str = json.dumps(request);

    __submit(json_str)

#--------------------------------------------------
#create and submit tactile pattern with specific features (altKey, rotation, scale)
#--------------------------------------------------
def submit_dot(key, position, dot_points, duration_millis):
    front_frame = {
        "position": position,
        "dotPoints": dot_points,
        "durationMillis": duration_millis
    }
    submit(key, front_frame)

#--------------------------------------------------
#send data do json
#--------------------------------------------------    
def __submit(json_str):
    if ws is not None:
        ws.send(json_str)
