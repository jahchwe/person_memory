from psychopy import visual, core, event, gui
import random
import os
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from PIL import Image

import encoding_task
import distractor_task

# INITIALIZE WINDOW
#!!!!!!
# I've split the size in half for development, but from Camille's script, the size should be 1440, 900
win = visual.Window(size=(1440,900), fullscr=False, color="white", screen=0)

#############################
# INITIALIZE SUBJECT
# 	Choose randomized trial orders for all 4 runs
#	Store chosen runs and print that to txt in case we need to restart a run 
#	Get subject info
#############################

stim_folder_path = "./white_neutral_faces"
file_names = []

myDlg = gui.Dlg(title="Person memory")
myDlg.addText('Subject info')
myDlg.addField('Name:')
myDlg.addField('SubjID:', 'ex. 001')
myDlg.addText('Experiment Info')
myDlg.addField('Date:', 'Month/Date/Year')
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
# ok_data is a list of responses corresponding to the order of 
if myDlg.OK:  # or if ok_data is not None
    print(ok_data)
else:
    print('user cancelled')

subjID = ok_data[1]
outpath = 'output/%s' % subjID

if not os.path.exists(outpath):
	os.makedirs(outpath)
	print('Making subject results folder')

# select a random ordering for each run
activities_order = np.random.choice(glob.glob('encoding_runs/*activities*'))
animals_order = np.random.choice(glob.glob('encoding_runs/*animals*'))
food_order = np.random.choice(glob.glob('encoding_runs/*food*'))
weather_order = np.random.choice(glob.glob('encoding_runs/*weather*'))

encoding_run_selections = [activities_order, animals_order, food_order, weather_order]
# randomize the ordering of the runs
np.random.shuffle(encoding_run_selections)
print(encoding_run_selections)

# !!!!!!!!!!!!!!!!
# TO DO
# !!!!!!!!!!!!!!!!
# Save the order selection so that we can restart at a given run if necessary
# and implement restarting at a given run selection


# !!!variant number must match between encoding and retrieval!!!

'''
for i in range(len(encoding_run_selections)):
	# run encoding
	# run distractor
	# run retrieval
'''
run_id = 0

#encoding_task.run(run_id, outpath, win, encoding_run_selections[0])
distractor_task.run(run_id, outpath, win)