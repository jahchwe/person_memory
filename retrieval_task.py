from psychopy import visual, core, event
import random
import pandas as pd
import sys


def init_recall(win, images, statement):

	stim_size = (0.45, 0.45)
	x_half = stim_size[0]/2
	y_half = stim_size[0]/2
	x_shift = 0
	y_shift = 0.25

	locations = [(x_half*-3 + x_shift, y_half + y_shift),
				(x_half*-1 + x_shift, y_half + y_shift), 
				(x_half + x_shift, y_half + y_shift), 
				(x_half*3 + x_shift, y_half + y_shift),
				(x_half*-3 + x_shift, y_half*-1 + y_shift),
				(x_half*-1 + x_shift, y_half*-1 + y_shift), 
				(x_half + x_shift, y_half*-1 + y_shift), 
				(x_half*3 + x_shift, y_half*-1 + y_shift)
				]

	stims = []
	for i in range(len(images)):
		stim = visual.ImageStim(win, image = images[i], pos = locations[i])
		stim.size = stim_size
		stims.append(stim)
		
	borders = []
	# draw all red borders in advance to save execution time.
	# return all rectangles, and then on user input just change the lineColor
	for i in range(len(images)):
		rect = visual.Rect(win, pos=locations[i], lineColor ='red', fillColor = None, lineWidth = 4)
		rect.size = stim_size
		borders.append(rect)

	# statements
	statement = visual.TextStim(win, text = statement, height = 0.2, pos = (0, -0.5), color = "black")
	
	return stims, borders, statement

def draw_recall(win, stims, borders, selected, statement):
	# draw all stim
	for i in range(len(stims)):
		stims[i].draw()

	# draw statement
	statement.draw()

	# draw selected border
	borders[selected].draw()

	win.flip()

def move_position(current_pos, direction):
	update_pos = current_pos + direction
	if update_pos > 7:
		update_pos = 0
	if update_pos < 0:
		update_pos = 7

	return(update_pos)

def run(run_id, outpath, win, retrieval_csv):
	trial_order = pd.read_csv(retrieval_csv)
	order_id = retrieval_csv.split('/')[-1].split('.')[0][4:]
	print(order_id)

	text = visual.TextStim(win, text = 'waiting for scanner', height = 0.05, pos = (0, -0.35), color = "black")
	text.draw()
	win.flip()
	event.waitKeys(keyList = ['5'])
	event.clearEvents()

	global_clock = core.Clock()
	logging = []

	faces = trial_order.face.dropna().unique()

	# set up grid dynamics
	left_keys = ['1','2','3','4']
	right_keys = ['5','6','7','8']
	quit_keys = ['9', '0']

	for it, row in trial_order.iterrows():
		if row.event_type == 'show_statement':
			statement = visual.TextStim(win, text = row.statement, height = 0.2, pos = (0, -0.5), color = "black")
			statement.draw()
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
			logging.append([it, row.event_type, row.statement, -1, -1, global_clock.getTime()])

		if row.event_type == 'show_grid':
			current_pos = random.randint(0,7)
			random.shuffle(faces)
			stims, borders, statement = init_recall(win, faces, row.statement)
			draw_recall(win, stims, borders, current_pos, statement)
			while global_clock.getTime() < row.end_time:
				keys = event.getKeys(left_keys + right_keys)
				if keys:
					if keys[0] in left_keys:
						location = move_position(current_pos, -1)
						current_pos = location
						draw_recall(win, stims, borders, current_pos, statement)
					if keys[0] in right_keys:
						location = move_position(current_pos, 1)
						current_pos = location
						draw_recall(win, stims, borders, current_pos, statement)
				else:
					continue

			logging.append([it, row.event_type, row.statement, current_pos, faces[current_pos], global_clock.getTime()])

	logging_df = pd.DataFrame(logging, columns = ['iterator', 'event_type', 'statement', 'final_position', 'selected_face', 'global_time_end'])
	logging_df.to_csv(outpath + '/RETRIEVAL_RUN-%s_%s.csv' % (run_id, order_id))

if __name__ == "__main__":
	try: 
		run_id = int(sys.argv[1])
		subj_id = sys.argv[2]
		outpath = 'output/%s' % subj_id
		subj_info = pd.read_csv(outpath + '/run_selections.csv')
		csv = subj_info.loc[(subj_info.run==run_id) & (subj_info.task=='retrieval'), 'selection'].item()
		win = visual.Window(size=(1440,900), fullscr=False, color="white", screen=0)

	except:
		print('Error in retrieving trial selections for %s. Please ensure that trial selections exist and the subjID key is correct' % (subj_id))
		exit()

	print('attempting to start RETRIEVAL task for subj %s, run_id %s' % (subj_id, run_id))
	start_input = input('Press y to continue. Note that any other output file for the corresponding subject and run will be overwritten for RETRIEVAL')
	if start_input == 'y':
		run(run_id, outpath, win, csv)



















