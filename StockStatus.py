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

	class madeupintervalobj:
		def __init__(self, value):
			self.value = value
	x2D=madeupintervalobj('2D')
	x10W=madeupintervalobj('10W')

	
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
		#self.loginWithTracker()
		self.searchStatus(self.stockSymbolList)
		username = 'trader989'
		password = '$Palta646'
		print('______BEGIN____')
		self.tv = TvDatafeed(username, password)
		self.tv.token="eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoyMTM0NjYzLCJleHAiOjE2NzQwNTM5NTAsImlhdCI6MTY3NDAzOTU1MCwicGxhbiI6InByb19wcmVtaXVtIiwiZXh0X2hvdXJzIjoxLCJwZXJtIjoiYW1leCxjYm90LGNib3RfbWluaSxjbWUsY21lLWZ1bGwsY21lX21pbmksY29tZXgsY29tZXhfbWluaSxuYXNkYXEsbmFzZGFxX2dpZHMsbnltZXgsbnltZXhfbWluaSxueXNlLGx1eHNlX2RseSIsInN0dWR5X3Blcm0iOiJQVUI7T3BtV3NabWhHNFQ4QnN6TkFBUmozTVFPc0dRSzU4ZngsUFVCO2ZlMWJkZWFiMDA2YjQ4MTM4ZGNkZTM1ZWZmYmFjMGNmLFBVQjtZdGd5ckwzU2pwVThMM09YSkc5em5STFI2ZkxuVnlZWSxQVUI7YjI2ZjY1YzMyYWUzNDU1YjhkNzgzN2I4NjZmNDJiZTksdHYtdm9sdW1lYnlwcmljZSxQVUI7NjI5MzM2YjhiYTJlNGQ0NDlmZjkxMTMwOGYwNTUyOTQsdHYtcHJvc3R1ZGllcyxQVUI7cXNFbEIzT0kyVVA0bUl2V0ZTRVhMazlCSDJCY0RTdjMsdHYtY2hhcnRwYXR0ZXJucyxQVUI7Y1hvTFJKc1ZxUTFuZXg5VGNrc21wSEZGb2RhTGdBTDQsUFVCOzhrSDZVNWRPcEJweWZZNXpIY3NNYWxRVXRsMGlQdzhHLFBVQjsyMTJjNGVkYmZlMWM0MDU2YjJhM2YyMWYyMzg2YmU5ZiIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MCwibWF4X2NoYXJ0cyI6OCwibWF4X2FjdGl2ZV9hbGVydHMiOjQwMCwibWF4X3N0dWR5X29uX3N0dWR5IjoyNH0.S0wxDL7c1NV5H477QEgMAdVb0HejdwBYfqpeFhWjHXrlMED8AT-UJJ3ozKUGyqZYVW0yVvrYzCEdbabYGXnQWKAoXEnz2lZsgU--0yHNZUp3R5yjCEnDcVkk0GLqSrKIFsYhuGzavL2sK6bY9gGrHiggzC2ADU6RlzeVz6SvkpI"
		print('______BEGIN222222222____')

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


	def converter(self, df):
		today = datetime.today()
		current_year = today.strftime("%Y")

		df=df.iloc[7:,:]
		xs=[]
		for i in df.index:
			xs.append(i.year)
		xs=sorted(set(xs))
		df_final=df.iloc[0:2,:]
		for yr in xs:
			if yr==2014 or yr==2015:
				continue

			df_year=df[df.index.year==yr]
			j=0
			for i in range(len(df_year.index)):
				date1=df_year.index[j]
				date2=df_year.index[i]
				
				if date1.month==1 and (date1.day_of_week!=0 and date1.day_of_week!=1):
					j=j+1
					continue
				
				if yr!=current_year and date1.month==12:
					df1=df_year.iloc[j:,:]
					#df1['open'][0] no changes
					df1['close'][0]=df1['close'][-1]
					df1['low'][0]=df1['low'].min()
					df1['high'][0]=df1['high'].max()
					df1.drop(df1.tail(len(df1.index)-1).index,inplace=True)
					df_final=df_final.append(df1, ignore_index=False)
					break
				
				if str(yr)==current_year and date2==df_year.index[-1] and not ((date2-date1).days>=69):
					df1=df_year.iloc[j:,:]
					#df1['open'][0] no changes
					df1['close'][0]=df1['close'][-1]
					df1['low'][0]=df1['low'].min()
					df1['high'][0]=df1['high'].max()
					df1.drop(df1.tail(len(df1.index)-1).index,inplace=True)
					df_final=df_final.append(df1, ignore_index=False)

				if (date2-date1).days>=69:
					df1=df_year.iloc[j:i,:]
					#df1['open'][0] no changes
					df1['close'][0]=df1['close'][-1]
					df1['low'][0]=df1['low'].min()
					df1['high'][0]=df1['high'].max()
					df1.drop(df1.tail(len(df1.index)-1).index,inplace=True)
					df_final=df_final.append(df1, ignore_index=False)
					j=i

		df_final=df_final.iloc[2:,:]
		return df_final

	def ST(self, df): #df is the dataframe, n is the period, f is the factor; f=3, n=7 are commonly used.
		#Calculation of ATR
		f=3
		n=10
		df['H-L']=abs(df['high']-df['low'])
		df['H-PC']=abs(df['high']-df['close'].shift(1))
		df['L-PC']=abs(df['low']-df['close'].shift(1))
		df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1)
		df['ATR']=np.nan
		df['ATR'][n-1]=df['TR'][:n-1].mean() #.ix is deprecated from pandas verion- 0.19
		for i in range(n,len(df)):
			df['ATR'][i]=(df['ATR'][i-1]*(n-1)+ df['TR'][i])/n

		#Calculation of SuperTrend
		df['Upper Basic']=(df['high']+df['low'])/2+(f*df['ATR'])
		df['Lower Basic']=(df['high']+df['low'])/2-(f*df['ATR'])
		df['Upper Band']=df['Upper Basic']
		df['Lower Band']=df['Lower Basic']
		for i in range(n,len(df)):
			if df['close'][i-1]<=df['Upper Band'][i-1]:
				df['Upper Band'][i]=min(df['Upper Basic'][i],df['Upper Band'][i-1])
			else:
				df['Upper Band'][i]=df['Upper Basic'][i]    
		for i in range(n,len(df)):
			if df['close'][i-1]>=df['Lower Band'][i-1]:
				df['Lower Band'][i]=max(df['Lower Basic'][i],df['Lower Band'][i-1])
			else:
				df['Lower Band'][i]=df['Lower Basic'][i]   
		df['SuperTrend']=np.nan
		for i in df['SuperTrend']:
			if df['close'][n-1]<=df['Upper Band'][n-1]:
				df['SuperTrend'][n-1]=df['Upper Band'][n-1]
			elif df['close'][n-1]>df['Upper Band'][i]:
				df['SuperTrend'][n-1]=df['Lower Band'][n-1]
		for i in range(n,len(df)):
			if df['SuperTrend'][i-1]==df['Upper Band'][i-1] and df['close'][i]<=df['Upper Band'][i]:
				df['SuperTrend'][i]=df['Upper Band'][i]
			elif  df['SuperTrend'][i-1]==df['Upper Band'][i-1] and df['close'][i]>=df['Upper Band'][i]:
				df['SuperTrend'][i]=df['Lower Band'][i]
			elif df['SuperTrend'][i-1]==df['Lower Band'][i-1] and df['close'][i]>=df['Lower Band'][i]:
				df['SuperTrend'][i]=df['Lower Band'][i]
			elif df['SuperTrend'][i-1]==df['Lower Band'][i-1] and df['close'][i]<=df['Lower Band'][i]:
				df['SuperTrend'][i]=df['Upper Band'][i]
		for i in range(len(df)):
			if abs(df['SuperTrend'][i]-df['Upper Band'][i])<0.00001:
				df['Lower Band'][i]=np.nan
			elif abs(df['SuperTrend'][i]-df['Lower Band'][i])<0.00001:
				df['Upper Band'][i]=np.nan
		return df['Lower Band'], df['Upper Band']



	def Supertrend(self, some_symbol, intrval, tv=self.tv):
		
		atr_period = 10
		multiplier = 3.0
		american=["NASDAQ", "NYSE", "Arca", "OTC", "DJ", "SP", "CBOE", "CBOT", "CME GLOBEX", "COMEX", "NYMEX", "ICEUS", "FairX", "ECONOMY"]



		exch=tv.search_symbol(some_symbol)[0]['exchange']
		print('______END____')

		if len(set(exch.split()).intersection(set(american)))==0:
			for i in range(len(tv.search_symbol(some_symbol))):
				try:
					exch=tv.search_symbol(some_symbol)[i]['exchange']
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
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_daily, n_bars=500, extended_session=False)
		elif intrval=="1w":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_weekly, n_bars=500, extended_session=False)
		elif intrval=="2d":
			print("___________________________________________________!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ",x2D.value)
			df=tv.get_hist(some_symbol, exchange=exch, interval = x2D, n_bars=500, extended_session=False)
		elif intrval=="10weeks":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_daily, n_bars=5000, extended_session=False)
			try:
				df=converter(df)
			except:
				prefix=tv.search_symbol(some_symbol)[0]['prefix']
				df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_daily, n_bars=5000, extended_session=False)
				df=converter(df)

		
		
		try:
			high = df['high']
			low = df['low']
			close = df['close']
		except:
			prefix=tv.search_symbol(some_symbol)[0]['prefix']
			try:
				if intrval=="4hr":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_4_hour, n_bars=300, extended_session=True)
				elif intrval=="1d":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_daily, n_bars=500, extended_session=False)
				elif intrval=="2d":
					print("___________________________________________________!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ",x2D.value)
					df=tv.get_hist(some_symbol, exchange=prefix, interval = x2D, n_bars=500, extended_session=False)
				elif intrval=="1w":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_weekly, n_bars=500, extended_session=False)
				
				high = df['high']
				low = df['low']
				close = df['close']
			except:
				pass
		

		df_new=self.ST(df)
		final_lowerband=df_new[0]
		final_upperband=df_new[1]
		
		supertrend_signal=""
		try:
			if np.isnan(final_lowerband[-1]) and np.isnan(final_lowerband[-2]) and np.isnan(final_lowerband[-3])  and not np.isnan(final_lowerband[-4]) and not np.isnan(final_upperband[-1]) and not np.isnan(final_upperband[-2]) and not np.isnan(final_upperband[-3]) and np.isnan(final_upperband[-4]):
				supertrend_signal="Sell"
			elif (not np.isnan(final_upperband[-1]) and np.isnan(final_upperband[-2]) and not np.isnan(final_lowerband[-2])) or (not np.isnan(final_upperband[-2]) and np.isnan(final_upperband[-3]) and not np.isnan(final_lowerband[-3])) or (not np.isnan(final_upperband[-3]) and np.isnan(final_upperband[-4]) and not np.isnan(final_lowerband[-4])) or (not np.isnan(final_upperband[-3]) and not np.isnan(final_upperband[-4]) and (abs(final_upperband[-3]-final_upperband[-4])<0.001) and not np.isnan(final_lowerband[-5])):
				supertrend_signal="Sell"
			elif intrval=="2d" and not np.isnan(final_lowerband[-1]) and np.isnan(final_lowerband[-2]) and np.isnan(final_upperband[-1]): 
			#not np.isnan(final_lowerband[-1]) and not np.isnan(final_lowerband[-2]) and not np.isnan(final_lowerband[-3]) and np.isnan(final_lowerband[-4]) and np.isnan(final_upperband[-1]) and np.isnan(final_upperband[-2]) and np.isnan(final_upperband[-3]) and not np.isnan(final_upperband[-4]):
				supertrend_signal="Buy"
			else:
				supertrend_signal="Mixed"
		except:
			print('problems at line 349')

		return supertrend_signal






	def Supertrend2(self, some_symbol, intrval):
    
		atr_period = 10
		multiplier = 3.0
		american=["NASDAQ", "NYSE", "Arca", "OTC", "DJ", "SP", "CBOE", "CBOT", "CME GLOBEX", "COMEX", "NYMEX", "ICEUS", "FairX", "ECONOMY"]

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
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_4_hour, n_bars=300, extended_session=True)
		elif intrval=="1d":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_daily, n_bars=300, extended_session=False)
		elif intrval=="1w":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_weekly, n_bars=100, extended_session=False)
		elif intrval=="10weeks":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_daily, n_bars=1000, extended_session=False)
			logic = {'open'  : 'first', 'high'  : 'max', 'low'   : 'min', 'close' : 'last', 'volume': 'sum'}
			try:
				df = df.resample('10W').apply(logic)
			except:
				prefix=tv.search_symbol(some_symbol)[0]['prefix']
				df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_daily, n_bars=1000, extended_session=False)
				df = df.resample('10W').apply(logic)
		
		
		try:
			high = df['high']
			low = df['low']
			close = df['close']
		except:
			prefix=tv.search_symbol(some_symbol)[0]['prefix']
			try:
				if intrval=="4hr":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_4_hour, n_bars=300, extended_session=True)
				elif intrval=="1d":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_daily, n_bars=300, extended_session=False)
				elif intrval=="1w":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_weekly, n_bars=100, extended_session=False)
				
				high = df['high']
				low = df['low']
				close = df['close']
			except:
				pass





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
		infolist2 = []
		infolist3 = []

		docfile_list=[]
		with open("tickers.txt", "r") as crossref_tickers:
			lines = crossref_tickers.readlines()
		for l in lines:
					as_list = l.split("\n")
					docfile_list.append(as_list[0].replace("\n", ""))
		docfile_list=[x.strip(' ') for x in docfile_list]
		print("DOCFILE_LIST:", docfile_list)

		if stockSymbolList!=[]:
			stockSymbolList=list(set(stockSymbolList))

		for stockSymbol in stockSymbolList:
			print("stockSymbol Name:", stockSymbol)
			try:
				signal_4hr=self.Supertrend(stockSymbol,"4hr")
			except:
				signal_4hr=""
			try:
				signal_1d=self.Supertrend(stockSymbol,"1d")
			except Exception as ert:
				signal_1d=""
				print(ert)
			try:
				signal_1w=self.Supertrend(stockSymbol,"1w")
			except:
				signal_1w=""
			try:
				signal_10weeks=self.Supertrend(stockSymbol,"10weeks")
			except:
				signal_10weeks=""
			try:
				signal_2d=self.Supertrend(stockSymbol,"2d")
			except:
				signal_2d=""
			try:
				if stockSymbol in docfile_list:
					infolist2.append(stockSymbol)
			except:
				pass

			print(stockSymbol, end = ' ')
			print(signal_4hr, end = ' ')
			print(signal_1d, end = ' ')
			print(signal_1w, end = ' ')
			print("signal_2d:",signal_2d, "||||",end = ' ')
			print(signal_10weeks)
			#signal_4hr=="Sell" or
			if  signal_1d=="Sell" or signal_1w=="Sell" or signal_10weeks=="Sell":
				infolist.append(stockSymbol)
			else:
				continue

			if  signal_2d=="Buy":
				infolist3.append(stockSymbol)
			else:
				continue

		print("______________________")
		print("______________________")
		print("BUY INFOLIST3=",infolist3)
		print("______________________")
		print("______________________")

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
			msg['Subject'] = 'Cross referenced with doc file'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['high.risk.stocks@gmail.com', 'mike@mihfinancial.ca']
			msg['To'] = ", ".join(recipients)
			# Send the message via our own SMTP server.
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "gnxzvixizpfqdhhj")
			print("SUCCESS2 at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block2___')
			
			server.quit()


		print("=======")


bet = StockStatusBot(Config())
