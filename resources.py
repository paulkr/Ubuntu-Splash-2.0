# #----------------------------Ubuntu Splash 2.0-----------------------------# #
# ============================================================================ #
# # An MS Paint Clone using a pygame framework with an Ubuntu Desktop Theme  # #
# #                        Paul Krishnamurthy 2015                           # #
# #                              Resources                                   # #
# # ------------------------------------------------------------------------ # #

from pygame import *
init()
screen_res = display.Info()
screen = display.set_mode((screen_res.current_w, screen_res.current_h),FULLSCREEN)
res_x, res_y = screen.get_size()


## ----Images---- ##
images = {
	# convert_alpha for speed
	"wallpaper" : transform.scale(image.load("images/wallpaper.jpg"), (1090, 680)).convert_alpha(), # Resize to fit screen
	"color-picker" : transform.scale(image.load("images/grad.png"),(200,200)).convert_alpha(),
	"hue-bar" : transform.scale(image.load("images/hue-bar.png"),(20,200)).convert_alpha(),
	"toolbar" : image.load("images/toolbar.png").convert_alpha(),
	"toolbar-apps" : image.load("images/toolbar-deco.png").convert_alpha(),
	"clean" : image.load("images/clean.png").convert_alpha(),
	"exit" : image.load("images/exit.png").convert_alpha(),
	"exit-hover" : image.load("images/exit-hover.png").convert_alpha(),
	# Icons
	"btn1" : image.load("images/btn1.png").convert_alpha(),
	"btn1-hover" : image.load("images/btn1-hover.png").convert_alpha(),
	"btn2" : image.load("images/btn2.png").convert_alpha(),
	"btn2-hover" : image.load("images/btn2-hover.png").convert_alpha(),
	"btn3" : image.load("images/btn3.png").convert_alpha(),
	"btn3-hover" : image.load("images/btn3-hover.png").convert_alpha(),
	"btn4" : image.load("images/btn4.png").convert_alpha(),
	"btn4-hover" : image.load("images/btn4-hover.png").convert_alpha(),
	"btn5" : image.load("images/btn5.png").convert_alpha(),
	"btn5-hover" : image.load("images/btn5-hover.png").convert_alpha(),
	"btn6" : image.load("images/btn6.png").convert_alpha(),
	"btn6-hover" : image.load("images/btn6-hover.png").convert_alpha(),
	"btn7" : image.load("images/btn7.png").convert_alpha(),
	"btn7-hover" : image.load("images/btn7-hover.png").convert_alpha(),
	"btn8" : image.load("images/btn8.png").convert_alpha(),
	"btn8-hover" : image.load("images/btn8-hover.png").convert_alpha(),
	"btn9" : image.load("images/btn9.png").convert_alpha(),
	"btn9-hover" : image.load("images/btn9-hover.png").convert_alpha(),
	"btn10" : image.load("images/btn10.png").convert_alpha(),
	"btn10-hover" : image.load("images/btn10-hover.png").convert_alpha(),
	"fun" : image.load("images/fun.png").convert_alpha(),
	"fun-hover" : image.load("images/fun-hover.png").convert_alpha(),
	# Stamps
	"stamp1" : image.load("images/stamps/stamp1.png").convert_alpha(),
	"stamp2" : image.load("images/stamps/stamp2.png").convert_alpha(),
	"stamp3" : transform.scale(image.load("images/stamps/stamp3.gif"),(70,80)).convert_alpha(),
	"stamp4" : transform.scale(image.load("images/stamps/stamp4.png"),(64,64)).convert_alpha(),
	"stamp5" : transform.scale(image.load("images/stamps/stamp5.png"),(84,84)).convert_alpha(),
	"stamp6" : image.load("images/stamps/stamp6.png").convert_alpha(),
	"stamp7" : image.load("images/stamps/stamp7.gif").convert_alpha(),
	"stamp8" : image.load("images/stamps/stamp8.gif").convert_alpha(),
	"stamp9" : image.load("images/stamps/stamp9.png"),
	"stamp10" : transform.scale(image.load("images/stamps/stamp10.png"),(450,450)).convert_alpha(),
	# Shapes 
	"rect" : image.load("images/shapes/rect.gif").convert_alpha(),
	"rect-hover" : image.load("images/shapes/rect-hover.gif").convert_alpha(),
	"rect-pressed" : image.load("images/shapes/rect-pressed.gif").convert_alpha(),
	"circ" : image.load("images/shapes/circ.gif").convert_alpha(),
	"circ-hover" : image.load("images/shapes/circ-hover.gif").convert_alpha(),
	"circ-pressed" : image.load("images/shapes/circ-pressed.gif").convert_alpha(),
	"line" : image.load("images/shapes/line.gif").convert_alpha(),
	"line-hover" : image.load("images/shapes/line-hover.gif").convert_alpha(),
	"line-pressed" : image.load("images/shapes/line-pressed.gif").convert_alpha(),
	"poly" : image.load("images/shapes/poly.gif").convert_alpha(),
	"poly-hover" : image.load("images/shapes/poly-hover.gif").convert_alpha(),
	"poly-pressed" : image.load("images/shapes/poly-pressed.gif").convert_alpha(),
	# Filters
	"bw" : image.load("images/filters/bw.png").convert_alpha(),
	"sephia" : image.load("images/filters/sephia.png").convert_alpha(),
	"negative" : image.load("images/filters/negative.png").convert_alpha(),
	"blur_filter" : image.load("images/filters/blur.png").convert_alpha(),
	"tint" : image.load("images/filters/tint.gif").convert_alpha(),
	"fill_screen" : image.load("images/filters/fill.gif").convert_alpha(),
	# Other
	"save" : image.load("images/save.png").convert_alpha(),
	"save-hover" : image.load("images/save-hover.png").convert_alpha(),
	"open" : image.load("images/open.png").convert_alpha(),
	"open-hover" : image.load("images/open-hover.png").convert_alpha(),
	"email" : image.load("images/email.png").convert_alpha(),
	"email-hover" : image.load("images/email-hover.png").convert_alpha(),
	"filled" : image.load("images/shapes/fill_on.png").convert_alpha(),
	"unfilled" : image.load("images/shapes/fill_off.png").convert_alpha(),
	"redo" : image.load("images/redo.png").convert_alpha(),
	"redo-hover" : image.load("images/redo-hover.png").convert_alpha(),
	"undo" : image.load("images/undo.png").convert_alpha(),
	"undo-hover" : image.load("images/undo-hover.png").convert_alpha(),
	"alpha-brush" : image.load("images/alpha-brush.png"),
	"alpha-brush-hover" : image.load("images/alpha-brush-hover.png").convert_alpha(),
	"blur" : image.load("images/blur.png").convert_alpha(),
	"blur-hover" : image.load("images/blur-hover.png").convert_alpha(),
	"eyedropper" : image.load("images/eyedropper.png").convert_alpha(),
	"eyedropper-hover" : image.load("images/eyedropper-hover.png").convert_alpha(),
	"scissors" : image.load("images/scissors.png").convert_alpha(),
	"scissors-hover" : image.load("images/scissors-hover.png").convert_alpha(),
	"about" : image.load("images/about.png").convert_alpha(),
	"homepage" : image.load("images/homepage.png").convert_alpha(),
	"display-view" : image.load("images/display-view.png").convert_alpha(),
	"load-song" : image.load("images/load-song.png").convert_alpha(),
	"play" : image.load("images/play.png").convert_alpha(),
	"pause" : image.load("images/pause.png").convert_alpha(),
	"v-up" : image.load("images/v-up.png").convert_alpha(),
	"v-down" : image.load("images/v-down.png").convert_alpha()
}

