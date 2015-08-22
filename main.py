#!/usr/bin/python

# #----------------------------Ubuntu Splash 2.0-----------------------------# #
# ============================================================================ #
# # An MS Paint Clone using a pygame framework with an Ubuntu Desktop Theme  # #
# #                        Paul Krishnamurthy 2015                           # #
# #                            www.paulKr.com                                # #
# # ------------------------------------------------------------------------ # #

# ----Modules---- #
from pygame import *
from tkinter import *
import webbrowser
from datetime import datetime
from random import randrange,randint,choice
from math import hypot,sqrt
from time import sleep
from getpass import getuser as username
from os import environ
from send_email import send
from resources import images,rects
from ButtonEffect import highlight,border
from loading import loading

# Tkinter
try: # Python 2x
	from tkMessageBox import tkMessageBox as messageboxs
	from tkinter.filedialog import askopenfilename as open_file
	from tkinter.filedialog import asksaveasfilename as save_file
	from tkinter.simpledialog import askstring
except: # Python 3x
	from tkinter import messagebox
	from tkinter.filedialog import askopenfilename as open_file
	from tkinter.filedialog import asksaveasfilename as save_file
	from tkinter.simpledialog import askstring

init()
root = Tk()
root.withdraw() # Hide tkinter screen

# Instructions

htext = \
"""
Brush: Hold mouse down to draw
Eraser: Hold mouse down to draw
Pencil: Hold mouse down to draw
Ink: Hold mouse down to draw

Spray: Spray effect when clicked
Flood Fill: Fills area with color
Text: Type to draw text; reuturn to stop

Rectangle: Hold to draw resizable rectangle
Circle: Hold to draw resizable circle
Line: Draw line from one point to another
Polygon: Click for vertices; right-click to close shape

Stamp: Position stamp with mouse; change with key/num pad
Waterbrush: Hold mouse down to draw
Blur: Hold mouse down to draw
Crop: Hold mouse down to select area and click to place it

Undo/Redo: Use CTRL-Z, CTRL-Y or the respective buttons buttons
Save/Load: Use CTRL-S, CTRL-O or the respective buttons buttons
Email: Click on the email button

Important:

Use up/down arrows to switch between layers
Use scroll wheel to change size
Click on a filter to apply to it to that layer
Click on the fill checkbox for shape fill on or off, respectively
Click on the guitar folder to load your music

Have fun! 
(Click the help button on the toolbar to see this message again)
"""

# About

atext = \
'''
ICS3U Paint Project
Ubuntu Splash 2.0
January 2015
Paul K.

www.paulKr.com
'''
#-----------------------------------------------#

# ----Global functions---- 
def rm():
	""" Returns real mouse positions """
	return mouse.get_pos()
def cm():
	""" Returns mouse position on canvas """
	return mouse.get_pos()[0]-80,mouse.get_pos()[1]-45
def lc():
	""" Check left button click """
	return mouse.get_pressed() == (1,0,0)
def rc():
	""" Check right button click """
	return mouse.get_pressed() == (0,0,1)
def randcol():
	""" Returns random color in (r,g,b) format"""
	return (randrange(255),randrange(255),randrange(255))

#-----------------------------------------------#

# ----Setup / Important variables---- #
screen_res = display.Info() # To get current_w and current_h
clock = time.Clock()

# Remove frame and launch at top left corner so that tkinter filedialog opens over the program without minimizing it
environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
screen = display.set_mode((screen_res.current_w, screen_res.current_h), NOFRAME) # Full screen with screen res size

res_x, res_y = screen.get_size() # Store screen size
old = (0,0) # Old x,y positions

color = (0,0,0) # Drawing color
blit_color = (0,0,0) # Color-picker color

cur_tool = "brush" # Current tool
cur_stamp = "stamp1" # Current stamp

size = 10 # Current size
saved = 0 # Number of saved email copies
music_vol = .5 # Loaded music volume = 50%

# Crop tool
cropMove = False # Position area 
cropArea = Rect(0,0,0,0) # Staring cropArea

# Shape fill
fill_check = [images["filled"],images["unfilled"]]
fill_check_num = 0 # Check index at fill_check
filled = True # If rectangle or ellipse is filled

# Fonts
fixedFont = font.Font("fonts/ubuntu.ttf", 17)
drawFont = font.Font("fonts/ubuntu.ttf", size)

# Alpha brush surface + Blur tool surfaces
alpha_brush_surf = Surface((24,24),SRCALPHA)
blur_surf = Surface((24,24),SRCALPHA)
draw.circle(blur_surf,(255,255,255,10),(12,12),12)

def alpha_brush_update():
	""" Updates waterbrush with current color """
	display.update(draw.circle(alpha_brush_surf,(color[0],color[1],color[2],10),(12,12),12))

def about():
	pass
	# Optional about me window
	# Tkinter window interferes with save/load tools
	#root.deiconisy() # Bring window back
	#photo = PhotoImage(file="images/aboutme.gif")
	#label = Label(root, image=photo)
	#label.pack()
	#root.mainloop()

