# #----------------------------PyMail------------------------------# #
# ================================================================== #
# #                         PyMail 2015                            # #
# #                   Paul Krishnamurthy 2015                      # #
# #                       www.paulKr.com                           # #
# # -------------------------------------------------------------- # #

import smtplib
from email.mime.multipart import MIMEMultipart as base # Message
from email.mime.text import MIMEText as text # Text
from email.mime.image import MIMEImage as img # Image attachment
from datetime import datetime # Time
from login import *

# Currently this only supports image attachment

def send(to,subject,content,file_name):
	""" Sends email using credectials passed as arguments """
	
	# Log file to keep track of events
	log_file = open("events.log","a")

	try:
		# Main
		message = base()
		message["Subject"] = subject
		message["From"] = me
		message["To"] = to

		output = base()
		message.attach(output)

		# Attach content
		description = text(content, "html")
		output.attach(description)

		# For attachment
		if file_name != "":
			# This example assumes the image is in the current directory
			fp = open(file_name, "rb")
			attachment = img(fp.read())
			attachment.add_header('Content-ID', 'Attachment')
			output.attach(attachment)
			fp.close()

			# Log event
			log_file.write("%s emailed to %s at %s\n"%(file_name[file_name.rfind("/")+1:],to.strip(),datetime.now().strftime('%I:%M:%S %p')))
			

		else:
			# Log event
			log_file.write("Emailed to %s at %s\n"%(to.strip(),datetime.now().strftime('%I:%M:%S %p')))

		# Final send
		smtp = smtplib.SMTP("smtp.gmail.com",587) # Gmail smtp and port number

		# For authentication
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo
		smtp.login(me,me_pass) # Login
		smtp.sendmail(me,to,message.as_string()) # Send email
		smtp.quit()

	except:
		# Log errors
		log_file.write("Unable to establish connection. Email not sent\n")
	
	log_file.close()
  