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
import numpy as np
from dotenv import load_dotenv
load_dotenv()
from tvDatafeed import TvDatafeed, Interval
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

import yfinance as yf

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
		self.searchStatus(self.stockSymbolList)

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
		FROM_PWD = "gnxzvixizpfqdhhj" 
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

	def Supertrend(self,some_symbol):
		
		atr_period = 10
		multiplier = 3.0

		#df = yf.download(some_symbol, start='2022-03-11', end='2022-11-11', interval="1wk")
		username = 'emingarayevemin'
		password = 'Maykhart1992!'
		tv = TvDatafeed(username, password)
		df=tv.get_hist(symbol="ARCKW", exchange='NASDAQ', interval = Interval.in_weekly, n_bars=100)
		high = df['high']
		low = df['low']
		close = df['close']
		
		# calculate ATR
		price_diffs = [high - low, 
					high - close.shift(), 
					close.shift() - low]
		true_range = pd.concat(price_diffs, axis=1)
		true_range = true_range.abs().max(axis=1)
		# default ATR calculation in supertrend indicator
		atr = true_range.ewm(alpha=1/atr_period,min_periods=atr_period).mean() 
		# df['atr'] = df['tr'].rolling(atr_period).mean()
		
		# HL2 is simply the average of high and low prices
		hl2 = (high + low) / 2
		# upperband and lowerband calculation
		# notice that final bands are set to be equal to the respective bands
		final_upperband = upperband = hl2 + (multiplier * atr)
		final_lowerband = lowerband = hl2 - (multiplier * atr)
		
		# initialize Supertrend column to True
		supertrend = [True] * len(df)
		
		for i in range(1, len(df.index)):
			curr, prev = i, i-1
			
			# if current close price crosses above upperband
			if close[curr] > final_upperband[prev]:
				supertrend[curr] = True
			# if current close price crosses below lowerband
			elif close[curr] < final_lowerband[prev]:
				supertrend[curr] = False
			# else, the trend continues
			else:
				supertrend[curr] = supertrend[prev]
				
				# adjustment to the final bands
				if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
					final_lowerband[curr] = final_lowerband[prev]
				if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
					final_upperband[curr] = final_upperband[prev]

			# to remove bands according to the trend direction
			if supertrend[curr] == True:
				final_upperband[curr] = np.nan
			else:
				final_lowerband[curr] = np.nan
		
		supertrend_signal=""
		try:
			if np.isnan(final_lowerband[-1]) and np.isnan(final_lowerband[-2]) and np.isnan(final_lowerband[-3]) and not np.isnan(final_upperband[-1]) and not np.isnan(final_upperband[-2]) and not np.isnan(final_upperband[-3]):
				supertrend_signal="Sell"
			elif not np.isnan(final_lowerband[-1]) and not np.isnan(final_lowerband[-2]) and not np.isnan(final_lowerband[-3]) and np.isnan(final_upperband[-1]) and np.isnan(final_upperband[-2]) and np.isnan(final_upperband[-3]):
				supertrend_signal="Buy"
			else:
				supertrend_signal=""
		except:
			print(some_symbol)

		return supertrend_signal

	def searchStatus(self, stockSymbolList):
		infolist = []

		for stockSymbol in stockSymbolList:
			sgn=self.Supertrend(stockSymbol)
			print(sgn)
			if sgn=="Sell":
				infolist.append(stockSymbol)
			else:
				continue

		if infolist!=[]:
			mail_content = "Stock Symbol   Overall Risk\n"
			for sym in infolist:
				mail_content += f"{sym}\n"
			print('___entered if block___')
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = 'High Risk Stocks'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['mike@mihfinancial.ca', 'high.risk.stocks@gmail.com']
			msg['To'] = ", ".join(recipients)
			# Send the message via our own SMTP server.
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "gnxzvixizpfqdhhj")
			print("SUCCESS at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block___')
			
			server.quit()


		print("=======")


bet = StockStatusBot(Config())
