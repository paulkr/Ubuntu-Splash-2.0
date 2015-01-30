# #----------------------------Ubuntu Splash 2.0-----------------------------# #
# ============================================================================ #
# # An MS Paint Clone using a pygame framework with an Ubuntu Desktop Theme  # #
# #                        Paul Krishnamurthy 2015                           # #
# #                            Loading Frames                                # #
# # ------------------------------------------------------------------------ # #

from pygame import *
init()
screen_res = display.Info()
screen = display.set_mode((screen_res.current_w, screen_res.current_h),FULLSCREEN)
res_x, res_y = screen.get_size()

# No need to worry, I did not type all this out!

loading = {
	'0' : transform.scale(image.load('images/loading/Frame0.png'),(res_x,res_y)).convert_alpha(),
	'1' : transform.scale(image.load('images/loading/Frame1.png'),(res_x,res_y)).convert_alpha(),
	'2' : transform.scale(image.load('images/loading/Frame2.png'),(res_x,res_y)).convert_alpha(),
	'3' : transform.scale(image.load('images/loading/Frame3.png'),(res_x,res_y)).convert_alpha(),
	'4' : transform.scale(image.load('images/loading/Frame4.png'),(res_x,res_y)).convert_alpha(),
	'5' : transform.scale(image.load('images/loading/Frame5.png'),(res_x,res_y)).convert_alpha(),
	'6' : transform.scale(image.load('images/loading/Frame6.png'),(res_x,res_y)).convert_alpha(),
	'7' : transform.scale(image.load('images/loading/Frame7.png'),(res_x,res_y)).convert_alpha(),
	'8' : transform.scale(image.load('images/loading/Frame8.png'),(res_x,res_y)).convert_alpha(),
	'9' : transform.scale(image.load('images/loading/Frame9.png'),(res_x,res_y)).convert_alpha(),
	'10' : transform.scale(image.load('images/loading/Frame10.png'),(res_x,res_y)).convert_alpha(),
	'11' : transform.scale(image.load('images/loading/Frame11.png'),(res_x,res_y)).convert_alpha(),
	'12' : transform.scale(image.load('images/loading/Frame12.png'),(res_x,res_y)).convert_alpha(),
	'13' : transform.scale(image.load('images/loading/Frame13.png'),(res_x,res_y)).convert_alpha(),
	'14' : transform.scale(image.load('images/loading/Frame14.png'),(res_x,res_y)).convert_alpha(),
	'15' : transform.scale(image.load('images/loading/Frame15.png'),(res_x,res_y)).convert_alpha(),
	'16' : transform.scale(image.load('images/loading/Frame16.png'),(res_x,res_y)).convert_alpha(),
	'17' : transform.scale(image.load('images/loading/Frame17.png'),(res_x,res_y)).convert_alpha(),
	'18' : transform.scale(image.load('images/loading/Frame18.png'),(res_x,res_y)).convert_alpha(),
	'19' : transform.scale(image.load('images/loading/Frame19.png'),(res_x,res_y)).convert_alpha(),
	'20' : transform.scale(image.load('images/loading/Frame20.png'),(res_x,res_y)).convert_alpha(),
	'21' : transform.scale(image.load('images/loading/Frame21.png'),(res_x,res_y)).convert_alpha(),
	'22' : transform.scale(image.load('images/loading/Frame22.png'),(res_x,res_y)).convert_alpha(),
	'23' : transform.scale(image.load('images/loading/Frame23.png'),(res_x,res_y)).convert_alpha(),
	'24' : transform.scale(image.load('images/loading/Frame24.png'),(res_x,res_y)).convert_alpha(),
	'25' : transform.scale(image.load('images/loading/Frame25.png'),(res_x,res_y)).convert_alpha(),
	'26' : transform.scale(image.load('images/loading/Frame26.png'),(res_x,res_y)).convert_alpha(),
	'27' : transform.scale(image.load('images/loading/Frame27.png'),(res_x,res_y)).convert_alpha(),
	'28' : transform.scale(image.load('images/loading/Frame28.png'),(res_x,res_y)).convert_alpha(),
	'29' : transform.scale(image.load('images/loading/Frame29.png'),(res_x,res_y)).convert_alpha(),
	'30' : transform.scale(image.load('images/loading/Frame30.png'),(res_x,res_y)).convert_alpha()
}