## ----Rects---- ##
rects = {
	"canvas" : Rect(80,45,res_x*.71,res_y*.8),
	# Color Selector
	"color-picker" : Rect((res_x*.8,res_y-300)+images["color-picker"].get_size()),
	"hue-bar" : Rect((res_x*.8+200,res_y-300)+images["hue-bar"].get_size()),
	"color-deco" : Rect(res_x*.795,res_y-305,235,290), # Current color info
	"current-color" : Rect(res_x*.805,res_y-75,50,50),
	"delete" : Rect(*((7,110)+images["btn2"].get_size())),
	"exit" : Rect(*((res_x-26,0)+images["exit"].get_size())), 
	# Tool rects
	"btn1" : Rect(*((7,40)+images["btn1"].get_size())), 
	"btn2" : Rect(*((7,110)+images["btn2"].get_size())),
	"btn3" : Rect(*((7,180)+images["btn3"].get_size())),
	"btn4" : Rect(*((3,250)+images["btn4"].get_size())),
	"btn5" : Rect(*((7,300)+images["btn5"].get_size())),
	"btn6" : Rect(*((7,370)+images["btn6"].get_size())),
	"btn7" : Rect(*((7,440)+images["btn7"].get_size())),
	"btn8" : Rect(*((3,500)+images["btn8"].get_size())),
	"btn9" : Rect(*((7,580)+images["btn9"].get_size())),
	"btn10" : Rect(*((7,650)+images["btn10"].get_size())),
	"fun_rect" : Rect(*((res_x*.87,res_y*.4)+images["fun"].get_size())),
	# Shapes 
	"rect_rect" : Rect(*((res_x*.79+170,res_y*.5-19)+images["rect"].get_size())),
	"circ_rect" : Rect(*((res_x*.79+236,res_y*.5-19)+images["circ"].get_size())),
	"line_rect" : Rect(*((res_x*.79+170,res_y*.5+42)+images["line"].get_size())),
	"poly_rect" : Rect(*((res_x*.79+236,res_y*.5+42)+images["poly"].get_size())),
	# Filters
	"bw_rect" : Rect(*((95,res_y*.8+80)+images["bw"].get_size())),
	"sephia_rect" : Rect(*((195,res_y*.8+80)+images["sephia"].get_size())),
	"negative_rect" : Rect(*((295,res_y*.8+80)+images["negative"].get_size())),
	"blur_rect" : Rect(*((395,res_y*.8+80)+images["blur_filter"].get_size())),
	"tint_rect" : Rect(*((495,res_y*.8+80)+images["tint"].get_size())),
	"fill_screen_rect" : Rect(*((595,res_y*.8+80)+images["fill_screen"].get_size())),
	# Other
	"save_but" : Rect(*((res_x*.8,60)+images["save"].get_size())),
	"open_but" : Rect(*((res_x*.87,60)+images["open"].get_size())),
	"email_but" : Rect(*((res_x*.94,60)+images["email"].get_size())),
	"fill_rect" : Rect(*((690,res_y*.8+70)+images["filled"].get_size())),
	"undo_rect" : Rect(*((res_x*.73,res_y*.8+69)+images["undo"].get_size())),
	"redo_rect" : Rect(*((res_x*.73,res_y*.8+107)+images["redo"].get_size())),
	"var_back" : Rect(690,res_y*.8+70,80,75),
	"alpha-brush-rect" :  Rect(*((res_x*.79,res_y*.2)+images["alpha-brush"].get_size())),
	"blur-rect" :  Rect(*((res_x*.84,res_y*.2)+images["blur"].get_size())),
	"eyedropper-rect" :  Rect(*((res_x*.89,res_y*.2)+images["eyedropper"].get_size())),
	"scissors-rect" :  Rect(*((res_x*.94,res_y*.2)+images["scissors"].get_size())),
	"about_rect" : Rect(*((res_x*.82,res_y*.3)+images["about"].get_size())),
	"homepage_rect" : Rect(*((res_x*.82+90,res_y*.3)+images["homepage"].get_size())),
	"help" : Rect(235,0,60,31),
	"load_song_rect" :  Rect(*((800,res_y*.8+70)+images["load-song"].get_size())),
	"play_rect" : Rect(*((840,res_y*.8+70)+images["play"].get_size())),
	"pause_rect" : Rect(*((890,res_y*.8+70)+images["pause"].get_size())),
	"v_up_rect" : Rect(*((840,res_y*.8+112)+images["v-up"].get_size())),
	"v_down_rect" : Rect(*((800,res_y*.8+112)+images["v-down"].get_size()))
}
