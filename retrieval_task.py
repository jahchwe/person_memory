from psychopy import visual, core, event
import random
import pandas as pd


def draw_grid(win, images, statement, selected):

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

	for i in range(len(images)):
		stim = visual.ImageStim(win, image = images[i], pos = locations[i])
		stim.size = stim_size

		stim.draw()

	# red border
	rect = visual.Rect(win, pos=locations[selected], lineColor ='red', fillColor = None, lineWidth = 4)
	rect.size = stim_size
	rect.draw()

	# statements
	statement = visual.TextStim(win, text = statement, height = 0.2, pos = (0, -0.5), color = "black")
	statement.draw()

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
			draw_grid(win, faces, row.statement, current_pos)
			while global_clock.getTime() < row.end_time:
				keys = event.getKeys(left_keys + right_keys)
				if keys:
					if keys[0] in left_keys:
						location = move_position(current_pos, -1)
						current_pos = location
						draw_grid(win, faces, row.statement, current_pos)
					if keys[0] in right_keys:
						location = move_position(current_pos, 1)
						current_pos = location
						draw_grid(win, faces, row.statement, current_pos)
				else:
					continue

			logging.append([it, row.event_type, row.statement, current_pos, faces[current_pos], global_clock.getTime()])

	logging_df = pd.DataFrame(logging, columns = ['iterator', 'event_type', 'statement', 'final_position', 'selected_face', 'global_time_end'])
	logging_df.to_csv(outpath + '/RETRIEVAL_RUN-%s_%s.csv' % (run_id, order_id))





















