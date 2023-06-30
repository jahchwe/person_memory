from psychopy import visual, core, event
import glob

win = visual.Window(size=(720,450), fullscr=False, color="white", screen=0)

faces = glob.glob('../csv_generation/white_neutral_faces/*')
faces = faces[0:8]

stim_size = (0.45, 0.45)
x_half = stim_size[0]/2
y_half = stim_size[0]/2
x_shift = 0
y_shift = 0.25

locations = [(x_half*-3 + x_shift, y_half + y_shift),
			(x_half*-3 + x_shift, y_half*-1 + y_shift),
			(x_half*-1 + x_shift, y_half*-1 + y_shift), 
			(x_half*-1 + x_shift, y_half + y_shift), 
			(x_half + x_shift, y_half*-1 + y_shift), 
			(x_half + x_shift, y_half + y_shift), 
			(x_half*3 + x_shift, y_half*-1 + y_shift),
			(x_half*3 + x_shift, y_half + y_shift)]

for i in range(len(faces)):
	stim = visual.ImageStim(win, image = faces[i], pos = locations[i])
	stim.size =stim_size

	stim.draw()

rect = visual.Rect(win, pos=locations[0], lineColor ='red', fillColor = None, lineWidth = 4)
rect.size = stim_size
rect.draw()

win.flip()

core.wait(5)
