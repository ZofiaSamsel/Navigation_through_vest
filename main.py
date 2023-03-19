# !/usr/bin/env python
# -*- coding: latin-1 -*-
#--------------------------------------------------
#imports
#--------------------------------------------------
import codecs
import random
import csv
from os.path import join
import yaml
from psychopy import visual, event, gui, core
from bhaptics import better_haptic_player as player
import atexit


#create player
player.initialize()

#register patterns
print("register 1_L")
player.register("1_L", "1_L.tact")
print("register 2_L")
player.register("2_L", "2_L.tact")
print("register 3_L")
player.register("3_L", "3_L.tact")
print("register 1_R")
player.register("1_R", "1_R.tact")
print("register 2_R")
player.register("2_R", "2_R.tact")
print("register 3_R")
player.register("3_R", "3_R.tact")
print("register Circle")
player.register("Circle", "Circle.tact")
print("register TEST")
player.register("TEST", "TEST.tact")

# load config file
conf = yaml.load(open('config.yaml', encoding='utf-8'), Loader=yaml.FullLoader)

clock = core.Clock()

# RESULTS = conf(['RESULTS'])
RESULTS = [["PART_ID", "TRIAL", "WARUNEK", "PATTERN", "CORRECT", "LATENCY"]]

#--------------------------------------------------
#read text from file or add some extra text
#file_name: the name of the file to read
#return: message
#--------------------------------------------------
def read_text_from_file(file_name, insert=''):
    msg = list()
    with codecs.open(file_name, encoding='utf-8', mode='r') as data_file:
        for line in data_file:
            if not line.startswith('#'):  # if not commented line
                if line.startswith('<--insert-->'):
                    if insert:
                        msg.append(insert)
                else:
                    msg.append(line)
    return ''.join(msg)

#--------------------------------------------------
#show the info
#--------------------------------------------------
type = ""
def show_info(win, file_name, type, insert=''):
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'], alignText='center' )
    msg.draw()
    win.flip()

    #only specific keyboard buttons are available 
    #with space button
    if type == "with_space":
        key = event.waitKeys(keyList=['g', 'space'])
        if key == ['g']:
            win.close()
            player.destroy()
            core.quit()
        win.flip()
    #with the test button and space
    elif type == "with_test":
        core.wait(2)
        play('TEST')
        key = event.waitKeys(keyList=['g', 'space', 't'])
        if key == ['g']:
            win.close()
            player.destroy()
            core.quit()
        elif key == ['t']:
            play('TEST')
        win.flip()
    # # with the 1-9 lickert scale
    # elif type == "with_scale":
    #     key = event.getKeys(conf['SCALE'])
    #     if key == ['g']:
    #         win.close()
    #         player.destroy()
    #         core.quit()   
    #only exit button is available
    elif type == "without_space":
        key = event.getKeys(keyList=['g'])
        if key == ['g']:
            win.close()
            player.destroy()
            core.quit()

#--------------------------------------------------
#save data in the .csv file
#--------------------------------------------------
def save_data():
    with open(join('results', datafile), "w", newline='') as df:
        write = csv.writer(df)
        write.writerows(RESULTS)

#--------------------------------------------------
#submits patterns according to index 
#--------------------------------------------------
def play(index):
    if index == '1_L':
        print("submit 1_L")
        player.submit_registered("1_L")  
    elif index == '2_L':
        print("submit 2_L")
        player.submit_registered("2_L")
    elif index == '3_L':
        print("submit 3_L")
        player.submit_registered("3_L")
    elif index == '1_R':
        print("submit 1_R")
        player.submit_registered("1_R")  
    elif index == '2_R':
        print("submit 2_R")
        player.submit_registered("2_R")
    elif index == '3_R':
        print("submit 3_R")
        player.submit_registered("3_R")
    elif index == "TEST":
        print("submit TEST")
        player.submit_registered("TEST")

    return index

