# encoding task

from psychopy import visual, core, event, gui
import pandas as pd

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
		        