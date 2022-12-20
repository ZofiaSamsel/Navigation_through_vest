from time import sleep
from bhaptics import better_haptic_player as player
import keyboard
import pygame

#window's features
background_colour = (255,0,255)
(width, height) = (820,600)

#create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Test PyGame')
screen.fill(background_colour)

pygame.display.flip()

#create player
player.initialize()

#register patterns
print("register CenterX")
player.register("CenterX", "CenterX.tact")
print("register Circle")
player.register("Circle", "Circle.tact")
print("register test")
player.register("test", "Slash9_Back_Vest.tact")
print("register lewa_ciągły góra-dół")
player.register("lewa_ciągły góra-dół", "lewa_ciągły góra-dół.tact")

#create a method which register patterns according to index 
def play(index):
    if index == 1:
        print("submit LEWA/CenterX")
        player.submit_registered("test")

    elif index == 2:
        print("submit Circle")
        player.submit_registered_with_option("Circle", "alt",
                                             scale_option={"intensity": 1, "duration": 1},
                                             rotation_option={"offsetAngleX": 180, "offsetY": 0})
    elif index == 3:
        print("submit Circle With Diff AltKey")
        player.submit_registered_with_option("Circle", "alt2",
                                             scale_option={"intensity": 1, "duration": 1},
                                             rotation_option={"offsetAngleX": 0, "offsetY": 0})
    elif index == 4:
        print("lewa_ciągły góra-dół")
        player.submit_registered("lewa_ciągły góra-dół")
    return index


#main 
def run(): 
    print("Press Q to quit")
    running = True
    while running:
        
        #creating a loop to check events that are occurring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #checking if keydown event happened or not
            if event.type == pygame.KEYDOWN:
            
                #checking if key "A" was pressed
                if event.key == pygame.K_q:
                    print("Key Q has been pressed")
                    screen.close()
                    break
                
                #checking if key "J" was pressed
                if event.key == pygame.K_j:
                    print("Key J has been pressed")
                    play(1)
                    
                #checking if key "P" was pressed
                if event.key == pygame.K_p:
                    print("Key P has been pressed")
                    play(2)
                
                #checking if key "M" was pressed
                if event.key == pygame.K_m:
                    print("Key M has been pressed")
                    play(3)

    



   #wait for pressed key to play pattern
    #while True:
     #   key = keyboard.read_key()
      #  if key == "q" or key == "Q":
       #     break
        #play(int(key))
        #elif key == "1":
         #   play(1)
    #    elif key == "2":
     #       play(2)
      #  elif key == "3":
       #     play(3)
        #elif key == "4":
         #   play(4)
        #elif key == "5":
    #print information abot patterns, device
    #print('=================================================')
    #print('is_playing', player.is_playing_key())
    #print(key)
    #print('is_playing_key(CenterX)', player.is_playing_key('lewe_przejscie_poziome'))
    #print('is_device_connected(Vest)', player.is_device_connected('Vest'))
    #print('is_device_connected(ForearmL)', player.is_device_connected('ForearmL'))
    #print('=================================================')


if __name__ == "__main__":
    run()