#--------------------------------------------------
#randomisation of the trials
#return the list of the trials in the random order
#--------------------------------------------------
def shaffle_trials(number_of_trials, number_of_patters):
    sets = int(number_of_trials/number_of_patters)
    stim_order = []
    [stim_order.extend(list(stim))  for i in range(sets)]
    print(stim_order)
    random.shuffle(stim_order)  
    return stim_order

#--------------------------------------------------
#one trial
#--------------------------------------------------
def run_trial(win, order, number):
    global key, rt, corr, pattern, stim_type

    # fixation
    # fix.setAutoDraw(True)
    # play('FIX')
    win.flip()
    core.wait(random.randint(1,4)) 

    #create the screen
    event.clearEvents()
    win.callOnFlip(clock.reset)

    # play the stimulus
    play(order[number])
    stim_type = order[number]
    win.flip()

    # reaction 
    while clock.getTime() <= conf['TIME_MAX']:
        key = event.getKeys(conf['REACTION_KEYS'])
        if key == ['q'] or key == ['p']:
            rt = clock.getTime()
            break
        if key == ['g']:
            win.close()
            player.destroy()
            core.quit()
   
    if clock.getTime() > conf['TIME_MAX']:
        rt = '-'

    # breake between trials
    core.wait(conf['STIM_BREAK'])

    # pattern type
    if (stim_type == "1_L") or (stim_type == "1_R"):
        pattern = 1
    elif (stim_type == "2_L") or (stim_type == "2_R"):
        pattern = 2
    elif (stim_type == "3_L") or (stim_type == "3_R"):
        pattern = 3

    # corr = correctness
    if (stim_type == "1_L" and key == ['q']) or (stim_type == "2_L" and key == ['q']) or (stim_type == "3_L" and key == ['q']) or \
        (stim_type == "1_R" and key == ['p']) or (stim_type == "2_R" and key == ['p']) or (stim_type == "3_R" and key == ['q']):
        corr = 1
    elif (stim_type == "1_L" and key == ['p']) or (stim_type == "2_L" and key == ['p']) or (stim_type == "3_L" and key == ['p']) or \
        (stim_type == "1_R" and key == ['q']) or (stim_type == "2_R" and key == ['q']) or (stim_type == "3_R" and key == ['p']):
        corr = 0
    else:
        corr = "-"

    RESULTS.append([ID, trial_no, train, pattern, corr, rt])

#-----------------------------------------------------------------------------
# experiment
#-----------------------------------------------------------------------------
# info window
#info = {'ID': '', 'PLEC': ['M', 'K'], 'WIEK': ''}
info = {'ID': '', 'WARUNEK': ''}
dlg = gui.DlgFromDict(info, title='Wpisz swoje dane :) ')
if not dlg.OK:
    print("User exited")
    core.quit()

# create ID
#ID = info['ID'] + info['PLEC'] + info['WIEK']
ID = info['ID'] + info['WARUNEK']

# create the data file 
datafile = '{}.csv'.format(ID)

# create window
window = visual.Window(units="pix", color=conf['BACKGROUND_COLOR'], fullscr=True, size=(1000, 1000))
window.setMouseVisible(False)

# stimuli
fix = visual.TextStim(win=window, text="+", color=conf['FIX_CROSS_COLOR'], height=conf['FIX_CROSS_SIZE'])
stim = ('1_L','1_R', '2_L','2_R', '3_L','3_R')

# display first info
show_info(window, join('.', 'messages', 'instr.txt'), "with_space")
show_info(window, join('.', 'messages', 'instr_1.txt'), "with_space")
show_info(window, join('.', 'messages', 'instr2.txt'), "with_test")

show_info(window, join('.', 'messages', 'train_mess.txt'), "with_space")


order = shaffle_trials(conf['N_TRIALS_EXP'], len(stim))
for i in range(conf['N_TRIALS_EXP']):
    if i == 0:
        prev_stim = '0'
    trial_no = i + 1
    train = 1
    run_trial(window,order , i)

event.waitKeys(maxWait=0)

# ending
save_data()
show_info(window, join('.', 'messages', 'fin_mess.txt'), "with_space")
window.close()
core.quit()
