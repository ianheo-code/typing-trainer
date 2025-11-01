import pygame, random, sys
pygame.init()

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED) # screen should be scalable to device if device resolution is smaller/larger than what we have

current_font = "inkfree" # default font, should be customizable
large_font = pygame.font.SysFont(current_font, 120) # The three sizes of fonts to mainly use for everything
small_font = pygame.font.SysFont(current_font, 85)
med_font = pygame.font.SysFont(current_font, 100)

clock = pygame.time.Clock() # to set frames per second and record increments of time for cooldowns

bg_color = "white"
text_color = "black"
colors = pygame.color.THECOLORS # all the colors and fonts in the pygame library
fonts = pygame.font.get_fonts()

# left keys, right keys, left words, right words, and both words were generated for me by GPT

left_keys = "QWERTASDFGZXCVB" # keys used mainly on the left and right hands so you can focus on one h and
right_keys = "YUIOPHJKLNM"
all_keys = left_keys + right_keys

left_words = [ # same idea as letters for words
    # 2-letter words
    "as", "at", "we",

    # 3-letter words
    "red", "rag", "gas", "war", "sat", "far", "tab", "fad", "wet",

    # 4-letter words
    "were", "rate", "fast", "west", "safe", "gate", "grab", "dart", "scar", "cast",

    # 5-letter words
    "great", "water", "waste", "craft", "brave", "bread", "trade", "grade"
]
right_words = [
    # 2-letter words
    "up", "in", "on", "no",

    # 3-letter words
    "him", "pin", "jog", "lip", "nun", "hop", "oil",

    # 4-letter words
    "join", "poll", "hill", "mono", "loom", "noon", "polo", "monk", "pink",

    # 5-letter words
    "union", "pooch", "hippo", "plump", "unpin", "jumpy"
]
all_words = [
    # 2-letter words
    "an", "at", "be", "by", "do", "go", "he", "if", "in", "is", "it", "me", "my", "no", "on", "or", "so", "to", "up", "we",
    
    # 3-letter words
    "and", "are", "can", "day", "dog", "fun", "get", "has", "her", "him", "his", "man", "not", "off", "one", "run", "see", "she", "too", "you",
    
    # 4-letter words
    "able", "also", "baby", "back", "ball", "bath", "book", "call", "come", "door", "ever", "game", "good", "have", "help", "jump", "like", "love", "play", "time",
    
    # 5-letter words
    "about", "after", "apple", "bring", "chair", "dance", "early", "every", "fruit", "green", "house", "laugh", "light", "night", "plant", "quick", "right", "small", "think", "water"
]

bank = None # the bank of letters or words that the game will randomly select for the user to type
score = 0 
current = None # the current letter/word the user must type

correct_sound = pygame.mixer.Sound("correct.mp3") # Thanks to pixabay, royalty-free sound effects
incorrect_sound = pygame.mixer.Sound("incorrect.mp3")
volume = 1
correct_sound.set_volume(volume)
incorrect_sound.set_volume(volume)

slider_width, slider_height = 400, 20 # how wide and tall the slider for volume is
slider_x, slider_y = screen_width//2 - slider_width//2 - 450, screen_height//2 - 300 # where the slider is located on the screen
handle_width = 20 # the knob on the slider's width

class Button(): # Thanks to baraltech on youtube for button code inspiration, adjusted to be based on text instead of a picture
	def __init__(self, x_pos, y_pos, text_input, size, selected):
		self.size = size
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.text_input = text_input
		self.color = text_color
		self.font = pygame.font.SysFont(current_font, self.size) # font for unselected
		self.text = self.font.render(self.text_input, True, self.color)
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.selected = pygame.font.SysFont(current_font, self.size + 10) # the font used for when a button has been selected
		self.flag = selected # flag to detect whether a button has been selected or not
	def update(self, position): # handles the basic state of the button
		self.font = pygame.font.SysFont(current_font, self.size) # have to update font in case user has changed the current font
		self.selected = pygame.font.SysFont(current_font, self.size + 10)
		if self.flag == False:
			self.color = text_color # should be red when selected, user's chosen color if not
		else:
			self.color = "red"
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom): # if mouse is over button
			self.text = self.selected.render(self.text_input, True, self.color)
		else:
			self.text = self.font.render(self.text_input, True, self.color)
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		screen.blit(self.text, self.text_rect)
	def checkForInput(self, position): # is the button being currently clicked
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
			return True
	def select(self): # switches button to "on" state
		self.flag = True
	def deselect(self): # swtiches button to "off state" for when other button is pressed
		self.flag = False
def switch_volume(volume): # to make volume adjustments easier
	correct_sound.set_volume(volume)
	incorrect_sound.set_volume(volume)