# Layers --> 5 Layers
# Set white to transparent
layer1 = Surface((res_x*.71,res_y*.8))
layer2 = Surface((res_x*.71,res_y*.8))
layer3 = Surface((res_x*.71,res_y*.8))
layer4 = Surface((res_x*.71,res_y*.8))
layer5 = Surface((res_x*.71,res_y*.8))

layers = [layer1,layer2,layer3,layer4,layer5]

for i in range(len(layers)):
	layers[i].fill((255,255,255))

layerIndex = 0 # Current layer

def layer_display():
	""" Blits current layer """
	cp = layers[layerIndex].copy()
	cp.set_colorkey(None) # Transparent to white
	screen.blit(transform.smoothscale(cp,(100,60)),(res_x*.79+41,res_y*.5+10))

# Undo / Redo lists
undo_list = [layers[layerIndex].copy()] 
redo_list = []

#-----------------------------------------------#

# ----Frequently used colors---- #
colors = {
	"white" : (255,255,255),
	"black" : (0,0,0),
	"purple" : (34,5,24),
	"gray" : (80,78,71),
	"gray-text" : (223,219,197),
	"red" : (66,14,14),
	"blended" : (122,87,85),
	"blended2" : (201,105,89),
	"blended3" : (139,99,81)
}

# ----Selected tool info---- #
tools = {
	"btn3" : "brush",
	"btn4" : "eraser",
	"btn5" : "pencil",
	"btn6" : "ink",
	"btn7" : "spray",
	"btn8" : "fill",
	"btn9" : "text",
	"btn10" : "stamp",
	"rect_rect" : "rect",
	"circ_rect" : "circ",
	"line_rect" : "line",
	"poly_rect" : "poly",
	"alpha-brush-rect" : "alpha-brush",
	"blur-rect" : "blur",
	"eyedropper-rect" : "eyedropper",
	"scissors-rect" : "crop",
	"fun_rect" : "fun"
}

#-------------------------------------#
 
# ----Tool class---- #
class Tool:
	""" Non object oriented class to organize tools -> To make code neater """

	def __init__(self):
		pass

class brush(Tool):
	""" Brush / Eraser Tool - Draw circles/rectangles between distance of points """

	def draw(start, end, eraser):
		sx,sy = start[0],start[1]# Start x,y
		ex,ey = end[0],end[1]# End x,y
		dx = ex-sx #Delta x
		dy = ey-sy #Delta y
		# Avoid division by zero
		dist = max(1,int(hypot(sx-ex,sy-ey))) 
		for i in range(dist):
			# x,y coordinates of points to draw circle
			x = int(sx+i/dist*dx)
			y = int(sy+i/dist*dy)
			# Draw circle at each point
			if eraser:
				display.update(draw.rect(layers[layerIndex], colors["white"], ((x-size)-80, (y-size)-45,size*2,size*2)))
			else:
				display.update(draw.circle(layers[layerIndex], color, (x-80, y-45), size))

class pencil(Tool):
	""" Pencil Tool - Draws line with 1px width """

	def draw(start, end, width=1):
		# Draw lines relative to canvas position current last pos to current pos
		display.update(draw.line(layers[layerIndex],color,(start[0]-80,start[1]-45),(end[0]-80,end[1]-45)))

class ink(Tool):
	""" Ink tool - Imitates ink pen """

	# Similar structure to brush/eraser
	def draw(start, end):
		sx,sy = start[0],start[1]# Start x,y
		ex,ey = end[0],end[1]# End x,y
		dx = ex-sx #Delta x
		dy = ey-sy #Delta y
		dist = int(hypot(sx-ex,sy-ey))
		for i in range(dist):
			# x,y coordinates of points to draw circle
			x = int(sx+i/dist*dx)
			y = int(sy+i/dist*dy)
			# # Avoid division by 0 + Set "max" limit --> Make radius proportionate to distance
			radius = int(max(size/10,size*3-dist) ** .6) 
			display.update(draw.circle(layers[layerIndex], color, (x-80, y-45), radius))

class spray(Tool):
	""" Spray Tool - Spray effect when pressed """

	def draw():
		for i in range(size*4): # Speed
			# Random coordinate in size X size rect
			x = randint(-size,size)
			y = randint(-size,size)
			# Check distance for circle
			if hypot(x,y) <= size:
				display.update(layers[layerIndex].set_at((cm()[0]+x, cm()[1]+y),color))

		# [[[screen.set_at((rm()[0]+x, rm()[1]+y),color) if hypot(x,y)<=size else None] \
		# for x,y in [(randint(-size,size),randint(-size,size))]] for i in range(size*4)]

