from psychopy import visual, core, event
import random

def draw_grid(images, selected_img):
	    plt.clf()
	    i=1
	    for image in images:
	        ax = fig.add_subplot(columns, rows, i)
	        if i == selected_img:
	            rect = plt.Rectangle((0, 0), image.shape[1], image.shape[0], edgecolor=(1,0,0), linewidth=3, fill=False)
	            ax.add_patch(rect)
	            ax.imshow(image)
	            ax.axis('off')
	        else:
	            rect = plt.Rectangle((0, 0), image.shape[1], image.shape[0], edgecolor=(0.5, 0.5, 0.5), linewidth=3, fill=False)
	            ax.add_patch(rect)            
	            ax.imshow(image)
	            ax.axis('off')
	        i = i + 1
	    
	    plt.subplots_adjust(hspace=0, wspace=0)
	    
	    plt.draw()

def run():

	win = visual.Window(size=(800,600), fullscr=False, color="white", screen=0)

	statements_list = []

	#creates a list of statements
	for key in face_text_pairs.keys():
	    statements_list += face_text_pairs[key]

	global_clock = core.Clock()

	#index of image with red border
	selected_img = None

	#creates a 2x4 grid of images with a red border around image with index selected_img
	

	#event handling from keyboard input
	def press_key(event):
	    global selected_img
	    left_keys = ['1','2','3','4']
	    right_keys = ['5','6','7','8']
	    quit_keys = ['9', '0']
	    
	    if event.key in left_keys:
	        if selected_img == 1:
	            selected_img = 8
	        else:
	            selected_img = selected_img - 1
	            
	    elif event.key in right_keys:
	        if selected_img == 8:
	            selected_img = 1
	        else:
	            selected_img = selected_img + 1
	            
	    elif event.key in quit_keys:
	            plt.close()
	            
	    draw_grid(images, selected_img)
	    fig.canvas.draw()
	#matches the users guess to the correct choice, checks if correct -WILL BE IMPLEMENTED LATER           
	answers = {}

	while len(statements_list) > 0:
	    #"who said what" text display
	    text = visual.TextStim(win, text = "", height = 0.05, pos = (0, 0), color = "black")
	    random_statement = random.choice(statements_list)
	    statements_list.remove(random_statement)
	    win.flip()
	    text.setText("Who said " + random_statement + "?")
	    text.draw()
	  
	    target_time = global_clock.getTime() + 6
	    while global_clock.getTime() < target_time:
	        continue
	    win.flip() 
	    
	    #first jitter
	    fixation_cross  = visual.TextStim(win, text = "+", height = 0.1, pos = (0, 0), color = "black")
	    fixation_cross.draw()
	    
	    #time for the jitter
	    jitter_duration = random.randint(1,3)
	    target_time = global_clock.getTime() + jitter_duration
	    while global_clock.getTime() < target_time:
	        continue
	    win.flip()
	    
	    #image grid
	    fig = plt.figure(figsize=(10, 7))
	    image_files = list(face_text_pairs.keys())
	    rows = 4
	    columns = 2
	    
	    images = []
	    for file in image_files:
	        image = cv2.imread(file)
	        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	        images.append(image)
	    
	    selected_img = random.randint(1,9)
	    
	    fig.canvas.mpl_connect('key_press_event', press_key)
	    
	    draw_grid(images, selected_img)
	    
	    #time for the grid
	    target_time = global_clock.getTime() + 4
	    while global_clock.getTime() < target_time:
	        plt.pause(0.1)
	    plt.close()
	    win.flip()
	    
	    #second jitter
	    fixation_cross  = visual.TextStim(win, text = "+", height = 0.1, pos = (0, 0), color = "black")
	    fixation_cross.draw()
	    win.flip()
	    
	    #time for the jitter
	    jitter_duration = random.randint(1,3)
	    target_time = global_clock.getTime() + jitter_duration
	    while global_clock.getTime() < target_time:
	        continue
	    win.flip()

	win.close() 
	core.quit()