play_button = Button(screen_width//2, screen_height//2, "Play", 120, False)
options_button = Button(screen_width//2, screen_height//2 + 200, "Options", 120, False)
quit_button = Button(screen_width//2, screen_height//2 + 400, "Quit", 120, False)
back_button = Button(screen_width//2, screen_height//2 + 400, "Back", 85, False)
bh_button = Button(screen_width//2, screen_height//2 - 150, "Both hands", 85, False)
lh_button = Button(screen_width//2 - 550, screen_height//2 - 150, "Left hand", 85, False)
rh_button = Button(screen_width//2 + 550, screen_height//2 - 150, "Right hand", 85, False)
letter_button = Button(screen_width//2 - 300, screen_height//2 + 150, "Letters", 85, False)
word_button = Button(screen_width//2 + 300, screen_height//2 + 150, "Words", 85, False)
go_button = Button(screen_width//2 + 550, screen_height//2 + 400, "Go!", 85, False)
def menu(): # acts as the "portal" to hop to the other screens
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if play_button.checkForInput(pygame.mouse.get_pos()):
					game(False, None, None, None, 0) # go to the game screen/loop
				if options_button.checkForInput(pygame.mouse.get_pos()):
					options() # go to the options screen/loop
				if quit_button.checkForInput(pygame.mouse.get_pos()):
					pygame.quit()
					sys.exit()
		screen.fill(bg_color)
		play_button.update(pygame.mouse.get_pos())
		options_button.update(pygame.mouse.get_pos())
		quit_button.update(pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60) # 60 FPS
def game(start, hand, mode, current, score): # picking game mode and the game itself, can exit back to menu and select screen
	word_input = "" # what the user is trying to type
	lockout = 0 # the "cooldown" period for a user
	while True:
		if lockout > 0: # so if someone mistypes something and keeps hitting enter, there won't be an obnoxious overlay of sound but a delay will trigger
			lockout -= clock.get_time() # goes at 60 fps so should never take much more than alotted time bc updating so fast, this function returns milliseconds from last call
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if bh_button.checkForInput(pygame.mouse.get_pos()):
					hand = "Both hands"
					bh_button.select()
					lh_button.deselect()
					rh_button.deselect()
				elif lh_button.checkForInput(pygame.mouse.get_pos()):
					hand = "Left hand"
					bh_button.deselect()
					lh_button.select()
					rh_button.deselect()
				elif rh_button.checkForInput(pygame.mouse.get_pos()):
					hand = "Right hand"
					bh_button.deselect()
					lh_button.deselect()
					rh_button.select()
				elif letter_button.checkForInput(pygame.mouse.get_pos()):
					mode = "Letters"
					letter_button.select()
					word_button.deselect()
				elif word_button.checkForInput(pygame.mouse.get_pos()):
					mode = "Words"
					letter_button.deselect()
					word_button.select()
				elif go_button.checkForInput(pygame.mouse.get_pos()):
					start = True # Telling the program that we are set to enter the game
					if mode == "Letters": # if statements determine what pool game should choose from
						if hand == "Left hand":
							bank = left_keys
						elif hand == "Right hand":
							bank = right_keys
						else:
							bank = all_keys
					elif mode == "Words":
						if hand == "Left hand":
							bank = left_words
						elif hand == "Right hand":
							bank = right_words
						else:
							bank = all_words
					current = random.choice(bank)
				elif back_button.checkForInput(pygame.mouse.get_pos()):
					bh_button.deselect()
					lh_button.deselect()
					rh_button.deselect()
					word_button.deselect()
					letter_button.deselect()
					menu()
			if lockout > 0: # can't do anything else if lockout is active to prevent spam
				pass
			elif event.type == pygame.KEYDOWN:
				if start:
					if mode == "Letters":
						if event.unicode.upper() == current:
							score += 1
							pygame.mixer.Sound.play(correct_sound)
							current = random.choice(bank) # picks next letter randomly
						else:
							pygame.mixer.Sound.play(incorrect_sound)
							lockout = 500 # should be around 500 milliseconds
					else: # had to make a seperate segment for words because you can backspace and actually store an input with words
						if event.key == pygame.K_BACKSPACE:
							word_input = word_input[:-1] # makes word smaller
						elif event.unicode.isalpha():
							word_input += event.unicode
						if word_input == current:
							score += 1
							pygame.mixer.Sound.play(correct_sound)
							current = random.choice(bank) # picks another random word and resets, admittedly a chance for repeats
							word_input = ""
		screen.fill(bg_color)
		if start == False: # if user has not selected mode
			mode_text = med_font.render("Select mode:", True, text_color)
			mode_rect = mode_text.get_rect(center = (screen_width//2, screen_height//2 - 400))
			screen.blit(mode_text, mode_rect)
			bh_button.update(pygame.mouse.get_pos())
			lh_button.update(pygame.mouse.get_pos())
			rh_button.update(pygame.mouse.get_pos())
			back_button.update(pygame.mouse.get_pos())
			letter_button.update(pygame.mouse.get_pos())
			word_button.update(pygame.mouse.get_pos())
			if hand and mode: # if the user has selected which hand(s) and whether to practice letters or words, go button pops up
				go_button.update(pygame.mouse.get_pos())
		else:
			if lockout <= 0: # resets the text back from red if lockout has ended/isnt active, otherwise is red
				current_text = large_font.render(current, True, text_color)
			else:
				current_text = large_font.render(current, True, "red")
			current_rect = current_text.get_rect(center = (screen_width//2, screen_height//2))
			screen.blit(current_text, current_rect)
			score_text = med_font.render(f"Score: {score} | Mode: {mode + ", " + hand}", True, text_color)
			score_rect = score_text.get_rect(center = (screen_width//2, screen_height//2 - 300))
			screen.blit(score_text, score_rect)
			back_button.update(pygame.mouse.get_pos())
			if mode == "Words": # to display the user actually typing their word
				input_text = large_font.render(word_input,  True, text_color)
				input_rect = input_text.get_rect(center = (screen_width//2, screen_height//2 + 200))
				screen.blit(input_text, input_rect)
		pygame.display.update()
		clock.tick(60)
def options(): # to customize volume, font, background color, and font color currently
	global text_color, bg_color, current_font, volume, small_font, med_font, large_font
	fcolor_input = "" # the user's inputs for what color/font they want
	bgcolor_input = ""
	font_input = ""
	fcolor_active = False # the flags to see if a user is trying to type something to set a color/font
	bgcolor_active = False
	font_active = False
	fcolor_lockout = 0 # if the user puts an invalid font or color, sets the amount of time the error message is on screen before the user can try again
	bgcolor_lockout = 0
	font_lockout = 0
	while True:
		finput_text = small_font.render(fcolor_input, True, text_color)
		bginput_text = small_font.render(bgcolor_input, True, text_color)
		fontinput_text = small_font.render(font_input, True, text_color)
		finput_width = max(400, finput_text.get_width() + 25) # the max() is so the text box can stretch with what the user types
		bginput_width = max(400, bginput_text.get_width() + 25)
		fontinput_width = max(400, fontinput_text.get_width() + 25)
		box_height = 150 # how tall the text box is
		finput_box = pygame.Rect(screen_width//2 - finput_width//2 + 450, screen_height//2 - box_height//2 - 200, finput_width, box_height)
		bginput_box = pygame.Rect(screen_width//2 - bginput_width//2 + 450, screen_height//2 - box_height//2 + 200, bginput_width, box_height)
		fontinput_box = pygame.Rect(screen_width//2 - fontinput_width//2 - 450, screen_height//2 - box_height//2 + 200, fontinput_width, box_height)
		if fcolor_active == False: # if not currently typing in a text box, is empty
			fcolor_input = ""
		if bgcolor_active == False:
			bgcolor_input = ""
		if font_active == False:
			font_input = ""
		if fcolor_lockout > 0: # to display error messages while lockout is active for if a font or color that the user puts isnt in the pygame libary, ticks down
			fcolor_lockout -= clock.get_time()
			fcolor_input = "Color not found"
		if bgcolor_lockout > 0:
			bgcolor_lockout -= clock.get_time()
			bgcolor_input = "Color not found"
		if font_lockout > 0:
			font_lockout -= clock.get_time()
			font_input = "Font not found"
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if back_button.checkForInput(pygame.mouse.get_pos()):
					menu()
				elif finput_box.collidepoint(event.pos) and fcolor_lockout <= 0: # turns on the text box so the user can type if they click the box
					fcolor_active = True
				elif bginput_box.collidepoint(event.pos) and bgcolor_lockout <= 0:
					bgcolor_active = True
				elif fontinput_box.collidepoint(event.pos) and font_lockout <= 0:
					font_active = True
				else:
					fcolor_active = False
					bgcolor_active = False
					font_active = False
			elif event.type == pygame.KEYDOWN:
				if fcolor_active and len(fcolor_input) <= 15: # a maximum character limit of 15
					if event.key == pygame.K_RETURN: # on hitting enter, the font/color is checked to see if it is in the pygame library
						fcolor_active = False # resets textbox to "not actively typing" state
						if fcolor_input.lower().replace(" ", "") in colors: 
							text_color = fcolor_input.lower().replace(" ", "")
						else:
							fcolor_lockout = 500 # 500 millisecond lockout (roughly)
					elif event.key == pygame.K_BACKSPACE: 
						fcolor_input = fcolor_input[:-1]
					else:
						fcolor_input += event.unicode
				if bgcolor_active and len(bgcolor_input) <= 15: # a maximum character limit of 15
					if event.key == pygame.K_RETURN: # on hitting enter, the font/color is checked to see if it is in the pygame library
						bgcolor_active = False # resets textbox to "not actively typing" state
						if bgcolor_input.lower().replace(" ", "") in colors:
							bg_color = bgcolor_input.lower().replace(" ", "")
						else:
							bgcolor_lockout = 500 # 500 millisecond lockout (roughly)
					elif event.key == pygame.K_BACKSPACE:
						bgcolor_input = bgcolor_input[:-1]
					else:
						bgcolor_input += event.unicode
				if font_active and len(font_input) <= 15: # a maximum character limit of 15
					if event.key == pygame.K_RETURN: # on hitting enter, the font/color is checked to see if it is in the pygame library
						font_active = False # resets textbox to "not actively typing" state
						if font_input.lower().replace(" ", "") in fonts:
							current_font = font_input.lower().replace(" ", "")
							large_font = pygame.font.SysFont(current_font, 120)
							small_font = pygame.font.SysFont(current_font, 85)
							med_font = pygame.font.SysFont(current_font, 100)
						else:
							font_lockout = 500 # 500 millisecond lockout (roughly)
					elif event.key == pygame.K_BACKSPACE:
						font_input = font_input[:-1]
					else:
						font_input += event.unicode
		mouse_pressed = pygame.mouse.get_pressed() # used this one instead of the event checker so you could actually hold down click and slide instead of just clicking
		if mouse_pressed[0]:
			mx, my = pygame.mouse.get_pos() # the mouse x and y positions
			if slider_x <= mx <= slider_x + slider_width and slider_y - 100 <= my <= slider_y + slider_height + 100: # checks if mouse is within the slider rectangle
				handle_x = mx # teleports the handle to the mouse location
				volume = (handle_x - slider_x) / slider_width # calculuates to what percent the handle is down the length of the slider, has a range of 0-1
				switch_volume(volume)
		screen.fill(bg_color)
		pygame.draw.rect(screen, "gray", (slider_x, slider_y, slider_width, slider_height))
		handle_x = int(slider_x + volume * slider_width)
		pygame.draw.rect(screen, text_color, (handle_x - handle_width//2, slider_y-10, handle_width, slider_height+20))
		vol_text = small_font.render("Volume", True, text_color)
		vol_rect = vol_text.get_rect(center = (screen_width//2 - 450, screen_height//2 - 400))
		screen.blit(vol_text, vol_rect)
		back_button.update(pygame.mouse.get_pos())

		fcolor_text = small_font.render("Text Color", True, text_color)
		fcolor_rect = fcolor_text.get_rect(center = (screen_width//2 + 450, screen_height//2 - 400))
		screen.blit(fcolor_text, fcolor_rect)

		bgcolor_text = small_font.render("Background Color", True, text_color)
		bgcolor_rect = bgcolor_text.get_rect(center = (screen_width//2 + 450, screen_height//2))
		screen.blit(bgcolor_text, bgcolor_rect)

		font_text = small_font.render("Font", True, text_color)
		font_rect = font_text.get_rect(center = (screen_width//2 - 450, screen_height//2))
		screen.blit(font_text, font_rect)

		finput_rect = finput_text.get_rect(center = (finput_box.x + finput_width//2, finput_box.y + box_height//2))
		bginput_rect = bginput_text.get_rect(center = (bginput_box.x + bginput_width//2, bginput_box.y + box_height//2))
		fontinput_rect = fontinput_text.get_rect(center = (fontinput_box.x + fontinput_width//2, fontinput_box.y + box_height//2))
		if fcolor_active: # sets the box to dark gray if user is actively typing, else is light gray
			pygame.draw.rect(screen, "darkgray", finput_box)
		else:
			pygame.draw.rect(screen, "lightgray", finput_box)
		if bgcolor_active:
			pygame.draw.rect(screen, "darkgray", bginput_box)
		else:
			pygame.draw.rect(screen, "lightgray", bginput_box)
		if font_active:
			pygame.draw.rect(screen, "darkgray", fontinput_box)
		else:
			pygame.draw.rect(screen, "lightgray", fontinput_box)
		screen.blit(finput_text, finput_rect)
		screen.blit(bginput_text, bginput_rect)
		screen.blit(fontinput_text, fontinput_rect)
		pygame.display.update()
		clock.tick(60)
menu()