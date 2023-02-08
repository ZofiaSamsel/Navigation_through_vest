# !/usr/bin/env python
# -*- coding: latin-1 -*-
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

# load config file
conf = yaml.load(open('config.yaml', encoding='utf-8'), Loader=yaml.FullLoader)

clock = core.Clock()

RESULTS = [["PART_ID", "TRIAL", "TRAINING","PATTERN", "CORRECT", "LATENCY"]]

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
#show the info; with the SPACE button
#--------------------------------------------------
def show_info(win, file_name, insert=''):
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    play('TEST')
    win.flip()
    key = event.waitKeys(keyList=['g', 'space', 't'])
    if key == ['g']:
        win.close()
        core.quit()
    elif key == ['t']:
        play('TEST')
    win.flip()

#--------------------------------------------------
#show the info; without the SPACE button
#--------------------------------------------------
def show_info_br(win, file_name, insert=''):
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    win.flip()
    key = event.getKeys(keyList=['g'])
    if key == ['g']:
        win.close()
        core.quit()
    #test the vest

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
    elif index == "FIX":
        print("submit FIX")
        player.submit_dot("backFrame", "VestBack", [{"index": 6, "intensity": 100}], 500)
    elif index == "TEST":
        print("submit TEST")
        player.submit_registered("Circle")

    return index
        # print("submit Circle With Diff AltKey")
        # player.submit_registered_with_option("Circle", "alt2",
        #                                      scale_option={"intensity": 1, "duration": 1},
        #                                      rotation_option={"offsetAngleX": 0, "offsetY": 0})

#--------------------------------------------------
#one trial
#--------------------------------------------------
def run_trial(win):
    global key, rt, corr, pattern, stim_type, prev_stim

    # losowanie bodzca tak, ze nie ma dwoch takich samych po sobie
    stim_type = random.choice(list(stim))
    while stim_type == prev_stim:
        stim_type = random.choice(list(stim))
    prev_stim = stim_type

    # punkt fiksacji
    fix.setAutoDraw(True)
    play('FIX')
    win.flip()
    core.wait(conf['FIX_CROSS_TIME'])  # wyswietlanie samego punktu fiksacji

    # rozpoczecie trialu
    event.clearEvents()
    win.callOnFlip(clock.reset)

    play(stim_type)
    win.flip()

    # czekanie na reakcje
    while clock.getTime() <= conf['TIME_MAX']:
        key = event.getKeys(conf['REACTION_KEYS'])
        if key == ['q'] or key == ['p']:
            rt = clock.getTime()
            break
        if key == ['g']:
            win.close()
            core.quit()
   
    if clock.getTime() > conf['TIME_MAX']:
        rt = '-'

    # stim[stim_type].setAutoDraw(False)
    fix.setAutoDraw(False)
    win.flip()

    # przerwa pomiedzy trialami
    core.wait(conf['STIM_BREAK'])

    # pattern 
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
        (stim_type == "1_R" and key == ['q']) or (stim_type == "2_R" and key == ['q']) or (stim_type == "3_R" and key == ['q']):
        corr = 0
    else:
        corr = "-"

    RESULTS.append([ID, trial_no, train, pattern, corr, rt])

#-----------------------------------------------------------------------------
# okno dialogowe
info = {'ID': '', 'PLEC': ['M', 'K'], 'WIEK': ''}
dlg = gui.DlgFromDict(info, title='Wpisz swoje dane :)')
if not dlg.OK:
    print("User exited")
    core.quit()

# create ID
ID = info['ID'] + info['PLEC'] + info['WIEK']

# create the data file 
datafile = '{}.csv'.format(ID)

# create window
window = visual.Window(units="pix", color=conf['BACKGROUND_COLOR'], fullscr=False, size=(1000, 1000))
window.setMouseVisible(True)

# stimuli
fix = visual.TextStim(win=window, text="+", color=conf['FIX_CROSS_COLOR'], height=conf['FIX_CROSS_SIZE'])

stim = ('1_L','1_R', '2_L','2_R', '3_L','3_R')

# display first info
show_info(window, join('.', 'messages', 'instr.txt'))
show_info(window, join('.', 'messages', 'instr2.txt'))

#training
show_info(window, join('.', 'messages', 'train_mess.txt'))

for block_no in range(conf['NO_BLOCK_TRAIN']):
    for a in range(conf['N_TRIALS_TRAIN']):
        if a == 0:
            prev_stim = '0'
        trial_no = a + 1
        train = 1
        run_trial(window)
    window.flip()

# final experiment
show_info(window, join('.', 'messages', 'exp_mess.txt'))

for block_no in range(conf['NO_BLOCK_EXP']):
    for i in range(conf['N_TRIALS_EXP']):
        if i == 0:
            prev_stim = '0'
        trial_no = i + 1
        train = 0
        run_trial(window)

    if block_no != conf['NO_BLOCK_EXP'] - 1:

        # po 0 sek od wyswietlenia bodzca nie ma reakcji na klikniecie klawisze
        event.waitKeys(maxWait=0)

        # for TIME_FOR_REAST display the mess without SPACE
        timer = core.CountdownTimer(conf['TIME_FOR_REAST'])
        while timer.getTime() > 0:
            show_info_br(window, join('.', 'messages', 'break_mess.txt'))
        show_info(window, join('.', 'messages', 'break_mess2.txt'))
        window.flip()

# ending
save_data()
show_info(window, join('.', 'messages', 'fin_mess.txt'))
window.close()
core.quit()

# if __name__ == "__main__":
#     run()