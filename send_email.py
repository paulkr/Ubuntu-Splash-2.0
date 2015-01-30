# #----------------------------Ubuntu Splash 2.0-----------------------------# #
# ============================================================================ #
# # An MS Paint Clone using a pygame framework with an Ubuntu Desktop Theme  # #
# #                        Paul Krishnamurthy 2015                           # #
# #                               PyMail                                     # #
# # ------------------------------------------------------------------------ # #

import smtplib
from email.mime.multipart import MIMEMultipart as base # Message
from email.mime.text import MIMEText as text # Text
from email.mime.image import MIMEImage as img # Image attachment
from datetime import datetime # Time

# Get password from online
# Yes I know I should have some encrypting and decrypting for this...
import urllib.request as get

def send(to,file_name):

	# Log file to keep track of events
	log_file = open("local/events.log","a") # Append without overwrite

	try:
		# Important variables
		me = "ubuntusplash2.0@gmail.com"
		me_pass = str(get.urlopen('http://paulkr.com/misc/password.txt').read().decode()) # Grab password from my server

		message = base()
		message["Subject"] = "Your Paint Masterpiece!"
		message["From"] = me
		message["To"] = to

		output = base()
		message.attach(output)

		# Pretty text --> Minified html code
		content = "<head><style>h1{color:#800080;font-family: sans-serif;font-size:20px;}h2{color:#800000;font-family: sans-serif;font-size:15px;}p{color: black;font-family: sans-serif;font-size: 10px;}</style>\
		</head><body><h1>Thank you for using Ubuntu Splash 2.0</h1><h2>Your masterpiece is attached.</h2><br/><p>(C) 2014<br/>www.paulkr.com</p></body></html>"
		description = text(content, "html")
		output.attach(description)

		# This example assumes the image is in the current directory
		fp = open("local/saves/"+file_name, "rb")
		attachment = img(fp.read())
		attachment.add_header('Content-ID', 'Paint Save')
		output.attach(attachment)
		fp.close()

		# Write data to file
		log_file.write("%s emailed to %s at %s \n"%(file_name,to,datetime.now().strftime('%I:%M:%S %p')))

		# I was going to configure this with my personal server but using google's was easier.
		smtp = smtplib.SMTP("smtp.gmail.com",587) # Gmail smtp and port #
		# For authentication
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo
		smtp.login(me,me_pass) # Login
		smtp.sendmail(me,to,message.as_string()) # Final step
		smtp.quit()

	except:
		log_file.write("Unable to establish connection. Email not sent\n")

	log_file.close()