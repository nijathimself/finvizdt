import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import re
import sys
from selenium.webdriver.common.keys import Keys
import time
import imaplib
import email
import traceback 
from bs4 import BeautifulSoup
import pandas as pd
from config import Config

from dotenv import load_dotenv
load_dotenv()

import imaplib
import smtplib

import mailparser
import os.path

import smtplib
from email.message import EmailMessage

import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os.path
import base64
import email
 
class StockStatusBot(object):
	"""
	class will scrape data from Imail Inbox after login
	"""
	def __init__(self, conf,data_center=None):
		super(StockStatusBot, self).__init__()
		self.stockSymbolList = []
		self.MAIL_USERNAME =  os.environ.get('MAIL_USERNAME')
		self.MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
		self.RECEIVER_MAIL = os.environ.get('RECEIVER_MAIL')
		self.IMAP_SERVER = os.environ.get('IMAP_SERVER')
		self.conf = Config()
		self.logger = self.conf.logger
		self.driver = self.conf.drivers()
		self.base_url = os.environ.get('BASE_URL')
		#self.loginWithMail()
		self.mailLoginWithSelenium()
		self.loginWithTracker()
		#self.searchStatus(self.stockSymbolList)

	def loginWithMail(self):
		imap = imaplib.IMAP4_SSL(self.IMAP_SERVER)
		# imap.login(self.MAIL_USERNAME, self.MAIL_PASSWORD)
		try:
			status, summary = imap.login(self.MAIL_USERNAME, self.MAIL_PASSWORD)
			if status == "OK":
				print(summary)
		except imaplib.IMAP4.error as e:
			print("Error logging into Mail",str(e))
			sys.exit(0)  # Successful termination
		imap.list()
		imap.select("inbox") # connect to inbox.
		result, data = imap.search(None, '(FROM "Nijat Hakimov" SUBJECT "Screener Alert")' )
		ids = data[0] # data is a list.
		id_list = ids.split() # ids is a space separated string
		latest_email_id = id_list[-1] # get the latest

		result, data = imap.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822)             for the given ID
		raw_email = data[0][1]
		mail_data = mailparser.parse_from_bytes(raw_email)
		mail_body = mail_data.body
		obj = re.findall(r'\w+://finviz.com/quote.ashx\?t=(\w+)',mail_body)
		self.stockSymbol = obj[0] if obj else None

	def mailLoginWithSelenium(self):
		
		ORG_EMAIL = "@gmail.com" 
		FROM_EMAIL = "high.risk.stocks" + ORG_EMAIL 
		FROM_PWD = "sezbjeayolssbrrx" 
		SMTP_SERVER = "imap.gmail.com"

		# Use the client_secret.json file to identify the application requesting
		# authorization. The client ID (from that file) and access scopes are required.
		flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials_mike.json',scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])
		flow.redirect_uri = 'https://dilutiontracker.herokuapp.com/oauth2/redirect'
		authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
		print('Successful logging in Gmail!')
		
		try:
			mail = imaplib.IMAP4_SSL(SMTP_SERVER)
			mail.login(FROM_EMAIL,FROM_PWD)
			mail.select('inbox')
			typ,data = mail.search(None,'UnSeen')
			mail_ids = data[0]
			id_list = mail_ids.split()
			first_email_id = int(id_list[0])
			latest_email_id = int(id_list[-1])
			for i in id_list:
				id_m=re.findall(r'\d+',str(i))[0]
				data = mail.fetch(id_m, '(RFC822)' )
				for response_part in data:
					arr = response_part[0]
					if isinstance(arr, tuple):
						msg = email.message_from_string(str(arr[1],'utf-8'))
						obj = re.findall(r'\w+://finviz.com/quote.ashx\?t=([A-Z]+)', msg.as_string())
						if obj!=[]:
							for i in range(len(obj)):
								self.stockSymbolList.append(obj[i])
			mail.store(mail_ids.decode('utf-8').replace(' ',','),'+FLAGS','\Seen')
			print('All ticks are copied')
			print(self.stockSymbolList)
				
		except Exception as e:
			traceback.print_exc() 
			print(str(e))
			
#		SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify']
# 		creds=None
# 		if os.path.exists('token.json'):
# 			creds = Credentials.from_authorized_user_file('token.json', SCOPES)
		
# 		if not creds or not creds.valid:
# 			if creds and creds.expired and creds.refresh_token:
# 				creds.refresh(Request())
# 			else:
# 				flow = InstalledAppFlow.from_client_secrets_file('credentials_mike.json', SCOPES)
# 				creds = flow.run_local_server(port=0)
#         	# Save the credentials for the next run
# 			with open('token.json', 'w') as token:
# 				token.write(creds.to_json())


