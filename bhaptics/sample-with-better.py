from time import sleep
from bhaptics import better_haptic_player as player
# import keyboard
# import pygame
from psychopy import visual, core
import random


#create player
player.initialize()

#register patterns
print("register CenterX")
player.register("1_L", "1_L.tact")
print("register Circle")
player.register("Circle", "Circle.tact")
print("register test")
player.register("test", "Slash9_Back_Vest.tact")
print("register lewa_ciągły góra-dół")
player.register("lewa_ciągły góra-dół", "lewa_ciągły góra-dół.tact")

#create a method which submits patterns according to index 
def play(index):
    if index == 1:
        print("submit 1_L")
        player.submit_registered("1_L")

    elif index == 2:
        print("submit Circle")
        player.submit_registered_with_option("Circle", "alt2",
                                             scale_option={"intensity": 10, "duration": 2},
                                             rotation_option={"offsetAngleX": 180, "offsetY": 0})
    elif index == 3:
        # print("submit Circle With Diff AltKey")
        # player.submit_registered_with_option("Circle", "alt2",
        #                                      scale_option={"intensity": 1, "duration": 1},
        #                                      rotation_option={"offsetAngleX": 0, "offsetY": 0})
        player.submit_dot("backFrame", "VestBack", [{"index": 7, "intensity": 100}], 100)
    elif index == 4:
        print("lewa_ciągły góra-dół")
        player.submit_registered("lewa_ciągły góra-dół")
    return index

def trial():
    global pattern_type, correct, latency
    prev_stim = ''

    pattern_type = random.choice((1,2,3,4))
    while pattern_type == prev_stim:
        pattern_type = random.choice(((1,2,3,4)))
    prev_stim = pattern_type

    play(pattern_type)
    sleep(2)

#main 
def run():     

    # print("Press Q to quit")


    for i in range(0,5):
        trial()




if __name__ == "__main__":
    run()
