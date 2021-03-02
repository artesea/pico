import time
import picokeypad as keypad
import random

# The following variables change the way the game is played
maxlength = 4 # set the number of buttons needed to unlock
shuf = 1      # set to zero if you wish to have the same lock everytime
debug = 1     # set to zero if you don't want to see the answer within the console
# if shuf is set to 0 you should set the lock here making sure it's as long as maxlenght and contains unique numbers, eg [9,0,11,6]
answer = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# END of setting variables

keypad.init()
keypad.set_brightness(1.0)

lit = -1
last_button_states = 0
colour_index = 0
spiral = [0,1,2,3,7,11,15,14,13,12,8,4,5,6,10,9]

NUM_PADS = keypad.get_num_pads()
    
def shuffle(seq):
    l = len(seq)
    for i in range(l):
        j = random.randrange(l)
        seq[i], seq[j] = seq[j], seq[i]

#print(answer)
while True:
    if lit == -1:
        if shuf:
            shuffle(answer)
        if debug:
            print(answer)
        lit = 0
    button_states = keypad.get_button_states()
    if last_button_states != button_states:
        last_button_states = button_states
        if button_states > 0:
            button = -1
            for i in range (0, NUM_PADS):
                if button_states == 2**i:
                    button = i
                    break
            #print(lit,button_states,button)
            if answer[lit] == button:
                keypad.illuminate(button, 0x00, 0x20, 0x00)
                keypad.update()
                lit += 1
            else:
                for i in range(0, NUM_PADS):
                    x = (i + button) % NUM_PADS
                    keypad.illuminate(x, 0x20, 0x00, 0x00)
                    keypad.update()
                    time.sleep(0.05)
                time.sleep(0.2)
                for i in range(0, NUM_PADS):
                    keypad.illuminate(i, 0x00, 0x00, 0x00)
                keypad.update()                    
                lit = 0
            if lit == maxlength:
                time.sleep(1)
                for i in spiral:
                    keypad.illuminate(i, 0x20, 0x20, 0x00)
                    keypad.update()
                    time.sleep(0.05)
                for i in spiral:
                    keypad.illuminate(i, 0x00, 0x00, 0x00)
                    keypad.update()
                    time.sleep(0.05)
                lit = -1
                
    time.sleep(0.1)