class flood(Tool):
	""" Fill Tool - Fills given area with specific color """

	def draw(pos,color):
		# Flood fill algorithm
		points = set() # No duplicate points
		points.add((pos))
		replace = layers[layerIndex].get_at((pos))
		if color != replace:
			while len(points) > 0: # There should be points to check
				x,y = points.pop() # Check coordinate (last in list)
				try: # Avoid pixel index out of range
					check = layers[layerIndex].get_at((x,y))
					if check == replace:
						layers[layerIndex].set_at((x,y),color) # Set pixel with new color
						points.add((x+1,y)) # Right
						points.add((x-1,y)) # Left
						points.add((x,y+1)) # Down
						points.add((x,y-1)) # Up
				except:
					pass

class text(Tool):
	""" Text Tool - Allows user to type """

	def draw():
		global drawFont
		text = "" # Text
		type_on = True
		draw.rect(layers[layerIndex],colors["black"],(cm()[0],cm()[1],100,size+10),1)
		while type_on:
			for e in event.get():
				if e.type == KEYDOWN:
					if e.key == K_BACKSPACE:
						# Delete last letter
						text = text[:-1]
					if e.key < 256:
						text += e.unicode # Add character to text
					# Check return and numpad enter
					if e.key == K_RETURN or e.key == K_KP_ENTER:
						# Blits fonts when enter is pressed
						type_on = False

			# For fixed text: 
			#layers[layerIndex].blit(drawFont.render(text, 1, (color)),start)

			# For movable text
				display.flip()
				layers[layerIndex].blit(drawFont.render(text, 1, (color)),cm())
				layers[layerIndex].blit(cover,(0,0))
						
			# Blit fixed text
			layers[layerIndex].blit(drawFont.render(text, 1, (color)),cm())


class rectangle(Tool):
	""" Rectangle tool - Draws rectangle based on given points """
 
	def draw(start, end, fill):
		layers[layerIndex] = cover.copy()
		sx,sy = start # First x,y
		ex,ey = end # End x,y
		sx -= 80
		ex -= 80
		sy -= 45
		ey -= 45
		half = size//2 # Half of the size to fix squared corners
		# Fill depending on flag
		if fill:
			display.update(draw.rect(layers[layerIndex],color,(min(sx,ex),min(sy,ey),abs(sx-ex),abs(sy-ey)))) # Filled
		else:
			# Positive rectangle
			if (ex - sx) >= 0:
				# Half-1 for accurate positioning
				display.update(draw.line(layers[layerIndex],color,(sx-(half-1),sy),(ex+(half),sy),size))
				display.update(draw.line(layers[layerIndex],color,(sx,sy),(sx,ey),size))
				display.update(draw.line(layers[layerIndex],color,(ex,ey),(ex,sy),size))
				display.update(draw.line(layers[layerIndex],color,(sx-(half-1),ey),(ex+(half),ey),size))

			# Negative rectangle
			elif (ex - sx) < 0:
				# Half-1 for accurate positioning
				display.update(draw.line(layers[layerIndex],color,(ex-(half-1),ey),(sx+(half),ey),size))
				display.update(draw.line(layers[layerIndex],color,(ex,ey),(ex,sy),size))
				display.update(draw.line(layers[layerIndex],color,(sx,sy),(sx,ey),size))
				display.update(draw.line(layers[layerIndex],color,(ex-(half-1),sy),(sx+(half),sy),size))


class ellipse(Tool):
	""" Ellipse tool - Draws ellipse based on given points / radius """

	def draw(start, end, fill):
		# Similar to rectangle tool
		layers[layerIndex] = cover.copy()
		sx,sy = start # First x,y
		ex,ey = end # End x,y
		diameter = size*2
		# Fill depending on flag
		if fill:
			display.update(draw.ellipse(layers[layerIndex],color,(min(sx,ex)-80,min(sy,ey)-45,abs(sx-ex),abs(sy-ey)))) # Filled
		else:
			try: # So width will not be greater than radius
				if diameter >= min(abs(sx-ex),abs(sy-ey)): # Check if there is a hole in the ellipse
					display.update(draw.ellipse(layers[layerIndex],color,(min(sx,ex)-80,min(sy,ey)-45,abs(sx-ex),abs(sy-ey))))
				else:
					# Draws 360 degree arc to fix glitchy circle
					display.update(draw.arc(layers[layerIndex],color,(min(sx,ex)-80,min(sy,ey)-45,abs(sx-ex),abs(sy-ey)),0,360,size))
			except:
				pass

