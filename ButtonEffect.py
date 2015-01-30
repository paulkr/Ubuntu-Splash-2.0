# #----------------------------Ubuntu Splash 2.0-----------------------------# #
# ============================================================================ #
# # An MS Paint Clone using a pygame framework with an Ubuntu Desktop Theme  # #
# #                        Paul Krishnamurthy 2015                           # #
# #                            Button Effects                                # #
# # ------------------------------------------------------------------------ # #

from pygame import *
from resources import images,rects

init()
screen_res = display.Info()
screen = display.set_mode((screen_res.current_w, screen_res.current_h),FULLSCREEN)
res_x, res_y = screen.get_size()

def fresh():
	""" Draw fresh screen for selected tools """
	
	# Cleaner way + Gives a fade effect for tool highlight
	icon_holder = Surface((70,res_y),SRCALPHA)
	icon_holder.fill((66,14,14,100)) # Add alpha (128)
	# Blit onto screen_res
	screen.blit(icon_holder,(0,25))
	
	# Blit copy of icons
	# Partial transparency looks bad on larger screen resolutions
	# screen.blit(images["clean"],(0,15))


def highlight(pos,left,tool):
	""" Blits icon based on mouse action """

	if rects["btn1"].collidepoint(pos) and not left:
		screen.blit(images["btn1-hover"],(7,40))
	else:
		screen.blit(images["btn1"],(7,40))

	if rects["btn2"].collidepoint(pos) and not left:
		screen.blit(images["btn2-hover"],(7,110))
	else:
		screen.blit(images["btn2"],(7,110))

	if rects["btn3"].collidepoint(pos) and not left:
		screen.blit(images	["btn3-hover"],(7,180))
	else:
		screen.blit(images["btn3"],(7,180))

	if rects["btn4"].collidepoint(pos) and not left:
		screen.blit(images["btn4-hover"],(3,250))
	else:
		screen.blit(images["btn4"],(3,250))

	if rects["btn5"].collidepoint(pos) and not left:
		screen.blit(images["btn5-hover"],(7,300))
	else:
		screen.blit(images["btn5"],(7,300))

	if rects["btn6"].collidepoint(pos) and not left:
		screen.blit(images["btn6-hover"],(7,370))
	else:
		screen.blit(images["btn6"],(7,370))

	if rects["btn7"].collidepoint(pos) and not left:
		screen.blit(images["btn7-hover"],(7,440))
	else:
		screen.blit(images["btn7"],(7,440))

	if rects["btn8"].collidepoint(pos) and not left:
		screen.blit(images["btn8-hover"],(3,500))
	else:
		screen.blit(images["btn8"],(3,500))

	if rects["btn9"].collidepoint(pos) and not left:
		screen.blit(images["btn9-hover"],(7,580))
	else:
		screen.blit(images["btn9"],(7,580))

	if rects["btn10"].collidepoint(pos) and not left:
		screen.blit(images["btn10-hover"],(7,650))
	else:
		screen.blit(images["btn10"],(7,650))
		
	# Save Button
	if rects["save_but"].collidepoint(pos) and not left:
		screen.blit(images["save-hover"],(res_x*.8,60))
	else:
		screen.blit(images["save"],(res_x*.8,60))
	
	# Open Button
	if rects["open_but"].collidepoint(pos) and not left:
		screen.blit(images["open-hover"],(res_x*.87,60))
	else:
		screen.blit(images["open"],(res_x*.87,60))

	# Email Button
	if rects["email_but"].collidepoint(pos) and not left:
		screen.blit(images["email-hover"],(res_x*.94,60))
	else:
		screen.blit(images["email"],(res_x*.94,60))

	# 4 extra tools
	if rects["alpha-brush-rect"].collidepoint(pos) or tool == "alpha-brush":
		screen.blit(images["alpha-brush-hover"],(res_x*.79,res_y*.2))
	else:
		screen.blit(images["alpha-brush"],(res_x*.79,res_y*.2))

	if rects["blur-rect"].collidepoint(pos) or tool == "blur":
		screen.blit(images["blur-hover"],(res_x*.84,res_y*.2))
	else:
		screen.blit(images["blur"],(res_x*.84,res_y*.2))

	if rects["eyedropper-rect"].collidepoint(pos) or tool == "eyedropper":
		screen.blit(images["eyedropper-hover"],(res_x*.89,res_y*.2))
	else:
		screen.blit(images["eyedropper"],(res_x*.89,res_y*.2))

	if rects["scissors-rect"].collidepoint(pos) or tool == "crop":
		screen.blit(images["scissors-hover"],(res_x*.94,res_y*.2))
	else:
		screen.blit(images["scissors"],(res_x*.94,res_y*.2))	

	if rects["fun_rect"].collidepoint(pos) or tool == "fun":
		screen.blit(images["fun-hover"],(res_x*.87,res_y*.4))
	else:
		screen.blit(images["fun"],(res_x*.87,res_y*.4))

	""" Shapes """ 
	# Rectangle tool
	if rects["rect_rect"].collidepoint(pos) and tool != "rect":
		screen.blit(images["rect-hover"],(res_x*.79+170,res_y*.5-19))
	elif tool == "rect":
		screen.blit(images["rect-pressed"],(res_x*.79+170,res_y*.5-19))
	else:
		screen.blit(images["rect"],(res_x*.79+170,res_y*.5-19))
	
	# Circle tool
	if rects["circ_rect"].collidepoint(pos) and tool != "circ":
		screen.blit(images["circ-hover"],(res_x*.79+216,res_y*.5-19))
	elif tool == "circ":
		screen.blit(images["circ-pressed"],(res_x*.79+216,res_y*.5-19))
	else:
		screen.blit(images["circ"],(res_x*.79+216,res_y*.5-19))
	
	# Line tool
	if rects["line_rect"].collidepoint(pos) and tool != "line":
		screen.blit(images["line-hover"],(res_x*.79+170,res_y*.5+42))
	elif tool == "line":
		screen.blit(images["line-pressed"],(res_x*.79+170,res_y*.5+42))
	else:
		screen.blit(images["line"],(res_x*.79+170,res_y*.5+42))
	
	# Polygon tool
	if rects["poly_rect"].collidepoint(pos) and tool != "poly":
		screen.blit(images["poly-hover"],(res_x*.79+216,res_y*.5+42))
	elif tool == "poly":
		screen.blit(images["poly-pressed"],(res_x*.79+216,res_y*.5+42))
	else:
		screen.blit(images["poly"],(res_x*.79+216,res_y*.5+42))

	if rects["undo_rect"].collidepoint(pos) and not left:
		screen.blit(images["undo-hover"],(res_x*.73,res_y*.8+69))
	else:
		screen.blit(images["undo"],(res_x*.73,res_y*.8+69))	
	
	if rects["redo_rect"].collidepoint(pos) and not left:
		screen.blit(images["redo-hover"],(res_x*.73,res_y*.8+107))
	else:
		screen.blit(images["redo"],(res_x*.73,res_y*.8+107))

def border(tool):
	''' Checks to draw border on selected tool '''

	if tool == "about":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn1"],1)

	elif tool == "brush":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn3"],1)

	elif tool == "eraser":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn4"],1)

	elif tool == "pencil":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn5"],1)

	elif tool == "ink":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn6"],1)

	elif tool == "spray":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn7"],1)

	elif tool == "fill":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn8"],1)

	elif tool == "text":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn9"],1)

	elif tool == "stamp":
		fresh()
		draw.rect(screen,(255,255,255),rects["btn10"],1)

	else:fresh()