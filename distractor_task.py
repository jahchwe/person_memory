# distractor
from psychopy import visual, core, event
from psychopy.visual import Circle
import random
import pandas as pd

def run(run_id, outpath, win):
	num_trials = 20
	less_keys = ['1','2','3','4']
	more_keys = ['5','6','7','8']

	text = visual.TextStim(win, text = 'You will now complete a math reasonsing task\nOn each trial you will be shown a screen of dots, followed by a number.\nYour job is to indicate whether the number is greater or less than the number of dots on the screen.\nUse any button on your left hand to indicate LESS. Use any button on your right hand to indicate RIGHT\nPress any button to continue', height = 0.05, pos = (0, -0.35), color = "black")
	text.draw()
	win.flip()
	event.waitKeys(keyList = less_keys.extend(more_keys))
	event.clearEvents()
	
	text = visual.TextStim(win, text = 'You will have unlimited time to respond, but please go quickly with your gut feeling. Press any button to start.', height = 0.05, pos = (0, -0.35), color = "black")
	text.draw()
	win.flip()
	event.waitKeys(keyList = less_keys.extend(more_keys))
	event.clearEvents()

	global_clock = core.Clock()

	results = []

	it = 0
	while it < num_trials:
		number_of_dots = random.randint(5,20)
		dots = []

		win.flip()

		#set x and y coordinate of dots, create the dots and add to list of dots
		for i in range(number_of_dots):
			dot_x_coordinate = random.randint(-350, 350)
			dot_y_coordinate = random.randint(-250, 250)
			dot_position = (dot_x_coordinate, dot_y_coordinate)
			dot = visual.Circle(win, radius = 10, units = "pix", lineColor = [0,0,0], fillColor = [0,0,0], pos = dot_position)
			dots.append(dot)

		for dot in dots:
			dot.draw()
			
		win.flip()

		target_time = global_clock.getTime() + 2
		while global_clock.getTime() < target_time:
			continue

		random_num = random.randint(1, 22)
		text = visual.TextStim(win, text = "", height = 0.2 , pos = (0, 0), color = "black")
		text.setText(random_num)
		text.draw()

		win.flip()

		truth = None
		if random_num > number_of_dots:
			truth = 'more'
		else:
			truth = 'less'

		user_response = None
		while user_response is None:
			keys = event.waitKeys()
			if keys[0] in less_keys:
				user_response = 'less'
			elif keys[0] in more_keys:					
				user_response = 'more'

		results.append([it, truth==user_response])
		it += 1

	result_df = pd.DataFrame(results, columns = ['iterator', 'correct'])
	result_df.to_csv(outpath + '/DISTRACTOR_RUN-%s_.csv' % run_id)

