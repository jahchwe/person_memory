# encoding task

from psychopy import visual, core, event, gui
import pandas as pd
import sys

def run(run_id, outpath, win, encoding_csv):

	trial_order = pd.read_csv(encoding_csv)
	order_id = encoding_csv.split('/')[-1].split('.')[0][4:]
	print(order_id)
	        	
	text = visual.TextStim(win, text = 'waiting for scanner', height = 0.05, pos = (0, -0.35), color = "black")
	text.draw()
	win.flip()
	event.waitKeys(keyList = ['5'])
	event.clearEvents()

	global_clock = core.Clock()
	logging = []
	
	for it, row in trial_order.iterrows():
		if row.event_type == 'encoding':
			image = visual.ImageStim(win, image = row.face, pos = (0, 0.1))
			image.size = (0.55, 0.55)
			text = visual.TextStim(win, text = row.statement, height = 0.05, pos = (0, -0.35), color = "black")
			
			image.draw()
			text.draw()
			win.flip()
			while global_clock.getTime() < row.end_time:
				continue
			logging.append([it, row.event_type, global_clock.getTime()])

		if row.event_type == 'jitter':
			fixation_cross  = visual.TextStim(win, text = "+", height = 0.1, pos = (0, 0), color = "black")
			fixation_cross.draw()
			win.flip()
			while global_clock.getTime() < row.end_time:
				continue
			logging.append([it, row.event_type, global_clock.getTime()])

	logging_df = pd.DataFrame(logging, columns = ['iterator', 'event_type', 'global_time_end'])
	logging_df.to_csv(outpath + '/ENCODING_RUN-%s_%s.csv' % (run_id, order_id))

if __name__ == "__main__":
	try: 
		run_id = int(sys.argv[1])
		subj_id = sys.argv[2]
		outpath = 'output/%s' % subj_id
		subj_info = pd.read_csv(outpath + '/run_selections.csv')
		csv = subj_info.loc[(subj_info.run==run_id) & (subj_info.task=='encoding'), 'selection'].item()
		win = visual.Window(size=(1440,900), fullscr=False, color="white", screen=0)

	except:
		print('Error in retrieving trial selections for %s. Please ensure that trial selections exist and the subjID key is correct' % (subj_id))
		exit()

	print('attempting to start ENCODING task for subj %s, run_id %s' % (subj_id, run_id))
	start_input = input('Press y to continue. Note that any other output file for the corresponding subject and run will be overwritten for ENCODING')
	if start_input == 'y':
		run(run_id, outpath, win, csv)






