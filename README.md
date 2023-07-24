# person_memory

# Log 

### 7/24/2023

Finishing this up for Quality Assurance testing

This is a finalized version of the task that is ready for validation. 

The issues discussed in the previous entry have been fixed. The red border now iterates as fast as a participant can press the button, and the script will output the selected variants for each subject. Now you can look at this text file within each subject's directory and manually start each task, in case a participant stops the scan execution.

### 7/6/2023

Checking out for vacation

All functionality is implemented, including verified non-slip timing, logging, randomization of encoding order, border iteration on the retrieval, distractor of dots, encoding task, logging, etc. 

Some things that need to be changed:
1. The iteration of the red border is too slow. I believe this is because we are re-creating the Image objects and Text object on each button press, when the only thing that is changing is the red border. From the message boards, the most time intensive component is the initialization of the visual components. We can initialize everything at the start of the task, then manipulate just what changes at runtime. That will hopefully speed the border movement up because it is far too slow right now. If we are not able to make it faster, then we will need to consider moving to the one button one stim approach. 
2. The main person_memory.py needs to be finalized, basic things like implementing all tasks. 
3. Ability to restart at a given run needs to be implemented. In the case that the participant stops the scan, we need to be able to pick up at a specific run. 

