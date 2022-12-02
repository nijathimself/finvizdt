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

	def Supertrend(self,some_symbol,intrval):
		
		atr_period = 10
		multiplier = 3.0
		american=["NASDAQ", "NYSE", "Arca", "OTC", "DJ", "SP", "CBOE", "CBOT", "CME GLOBEX", "COMEX", "NYMEX", "ICEUS", "FairX", "ECONOMY"]

		#df = yf.download(some_symbol, start='2022-03-11', end='2022-11-11', interval="1wk")
		username = 'emingarayevemin'
		password = 'Maykhart1992!'
		tv = TvDatafeed(username, password)
		exch=tv.search_symbol(some_symbol)[0]['exchange']

		if len(set(exch.split()).intersection(set(american)))==0:
			for i in range(len(tv.search_symbol(some_symbol))):
				try:
					exch=tv.search_symbol('BEST')[i]['exchange']
					if exch in american:
						break
					else:
						continue
				except:
					print('No American stock found')
					continue


		if intrval=="4hr":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_4_hour, n_bars=200, extended_session=True)
		elif intrval=="1d":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_daily, n_bars=200, extended_session=False)
		elif intrval=="1w":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_weekly, n_bars=50, extended_session=False)
		elif intrval=="10weeks":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_daily, n_bars=200, extended_session=False)
			logic = {'open'  : 'first', 'high'  : 'max', 'low'   : 'min', 'close' : 'last', 'volume': 'sum'}
			df = df.resample('10W').apply(logic)
		
		
		try:
			high = df['high']
			low = df['low']
			close = df['close']
		except:
			df=yf.download(some_symbol, interval='1wk', period='1y')
			high = df['High']
			low = df['Low']
			close = df['Close']

		lookback=10
		multiplier=3
		# ATR
		tr1 = pd.DataFrame(high - low)
		tr2 = pd.DataFrame(abs(high - close.shift(1)))
		tr3 = pd.DataFrame(abs(low - close.shift(1)))
		frames = [tr1, tr2, tr3]
		tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
		atr = tr.ewm(lookback).mean()
		
		# H/L AVG AND BASIC UPPER & LOWER BAND
		
		hl_avg = (high + low) / 2
		upper_band = (hl_avg + multiplier * atr).dropna()
		lower_band = (hl_avg - multiplier * atr).dropna()
		
		# FINAL UPPER BAND
		
		final_bands = pd.DataFrame(columns = ['upper', 'lower'])
		final_bands.iloc[:,0] = [x for x in upper_band - upper_band]
		final_bands.iloc[:,1] = final_bands.iloc[:,0]
		
		for i in range(len(final_bands)):
			if i == 0:
				final_bands.iloc[i,0] = 0
			else:
				if (upper_band[i] < final_bands.iloc[i-1,0]) | (close[i-1] > final_bands.iloc[i-1,0]):
					final_bands.iloc[i,0] = upper_band[i]
				else:
					final_bands.iloc[i,0] = final_bands.iloc[i-1,0]
		
		# FINAL LOWER BAND
		
		for i in range(len(final_bands)):
			if i == 0:
				final_bands.iloc[i, 1] = 0
			else:
				if (lower_band[i] > final_bands.iloc[i-1,1]) | (close[i-1] < final_bands.iloc[i-1,1]):
					final_bands.iloc[i,1] = lower_band[i]
				else:
					final_bands.iloc[i,1] = final_bands.iloc[i-1,1]
		
		# SUPERTREND
		
		supertrend = pd.DataFrame(columns = [f'supertrend_{lookback}'])
		supertrend.iloc[:,0] = [x for x in final_bands['upper'] - final_bands['upper']]
		
		for i in range(len(supertrend)):
			if i == 0:
				supertrend.iloc[i, 0] = 0
			elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] < final_bands.iloc[i, 0]:
				supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
			elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] > final_bands.iloc[i, 0]:
				supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
			elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] > final_bands.iloc[i, 1]:
				supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
			elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] < final_bands.iloc[i, 1]:
				supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
		
		supertrend = supertrend.set_index(upper_band.index)
		supertrend = supertrend.dropna()[1:]
		
		# ST UPTREND/DOWNTREND
		
		upt = []
		dt = []
		close = close.iloc[len(close) - len(supertrend):]

		for i in range(len(supertrend)):
			if close[i] > supertrend.iloc[i, 0]:
				upt.append(supertrend.iloc[i, 0])
				dt.append(np.nan)
			elif close[i] < supertrend.iloc[i, 0]:
				upt.append(np.nan)
				dt.append(supertrend.iloc[i, 0])
			else:
				upt.append(np.nan)
				dt.append(np.nan)
				
		st, upt, dt = pd.Series(supertrend.iloc[:, 0]), pd.Series(upt), pd.Series(dt)
		upt.index, dt.index = supertrend.index, supertrend.index
		#lowerband--upt
		supertrend_signal=""
		try:
			if np.isnan(upt[-1]) and np.isnan(upt[-2]) and np.isnan(upt[-3])  and not np.isnan(upt[-4]) and not np.isnan(dt[-1]) and not np.isnan(dt[-2]) and not np.isnan(dt[-3]) and np.isnan(dt[-4]):
				supertrend_signal="Sell"
			elif (not np.isnan(dt[-1]) and np.isnan(dt[-2]) and not np.isnan(upt[-2])) or (not np.isnan(dt[-2]) and np.isnan(dt[-3]) and not np.isnan(upt[-3])) or (not np.isnan(dt[-3]) and np.isnan(dt[-4]) and not np.isnan(upt[-4])) or (not np.isnan(dt[-3]) and not np.isnan(dt[-4]) and (abs(dt[-3]-dt[-4])<0.001) and not np.isnan(upt[-5])):
				supertrend_signal="Sell"
			elif not np.isnan(upt[-1]) and not np.isnan(upt[-2]) and not np.isnan(upt[-3]) and np.isnan(upt[-4]) and np.isnan(dt[-1]) and np.isnan(dt[-2]) and np.isnan(dt[-3]) and not np.isnan(dt[-4]):
				supertrend_signal="Buy"
			else:
				supertrend_signal="Mixed"
		except:
			print(some_symbol)

		return supertrend_signal

	def searchStatus(self, stockSymbolList):
		infolist = []
		infolist2=[]
		docfile_list=["BIOL", "ELYS", "VIVE", "BIVI", "GROM", "BXRX", "DBGI", "ONCS", "WISA", "CYTH", "REVB", "REED", "ENSC", "TIVC", "VS", "PTE", "BVXV", "TOPS", "CEMI", "OP", "MRM", "DRMA", "TROO", "BTOG", "CREG"]

		if stockSymbolList!=[]:
			stockSymbolList=list(set(stockSymbolList))

		for stockSymbol in stockSymbolList:
			try:
				signal_4hr=self.Supertrend(stockSymbol,"4hr")
			except:
				signal_4hr=""
			try:
				signal_1d=self.Supertrend(stockSymbol,"1d")
			except:
				signal_1d=""
			try:
				signal_1w=self.Supertrend(stockSymbol,"1w")
			except:
				signal_1w=""
			try:
				signal_10weeks=self.Supertrend(stockSymbol,"10weeks")
			except:
				signal_10weeks=""
			try:
				if stockSymbol in docfile_list:
					infolist2.append(stockSymbol)
			except:
				pass

			print(stockSymbol, end = ' ')
			print(signal_4hr, end = ' ')
			print(signal_1d, end = ' ')
			print(signal_1w, end = ' ')
			print(signal_10weeks)
			#signal_4hr=="Sell" or
			if  signal_1d=="Sell" or signal_1w=="Sell" or signal_10weeks=="Sell":
				infolist.append(stockSymbol)
			else:
				continue

		if infolist!=[]:
			infolist=list(set(infolist))
			mail_content = "Stock Symbol\n"
			for sym in infolist:
				mail_content += f"{sym}\n"
			print('___entered if block___')
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = 'High Risk Stocks'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['high.risk.stocks@gmail.com', 'mike@mihfinancial.ca']
			msg['To'] = ", ".join(recipients)
			# Send the message via our own SMTP server.
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "gnxzvixizpfqdhhj")
			print("SUCCESS at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block___')
			
			server.quit()

		if infolist2!=[]:
			infolist2=list(set(infolist2))
			mail_content = "Stock Symbol\n"
			for sym in infolist2:
				mail_content += f"{sym}\n"
			print('___entered if block___')
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = 'Stocks cross referenced with doc file'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['high.risk.stocks@gmail.com', 'mike@mihfinancial.ca']
			msg['To'] = ", ".join(recipients)
			# Send the message via our own SMTP server.
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "gnxzvixizpfqdhhj")
			print("SUCCESS at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block2___')
			
			server.quit()
		
		print("=======")


bet = StockStatusBot(Config())
