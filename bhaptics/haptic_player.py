#--------------------------------------------------
#import json and websocket libraries
#--------------------------------------------------
import json
from websocket import create_connection

# # send individual point for 1 seconds
# dotFrame = {
#     "Position": "Left",
#     "DotPoints": [{
#         "Index": 0,
#         "Intensity": 100
#     }, {
#         "Index": 3,
#         "Intensity": 50
#     }],
#     "DurationMillis": 1000
# }
# player.submit("dotPoint", dotFrame)
# sleep(2)
#
# pathFrame = {
#     "Position": "VestFront",
#     "PathPoints": [{
#         "X": "0.5",
#         "Y": "0.5",
#         "Intensity": 100
#     }, {
#         "X": "0.3",
#         "Y": "0.3",
#         "Intensity": 50
#     }],
#     "DurationMillis": 1000
# }
# player.submit("pathPoint", pathFrame)
# sleep(2)

#--------------------------------------------------
#create HapticPlayer class, which reads tactile patterns and play them
#--------------------------------------------------
class HapticPlayer:

    #--------------------------------------------------
    #connect with a vest
    #--------------------------------------------------
    def __init__(self):
        try:
            self.ws = create_connection("ws://localhost:15881/v2/feedbacks")
            print("Connected with websocket")
        except:
            print("Couldn't connect")
            return

    #--------------------------------------------------
    #register tactile pattern form the .tact file
    #--------------------------------------------------
    def register(self, key, file_directory):
        json_data = open(file_directory).read()

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

        #send data 
        self.ws.send(json_str)

    #--------------------------------------------------
    #simple submit tactile pattern and play it through the vest
    #--------------------------------------------------
    def submit_registered(self, key):
        submit = {
            "Submit": [{
                "Type": "key",
                "Key": key,
            }]
        }

        json_str = json.dumps(submit);

        self.ws.send(json_str)

    #--------------------------------------------------
    #submit tactile pattern with specific features (altKey, rotation, scale) and play it through the vest
    #--------------------------------------------------
    def submit_registered_with_option(
            self, key, alt_key,
            scale_option,
            rotation_option):
        # scaleOption: {"intensity": 1, "duration": 1}
        # rotationOption: {"offsetAngleX": 90, "offsetY": 0}
        submit = {
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

        json_str = json.dumps(submit);

        self.ws.send(json_str)

    #--------------------------------------------------
    #create and submit tactile pattern
    #--------------------------------------------------
    def submit(self, key, frame):
        submit = {
            "Submit": [{
                "Type": "frame",
                "Key": key,
                "Frame": frame
            }]
        }

        json_str = json.dumps(submit);

        self.ws.send(json_str)

    #--------------------------------------------------
    #create and submit tactile pattern with specific features (altKey, rotation, scale)
    #--------------------------------------------------
    def submit_dot(self, key, position, dot_points, duration_millis):
        front_frame = {
            "position": position,
            "dotPoints": dot_points,
            "durationMillis": duration_millis
        }
        self.submit(key, front_frame)

    #--------------------------------------------------
    #close the WebSocket connection
    #--------------------------------------------------
    def __del__(self):
        self.ws.close()