# 		try:
# 			creds = service_account.Credentials.from_service_account_file('credentials_mike.json', scopes=SCOPES)
# 			service = build('gmail', 'v1', credentials=creds)
# 			results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
# 			messages = results.get('messages',[])
# 			if not messages:
# 				print('No new messages.')
# 			else:
# 				message_count = 0
# 				for message in messages:
# 					msg = service.users().messages().get(userId='me', id=message['id']).execute()                
# 					email_data = msg['payload']['headers']
# 					for values in email_data:
# 						name = values['name']
# 						if name == 'From':
# 							from_name= values['value']                
# 							for part in msg['payload']['parts']:
# 								try:
# 									data = part['body']["data"]
# 									byte_code = base64.urlsafe_b64decode(data)

# 									text = byte_code.decode("utf-8")
# 									obj = re.findall(r'\w+://finviz.com/quote.ashx\?t=(\w+)',text)
# 									self.stockSymbolList = obj
# 									print(obj)
# 									time.sleep(5)
# 									break

# 									# mark the message as read (optional)
# 									msg  = service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()                                                       
# 								except BaseException as error:
# 									pass                            
# 		except Exception as error:
# 			print(f'An error occurred: {error}')






	def loginWithTracker(self):
		SCREENER_MAIL = os.environ.get('SCREENER_MAIL')
		SCREENER_PASSWORD = os.environ.get('SCREENER_PASSWORD')

		self.driver.get(self.base_url)
		wait = WebDriverWait(self.driver, 10)
		wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='email']")))																																
		try:
			loginBox = self.driver.find_element_by_xpath('//*[@id ="email"]')
			loginBox.send_keys(SCREENER_MAIL)
			time.sleep(3)
			passWordBox = self.driver.find_element_by_xpath('//*[@id ="password"]')
			passWordBox.send_keys(SCREENER_PASSWORD)
			time.sleep(3)
			signInButton = self.driver.find_elements_by_xpath('//*[@id="form_wrapper__login"]/form/button')
			signInButton[0].click()
			print('Login Successful...!!')
			time.sleep(5)
		except Exception as e:
			print(str(e))
			print('Login Failed')

	def searchStatus(self, stockSymbolList):
		infolist = []
		all_ratings=[]


# 		msg = MIMEText(mail_content, 'plain')
# 		msg['From']   = self.MAIL_USERNAME
# 		receivers = [self.MAIL_USERNAME]
# 		s = smtplib.SMTP_SSL(host='smtp.mail.yahoo.com', port=587)
# 		s.starttls()
# 		s.login(self.MAIL_USERNAME, self.MAIL_PASSWORD)
# 		s.sendmail(self.MAIL_USERNAME, self.RECEIVER_MAIL, msg.as_string())
# 		s.quit()



# 		# If modifying these scopes, delete the file token.json.
# 		SCOPES = ['https://mail.google.com/']

# 		creds = None
# # 		if os.path.exists('token.json'):
# # 			creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# 		# If there are no (valid) credentials available, let the user log in.
# 		if not creds or not creds.valid:
# # 			if creds and creds.expired and creds.refresh_token:
# # 				creds.refresh(Request())
# # 			else:
# 			flow = InstalledAppFlow.from_client_secrets_file('/app/credentials.json', SCOPES)
# 			creds = flow.run_local_server(port=0)
# 			# Save the credentials for the next run
# 			with open('token.json', 'w') as token:
# 				token.write(creds.to_json())


# 		service = build('gmail', 'v1', credentials=creds)


# 		def create_message(sender, to, subject, message_text):
# 			message = MIMEText(message_text)
# 			message['to'] = to
# 			message['from'] = sender
# 			message['subject'] = subject
# 			return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


# 		def send_message(service, user_id, message):
# 			try:
# 				message = (service.users().messages().send(userId=user_id, body=message)
# 						.execute())
# 				print('Message Id: %s' % message['id'])
# 				return message
# 			except Exception as error:
# 				print(error)


# 		message = create_message('me', 'nijathkm@gmail.com', 'hello', mail_content)
# 		print(send_message(service=service, user_id='me', message=message))
		
		if infolist!=[]:
			print('___entered if block___')
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = 'High Risk Stocks'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['mike@mihfinancial.ca', 'high.risk.stocks@gmail.com']
			msg['To'] = ", ".join(recipients)
			# Send the message via our own SMTP server.
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "Maykhartman1992!")
			print("SUCCESS at log into high.risk.stocks")
			#server.send_message(msg)
			
			print('___exited if block___')
			
			server.quit()


		print("=======")

bet = StockStatusBot(Config())
