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
import atexit




# load config file
conf = yaml.load(open('config.yaml', encoding='utf-8'), Loader=yaml.FullLoader)

clock = core.Clock()

# RESULTS = conf(['RESULTS'])
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
#show the info
#--------------------------------------------------
type = ""
def show_info(win, file_name, type, insert=''):
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    win.flip()

    #only specific keyboard buttons are available 
    #with space button
    if type == "with_space":
        key = event.waitKeys(keyList=['g', 'space'])
        if key == ['g']:
            win.close()
            core.quit()
        win.flip()

    # with the 1-9 lickert scale
    elif type == "with_scale":
        key = event.getKeys(conf['SCALE'])
        if key == ['g']:
            win.close()
            core.quit()   
    #only exit button is available
    elif type == "without_space":
        key = event.getKeys(keyList=['g'])
        if key == ['g']:
            win.close()
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
def play(win, index):
    if index == 'L':
        image_stim = visual.ImageStim(win, image= "dot.png", pos = (-400,0), size=(100, 100))
        image_stim.draw()
    elif index == 'R':
        image_stim = visual.ImageStim(win, image= "dot.png", pos = (400,0), size=(100, 100))
        image_stim.draw()
    
    return index
        
#--------------------------------------------------
#randomisation of the trials
#return the list of the trials in the random order
#--------------------------------------------------
def shaffle_trials(number_of_trials, number_of_patters):
    sets = int(number_of_trials/number_of_patters)
    stim_order = []
    [stim_order.extend(list(stim)) for i in range(sets)]
    random.shuffle(stim_order) 
    print(stim_order) 
    return stim_order

#--------------------------------------------------
#one trial
#--------------------------------------------------
def run_trial(win, order, number):
    global key, rt, corr, pattern, stim_type

    # fixation
    fix.setAutoDraw(True)
    win.flip()
    core.wait(random.randint(1,4))
    # conf['FIX_CROSS_TIME'] 

    #create the screen
    event.clearEvents()
    win.callOnFlip(clock.reset)

    # play the stimulus
    play(win, order[number])
    stim_type = order[number]
    print(stim_type)
    print(order[number])
    win.flip()

    # reaction 
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

    fix.setAutoDraw(False)
    win.flip()


    # breake between trials
    core.wait(conf['STIM_BREAK'])

    # pattern type
    if (stim_type == "L") or (stim_type == "R"):
        pattern = 0

    print(key)
    # corr = correctness
    if (stim_type == "L" and key == ['q']) or (stim_type == "R" and key == ['p']):
        corr = 1
    elif (stim_type == "L" and key == ['p']) or (stim_type == "R" and key == ['q']):
        corr = 0
    else:
        corr = "-"

    RESULTS.append([ID, trial_no, train, pattern, corr, rt])

#-----------------------------------------------------------------------------
# experiment
#-----------------------------------------------------------------------------
# info window
#info = {'ID': '', 'PLEC': ['M', 'K'], 'WIEK': ''}
info = {'ID': ''}
dlg = gui.DlgFromDict(info, title='Wpisz swoje dane :) Zapamietaj ID do drugiej czesci badania')
if not dlg.OK:
    print("User exited")
    core.quit()

# create ID
#ID = info['ID'] + info['PLEC'] + info['WIEK']
ID = info['ID']

# create the data file 
datafile = '{}.csv'.format(ID)

# create window
window = visual.Window(units="pix", color=conf['BACKGROUND_COLOR'], fullscr=False, size=(1000, 1000))
window.setMouseVisible(True)

# stimuli
fix = visual.TextStim(win=window, text="+", color=conf['FIX_CROSS_COLOR'], height=conf['FIX_CROSS_SIZE'])
stim = ('L','R')

# display first info
show_info(window, join('.', 'messages', 'instr.txt'), "with_space")
show_info(window, join('.', 'messages', 'instr_1.txt'), "with_space")

#training
show_info(window, join('.', 'messages', 'train_mess.txt'), "with_space")

# # for block_no in range(conf['NO_BLOCK_TRAIN']):
# order = shaffle_trials(conf['N_TRIALS_TRAIN'], len(stim))
# for a in range(conf['N_TRIALS_TRAIN']):
#     trial_no = a + 1
#     train = 1
#     run_trial(window,order, a)
# window.flip()

# final experiment
# show_info(window, join('.', 'messages', 'exp_mess.txt'), "with_space")

order = shaffle_trials(conf['N_TRIALS_EXP'], len(stim))
for i in range(conf['N_TRIALS_EXP']):
    if i == 0:
        prev_stim = '0'
    trial_no = i + 1
    train = 0
    run_trial(window,order , i)

event.waitKeys(maxWait=0)

# # for TIME_FOR_REAST display the mess without SPACE
# timer = core.CountdownTimer(conf['TIME_FOR_REAST'])
# while timer.getTime() > 0:
#     show_info(window, join('.', 'messages', 'break_mess.txt'), "without_space")
# show_info(window, join('.', 'messages', 'break_mess2.txt'), "with_space")
# window.flip()

# order = shaffle_trials(conf['N_TRIALS_TRAIN'], len(stim))
# for i in range(conf['N_TRIALS_EXP']):
#     if i == 0:
#         prev_stim = '0'
#     trial_no = i + 1
#     train = 0
#     run_trial(window, order, i) # with confidence space

# ending
save_data()
show_info(window, join('.', 'messages', 'fin_mess.txt'), "with_space")
window.close()
core.quit()

# if __name__ == "__main__":
#     run()