class line(Tool):
	""" Line tool - Draws line from start to end of given points """

	def draw(start, end):
		layers[layerIndex] = cover.copy()
		# Similar to brush and eraser for smooth line
		sx,sy = start[0],start[1]# Start x,y
		ex,ey = end[0],end[1]# End x,y
		dx = ex-sx #Delta x
		dy = ey-sy #Delta y
		# Avoid division by zero
		dist = max(1,int(hypot(sx-ex,sy-ey))) 
		for i in range(dist):
			# x,y coordinates of points to draw ellipse
			x = int(sx+i/dist*dx)
			y = int(sy+i/dist*dy)
			# Draw ellipse at each point
			display.update(draw.circle(layers[layerIndex], color, (x-80, y-45), min(size//2+1,30)))

class poly(Tool):
	""" Polygon tool - Draws a polygon based on given points """

	def draw(filled,points=[]):
		# Do not append last point
		copy = layers[layerIndex].copy()
		if clicked and not rc() and rects["canvas"].collidepoint(rm()):
			points.append(cm()) # Append points to list
			display.update(draw.circle(layers[layerIndex],color,cm(),2)) # Indicate vertex
		if rc():
			# Connect points to draw polygon if there are more than 2 points
			if len(points)>2: 
				if filled:
					display.update(draw.polygon(layers[layerIndex],color,points))
				else:
					display.update(draw.polygon(layers[layerIndex],color,points,2))
				del points[:] # Delete old points

class stamp(Tool):
	"""" Stamp Tool - Blits selected image at given point """
	# Get the current stamp
	def get():
		global cur_stamp
		k = key.get_pressed()
		# Allow num pad or number
		if k[K_0] or k[K_KP0]: cur_stamp = "stamp1"
		if k[K_1] or k[K_KP1]: cur_stamp = "stamp2"
		if k[K_2] or k[K_KP2]: cur_stamp = "stamp3"
		if k[K_3] or k[K_KP3]: cur_stamp = "stamp4"
		if k[K_4] or k[K_KP4]: cur_stamp = "stamp5"
		if k[K_5] or k[K_KP5]: cur_stamp = "stamp6"
		if k[K_6] or k[K_KP6]: cur_stamp = "stamp7"
		if k[K_7] or k[K_KP7]: cur_stamp = "stamp8"
		if k[K_8] or k[K_KP8]: cur_stamp = "stamp9"
		if k[K_9] or k[K_KP9]: cur_stamp = "stamp10"

	def draw(x,y,image):
		w,h = image.get_size() # Get width and height
		# Allow draggable stamping
		layers[layerIndex] = cover.copy()
		# Mouse position centered on image
		display.update(layers[layerIndex].blit(image,((x-w/2) - 80,(y-h/2) - 45)))

		# Allows size-adjustable stamps 
		# Resolution of image is lost in the process
		# display.update(layers[layerIndex].blit(transform.scale(image,(w+size*3,h+size*3)),((x-w/2) - 80,(y-h/2) - 45)))


	def crop(x,y,image):
		# For crop tool -> Positioning differs than stamps
		layers[layerIndex] = cover.copy()
		display.update(layers[layerIndex].blit(image,(x - 80,y - 45)))

class alpha_tool(Tool):
	""" Alpha Brush Tool - Gives watercolor brush effect """
	""" Blur Tool - A mix of the alpha brush and photoshop blur tool """

	def draw(start, end, blur_on):
		sx,sy = start[0],start[1]# Start x,y
		ex,ey = end[0],end[1]# End x,y
		dx = ex-sx #Delta x
		dy = ey-sy #Delta y
		# Avoid division by zero
		dist = max(1,int(hypot(sx-ex,sy-ey))) 
		for i in range(dist):
			# x,y coordinates of points to draw circle
			x = int(sx+i/dist*dx)
			y = int(sy+i/dist*dy)
			# Draw circle at each point
			if rm()[0] != old[0] or rm()[1] != old[1]:
				if blur_on:
					display.update(layers[layerIndex].blit(blur_surf,((x-12)-80,(y-12)-45)))
				else:
					display.update(layers[layerIndex].blit(alpha_brush_surf,((x-12)-80,(y-12)-45)))

class crop(Tool):
	""" Crop Tool - Cuts and allows reposition of area selected"""

	def crop(start,end):
		global cropMove,cropArea
		# Select are
		if lc() and rects["canvas"].collidepoint(rm()):
			sx,sy = start
			ex,ey = rm()
			layers[layerIndex] = cover.copy()
			cropArea = Rect(min(sx,ex)-80,min(sy,ey)-45,abs(sx-ex),abs(sy-ey))
			cropArea.normalize()

		# Place the selected area
		if cropMove:
			layers[layerIndex] = cover.copy()
			cropMove = False
			# Avoid surface area errors
			try:cropPic = layers[layerIndex].subsurface(cropArea).copy()
			except:pass
			# Draw white rectangle and blit selected area
			stamp.crop(rm()[0],rm()[1],cropPic)
			draw.rect(layers[layerIndex],colors["white"],cropArea)
			draw.rect(layers[layerIndex],colors["black"],cropArea,1)
			layers[layerIndex].blit(cropPic,(cm()))

class fun(Tool):
	""" Fun tool - A hidden easter egg tool """

	def draw(start, end):
		sx,sy = start[0],start[1]# Start x,y
		ex,ey = end[0],end[1]# End x,y
		dx = ex-sx #Delta x
		dy = ey-sy #Delta y
		# Avoid division by zero
		dist = max(1,int(hypot(sx-ex,sy-ey))) 
		for i in range(dist):
			# x,y coordinates of points to draw circle
			x = int(sx+i/dist*dx) - 80
			y = int(sy+i/dist*dy) - 45
			# Draw circle at each point
			for i in range(5): # Less lag
				x2 = x + randint(-50,50)
				y2 = y + randint(-50,50)
				if sqrt((x2-x)**2+(y2-y)**2) <= 50: # Circular
					display.update(draw.line(layers[layerIndex],randcol(),(x,y),(x2,y2)))
				
class save_img(Tool):
	""" Save tool - Saves canvas """

	def draw():
		copy = screen.subsurface(rects["canvas"]).copy() # Copy canvas
		name = save_file(parent=root)
		if len(name) != 0: # Check if name is blank 
			image.save(copy,"%s.png"%name) # Save as png image

class open_img(Tool):
	""" Open Tool - Opens local image """

	def draw():
		name = open_file(parent=root)
		if len(name) != 0: # Check if name is blank
			load = image.load(name)
			layers[layerIndex].blit(load,(0,0))
			undo_list.append(layers[layerIndex].copy())

class song(Tool):
	""" All music options """

	def load():
		name = open_file(parent=root) # Load music from local directory
		if len(name) != 0:
			song = mixer.music.load(name)
			mixer.music.play(loops=100)

	def play():
		mixer.music.unpause()

	def pause():
		mixer.music.pause()

	def v_up():
		mixer.music.set_volume(min(1,music_vol+.1))

	def v_down():
		mixer.music.set_volume(max(.1,music_vol-.1))

class email(Tool):
	""" Send email of canvas """

	def set():
		user_email = askstring("Email", "Enter your email :")
		try:
			if len(user_email) > 2 and user_email.count("@") == 1 and user_email.count(".") >= 1: # Send if it is a valid email address
				image.save(screen.subsurface(rects["canvas"]),"local/saves/email%d.png"%saved)
				send(user_email, "Your masterpiece is ready!", "Thanks for using Ubuntu Splash 2.0", "email%d.png"%saved)
				messagebox.showinfo(title="Email Sent", message="Email sent successfully!\nEvent logged to file.")
			else:
				f = open("local/events.log","a") # Log to events file without overwrite
				f.write("Invalid email entered. Email not sent \n")
				f.close()
		except:
			messagebox.showinfo(title="Email Not Sent", message="Email not sent successfully!\nEvent logged to file.")

class filter_tool(Tool):
	""" Applies filter to layer """

	def bw(layer):
		# Greyscale algorithm
		# r,g,b = average of the pixel color
		for x in range(int(res_x*.71)):
			for y in range(int(res_y*.8)):
				check = layer.get_at((x,y))[:3] # Only rgb
				r,g,b = map(int,check)
				average = sum([r,g,b])//3 # Average pixel color
				layer.set_at((x,y),tuple([average]*3)) # Set pixel
				undo_list.append(layers[layerIndex].copy())

	def sephia(layer):
		# Sephia tone algorithm
		# outputRed = (inputRed * .393) + (inputGreen *.769) + (inputBlue * .189)
		# outputGreen = (inputRed * .349) + (inputGreen *.686) + (inputBlue * .168)
		# outputBlue = (inputRed * .272) + (inputGreen *.534) + (inputBlue * .131)
		for x in range(int(res_x*.71)):
			for y in range(int(res_y*.8)):
				check = layer.get_at((x,y))[:3] # Only rgb
				r,g,b = map(int,check)
				outr = (r*.393) + (g*.769) + (b*.189)
				if outr > 255: outr = 255
				outg = (r*.349) + (g*.686) + (b*.168)
				if outg > 255: outg = 255
				outb = (r*.272) + (g*.534) + (b*.131)
				if outb > 255: outb = 255
				layer.set_at((x,y),(outr,outg,outb))
		undo_list.append(layers[layerIndex].copy())

	def negative(layer):
		# Inverts colors
		# 255 -  color
		for x in range(int(res_x*.71)):
			for y in range(int(res_y*.8)):
				check = layer.get_at((x,y))[:3] # Only rgb
				r,g,b = map(int,check)
				r = 255 - r
				g = 255 - g
				b = 255 - b
				layer.set_at((x,y),(r,g,b))
		undo_list.append(layers[layerIndex].copy())

	def blur(layer):
		# Adds blur effect to current layer
		mini = transform.smoothscale(layer,(int(res_x*.71/4),int(res_y*.8/4))) # Resize to small image
		layer.blit(transform.smoothscale(mini,(int(res_x*.71),int(res_y*.8))),(0,0)) # Resize mini to large fit surface
		undo_list.append(layers[layerIndex].copy())

	def tint(layer):
		# Adds transparent layer over current layer
		t = layer.copy() 
		t.fill(color)
		t.set_alpha(40) # 40 Opacity
		layer.blit(t,(0,0))
		undo_list.append(layers[layerIndex].copy())

	def fill_screen(layer):
		# Fills layer with selected color
		layer.fill((color))
		undo_list.append(layers[layerIndex].copy())

# ----Main Display---- #
def main():
	""" Main homepage """
	screen.blit(transform.scale(images["wallpaper"], (res_x,res_y)),(0,0))# Ubuntu wallpaper
	# Alpha border for canvas
	canvas_border = Surface((res_x*.71+24,res_y*.8+24),SRCALPHA)
	canvas_border.fill((255,255,255,128)) # Add alpha (128)
	# Icon holding surface
	icon_holder = Surface((70,res_y),SRCALPHA)
	icon_holder.fill((66,14,14,100)) # Add alpha (128)
	# Blit onto screen_res
	screen.blit(icon_holder,(0,25))
	screen.blit(canvas_border,(70,34))
	draw.rect(screen,colors["white"],rects["canvas"]) # Drawing canvas
	# Tansparent "Info Dock"
	dock = Surface((res_x*.71,(res_y-res_y*.8)-75),SRCALPHA)
	dock.fill((80,78,71,160))
	screen.blit(dock,(80,res_y*.8+65))
	# Transparent overlay
	overlay = Surface((res_x,res_y*.42),SRCALPHA)
	overlay.fill((80,78,71,160))
	screen.blit(overlay,(res_x*.71+100,50))
	# Blit images
	screen.blit(images["display-view"],(res_x*.79,res_y*.5-19))
	screen.blit(images["load-song"],(800,res_y*.8+70))
	screen.blit(images["play"],(840,res_y*.8+70))
	screen.blit(images["pause"],(890,res_y*.8+70))
	screen.blit(images["v-up"],(840,res_y*.8+112))
	screen.blit(images["v-down"],(800,res_y*.8+112))
	screen.blit(images["about"],(res_x*.83,res_y*.3))
	screen.blit(images["homepage"],(res_x*.83+90,res_y*.3))

	# Filters
	f = ["bw","sephia","negative","blur_filter","tint","fill_screen"]
	for i in range(len(f)):
		screen.blit(images[f[i]],(95+100*i,res_y*.8+75))

def toolbar(colora,colorb):
	""" Ubuntu themed toolbar -> Constantly updated""" 
	screen.blit(transform.scale(images["toolbar"], (res_x,30)),(0,0))
	# Ubuntu Info/Deco --> Proportionate to screen resolution
	screen.blit(fixedFont.render("Ubuntu Desktop - Splash 2.0  |  Help", 1, (colorb)),[5,5])
	screen.blit(images["toolbar-apps"],(res_x-300,2))
	# Blit real time onto screen
	screen.blit(fixedFont.render(datetime.now().strftime('%I:%M:%S %p'), 1, (colorb)),[res_x-150,4])
	# Username + Mouse position relative to canvas
	if rects["canvas"].collidepoint(rm()):
		screen.blit(fixedFont.render("Welcome %s  |  X:%d  Y:%d  |  FPS: %d"%(
			username(),cm()[0],cm()[1],round(clock.get_fps())), 1, (colorb)),[res_x*.38,3])
	else:
		screen.blit(fixedFont.render("Welcome %s  |  %s  |  FPS: %d"%(
			username(),"Not on Canvas",round(clock.get_fps())), 1, (colorb)),[res_x*.38,3])

def color_update():
	# Info
	draw.rect(screen,colors["blended3"],rects["color-deco"])
	# Current color
	screen.blit(fixedFont.render("Current Color",1,colors["gray-text"]),[res_x*.8,res_y-99])
	# RGB Format
	screen.blit(fixedFont.render(str(color[:3]),1,colors["gray-text"]),[res_x*.85,res_y-75])
	# Hex Format
	screen.blit(fixedFont.render("#%02x%02x%02x"%color[:3],1,colors["gray-text"]),[res_x*.85,res_y-50])
	# The visuals
	draw.rect(screen,blit_color,rects["color-picker"]) # Specific shades
	draw.rect(screen,color,rects["current-color"])
	screen.blit(images["color-picker"],(res_x*.8,res_y-300)) # Color picker
	screen.blit(images["hue-bar"],(res_x*.8+200,res_y-300)) # Hue bar

def info_update():
	""" Constantly updated info """
	draw.rect(screen,colors["blended"],rects["var_back"])
	screen.blit(fixedFont.render("Size: %d"%size,1,colors["gray-text"]),[690,res_y*.8+94]) # Size
	screen.blit(fixedFont.render("Layer: %d/5"%(layerIndex+1),1,colors["gray-text"]),[690,res_y*.8+119]) # Layer

def fill_update():
	""" Update fill image only when needed """
	screen.blit(fill_check[fill_check_num],(690,res_y*.8+70)) # Draw fill on or off

# ----Loading display---- #

# White screen
background = Surface((screen.get_rect().width, screen.get_rect().height))
background.fill((255,255,255))
alpha = 255 # Alpha value
check_flash = True # To check if program if fading

# Ubuntu login sound
mixer.music.load("sound/startup.mp3")
mixer.music.play()
time.delay(500)

for i in range(0,30):
	display.update(screen.blit(loading[str(i)],(0,0)))
	sleep(.1) # Delay between frames
final = transform.scale(image.load("images/loading/Frame30.png").convert(),(res_x,res_y))
fade_in_pic = final.get_rect()

while check_flash:
	# Powerful introduction
	alpha -= 2.5
	if alpha == 0:
		check_flash = False
		# Call startup functions
		main()
		color_update()
		fill_update()
		info_update()
		border(cur_tool)
		highlight(rm(),lc(),cur_tool)
		alpha_brush_update()

	if check_flash:
		final.set_alpha(alpha)
		screen.blit(background, background.get_rect())
		screen.blit(final, fade_in_pic)
		time.delay(10) 
	display.flip()


running = True # Game loop flag
startH = True # Flag for messagebox to show after screen has loaded
rightControl = False
leftControl = False
while running:
	# Event flags
	clicked = False
	undoKey = False
	redoKey = False
	saveKey = False
	loadKey = False

	# Functions that need constant updates
	color_update()
	alpha_brush_update()
	layer_display()
	if not rects["canvas"].collidepoint(rm()): # Only draw when needed
		border(cur_tool) # Checks to draw border around selected tool icons
		highlight(rm(),lc(),cur_tool) # Checks to highlight tool icons
	toolbar(colors["gray"],colors["gray-text"]) # Draw toolbar

	for e in event.get():
		# Increase/Decrease layers based on up/down arrow keys
		if e.type == KEYDOWN and not lc():
			if e.key == K_UP:
				# Add layer (Max of 4)
				layerIndex += 1 if layerIndex < 4 else 0
				info_update()
			elif e.key == K_DOWN:
				# Subtract layer
				layerIndex -= 1 if layerIndex > 0 else 0
				info_update()
			# Shorcuts
			if e.key == K_RCTRL: 
				rightControl = True
			if e.key == K_LCTRL: 
				leftControl = True
			if rightControl or leftControl:
				if e.key == K_z:
					undoKey = True
				if e.key == K_y:
					redoKey = True
				if e.key == K_s:
					saveKey = True
				if e.key == K_o:
					loadKey = True
		# Right/left control key flags
		if e.type == KEYUP:
			if e.key == K_RCTRL:
				rightControl = False
			if e.key == K_LCTRL:
				leftControl = False	
		
		if e.type == MOUSEBUTTONDOWN:
			if e.button != 4 and e.button != 5: # Do not copy when scrolling
				cover = layers[layerIndex].copy()  # Copy only layer
			clicked = True # Constantly check for a click
			start = rm() # Starting position for shapes
			if e.button == 4:
				size = min(max(1,size+1),50) # Minimum size = 1, maximum size 50
				info_update()
				drawFont = font.Font("fonts/ubuntu.ttf", size) # Update fonts
			elif e.button == 5:
				size = max(1,size-1) # Minimum size = 1
				info_update()
				drawFont = font.Font("fonts/ubuntu.ttf", size) # Update fonts

		# Append copy to undo list
		if e.type == MOUSEBUTTONUP and rects["canvas"].collidepoint(rm()) and e.button != 4 and e.button != 5:
			undo_list.append(layers[layerIndex].copy())


	# Exit confirmation
	if rects["exit"].collidepoint(rm()) and not lc():
		screen.blit(images["exit-hover"],(res_x-26,0)) # Exit hover
	else:
		screen.blit(images["exit"],(res_x-26,1)) # Exit normal

	if rects["exit"].collidepoint(rm()) and clicked:
		if messagebox.askyesno("Exit", "Do you finally plan on being productive?"):
			if messagebox.askyesno("Save", "Would you at least like to save?"):
				save_img.draw()
			running = False


	# Filled / Unfilled Shapes
	if rects["fill_rect"].collidepoint(rm()) and clicked:
		fill_check_num = (fill_check_num + 1) % 2 # Sets 0 or 1 as value

	filled = True if not fill_check_num else False # Shape flag based fill_check_num value

	fill_update() # Update fill image

	# Allow user to select color from hue bar + color picker
	if rects["hue-bar"].collidepoint(rm()) and lc():
		color = screen.get_at((rm()))
		blit_color = color
	if rects["color-picker"].collidepoint(rm()) and lc():
		color = screen.get_at((rm()))

	# Check for selected tool
	for r,t in tools.items():
		if rects[r].collidepoint(rm()):
			if clicked:
				cur_tool = t # Set current tool

	if rects["btn1"].collidepoint(rm()) and clicked:
		about()

	if rects["delete"].collidepoint(rm()) and clicked:
		layers[layerIndex].fill((255,255,255))

	# Save
	if (rects["save_but"].collidepoint(rm()) and clicked) or saveKey:
		save_img.draw()
	# Load
	if (rects["open_but"].collidepoint(rm()) and clicked) or loadKey:
		open_img.draw()

	# Undo/Redo work best when working on current single layer

	# Undo 
	if (rects["undo_rect"].collidepoint(rm()) and clicked) or undoKey:
		if len(undo_list) > 1:
			redo_list.append(undo_list.pop())
			try:
				layers[layerIndex].blit(undo_list[-1],(0,0))
			except:
				pass
	# Redo
	if (rects["redo_rect"].collidepoint(rm()) and clicked) or redoKey:
		if len(redo_list) > 0:
			layers[layerIndex].blit(redo_list[-1],(0,0))
			undo_list.append(redo_list.pop())

	# Email
	if rects["email_but"].collidepoint(rm()) and clicked:
		email.set()

	# Help info
	if rects["about_rect"].collidepoint(rm()) and clicked:
		messagebox.showinfo(title="About", message=atext)

	# Advertise
	if rects["homepage_rect"].collidepoint(rm()) and clicked:
		try:
			webbrowser.open("www.paulkr.com")
		except:
			pass

	# Instructions
	if rects["help"].collidepoint(rm()) and clicked:
		messagebox.showinfo(title="Help", message=htext)

	# Music
	if rects["load_song_rect"].collidepoint(rm()) and clicked:
		song.load()
	if rects["play_rect"].collidepoint(rm()) and clicked:
		song.play()
	if rects["pause_rect"].collidepoint(rm()) and clicked:
		song.pause()
	if rects["v_up_rect"].collidepoint(rm()) and clicked:
		song.v_up()
	if rects["v_down_rect"].collidepoint(rm()) and clicked:
		song.v_down()

	# Change crop flag
	cropMove = False if cropMove else cropMove
	if cur_tool == "crop" and rects["canvas"].collidepoint(rm()) and not cropMove:
		cropMove = True

	# Tool collision
	if rects["canvas"].collidepoint(rm()) and lc(): 
		screen.set_clip(rects["canvas"]) # Clip canvas
		if cur_tool == "brush":
			brush.draw(rm(),old,False) # Current color
		elif cur_tool == "eraser":
			brush.draw(rm(),old,True)
		elif cur_tool == "pencil":
			pencil.draw(rm(),old)
		elif cur_tool == "ink":
			ink.draw(rm(),old)
		elif cur_tool == "spray":
			spray.draw()
		elif cur_tool == "fill":
			flood.draw(cm(),color)
		elif cur_tool == "text":
			text.draw()
		elif cur_tool == "stamp":
			stamp.draw(rm()[0],rm()[1],images[cur_stamp])
		elif cur_tool == "alpha-brush":
			alpha_tool.draw(rm(),old,False)
		elif cur_tool == "blur":
			alpha_tool.draw(rm(),old,True)
		elif cur_tool == "eyedropper":
			# Eyedropper tool - Gets color of selected coordinate
			color = layers[layerIndex].get_at((cm()))
			blit_color = color
		elif cur_tool == "rect":
			rectangle.draw(start,rm(),filled)
		elif cur_tool == "circ":
			ellipse.draw(start,rm(),filled)
		elif cur_tool == "line":
			line.draw(start, rm())
		elif cur_tool == "fun":
			fun.draw(rm(),old)

		screen.set_clip(None)

	# Tools that require special mouse actions (not like other tools)
	if cur_tool == "poly":
		screen.set_clip(rects["canvas"])
		poly.draw(filled)
		screen.set_clip(None)

	if cur_tool == "crop":
		screen.set_clip(rects["canvas"])
		crop.crop(start,rm())
		screen.set_clip(None)

	if cur_tool == "stamp":
		stamp.get()

	# Filters
	if rects["bw_rect"].collidepoint(rm()) and clicked: filter_tool.bw(layers[layerIndex])
	elif rects["sephia_rect"].collidepoint(rm()) and clicked: filter_tool.sephia(layers[layerIndex])
	elif rects["negative_rect"].collidepoint(rm()) and clicked: filter_tool.negative(layers[layerIndex])
	elif rects["blur_rect"].collidepoint(rm()) and clicked: filter_tool.blur(layers[layerIndex])
	elif rects["tint_rect"].collidepoint(rm()) and clicked: filter_tool.tint(layers[layerIndex])
	elif rects["fill_screen_rect"].collidepoint(rm()) and clicked: filter_tool.fill_screen(layers[layerIndex])


	if rects["canvas"].collidepoint(rm()):
		old = rm() # Set old positions to current positions

	for i in range(len(layers)):
		# Color key of layers[0] = None and others are transparent
		layers[0].set_colorkey(None) if i == 0 else layers[i].set_colorkey((255,255,255))
		screen.blit(layers[i], (80,45))	

	clock.tick() # FPS
	display.flip()

	if startH:
		messagebox.showinfo(title="Help", message=htext) # Show instructions on startup
	startH = False
quit()
