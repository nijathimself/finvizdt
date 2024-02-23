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

# New Twilio logic
from twilio.rest import Client
account_sid = 'ACec6c5a56a914075e0124b2fd8c088b1b'
auth_token = 'ea6b026ceb2a7bf887f292a324e4ada3'
client = Client(account_sid, auth_token)
from_ = "12345013256"
to = "+16046135789"

def send_sms(from_=from_, to=to, body="test"):
    """
    Sends an SMS message using the Twilio API.
    Args:
        from_ (str): The phone number or alphanumeric sender ID.
        to (str): The recipient's phone number.
        body (str): The text message to be sent.
    Returns:
        None
    Raises:
        TwilioException: If there is an error while sending the SMS.
    """
    message = client.messages \
                    .create(
                        body=body,
                        from_=from_,
                        to=to
                    )

    print(message.sid)
	
class madeupintervalobj:
	def __init__(self, value):
		self.value = value

class StockStatusBot(object):
	"""
	class will scrape data from Imail Inbox after login
	"""

	username = 'trader989'
	password = '$Palta646'
	#
	print('______BEGIN____')
	tv0 = TvDatafeed(username, password)
	#tv0.token="eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoyMTM0NjYzLCJleHAiOjE2NzQwNTM5NTAsImlhdCI6MTY3NDAzOTU1MCwicGxhbiI6InByb19wcmVtaXVtIiwiZXh0X2hvdXJzIjoxLCJwZXJtIjoiYW1leCxjYm90LGNib3RfbWluaSxjbWUsY21lLWZ1bGwsY21lX21pbmksY29tZXgsY29tZXhfbWluaSxuYXNkYXEsbmFzZGFxX2dpZHMsbnltZXgsbnltZXhfbWluaSxueXNlLGx1eHNlX2RseSIsInN0dWR5X3Blcm0iOiJQVUI7T3BtV3NabWhHNFQ4QnN6TkFBUmozTVFPc0dRSzU4ZngsUFVCO2ZlMWJkZWFiMDA2YjQ4MTM4ZGNkZTM1ZWZmYmFjMGNmLFBVQjtZdGd5ckwzU2pwVThMM09YSkc5em5STFI2ZkxuVnlZWSxQVUI7YjI2ZjY1YzMyYWUzNDU1YjhkNzgzN2I4NjZmNDJiZTksdHYtdm9sdW1lYnlwcmljZSxQVUI7NjI5MzM2YjhiYTJlNGQ0NDlmZjkxMTMwOGYwNTUyOTQsdHYtcHJvc3R1ZGllcyxQVUI7cXNFbEIzT0kyVVA0bUl2V0ZTRVhMazlCSDJCY0RTdjMsdHYtY2hhcnRwYXR0ZXJucyxQVUI7Y1hvTFJKc1ZxUTFuZXg5VGNrc21wSEZGb2RhTGdBTDQsUFVCOzhrSDZVNWRPcEJweWZZNXpIY3NNYWxRVXRsMGlQdzhHLFBVQjsyMTJjNGVkYmZlMWM0MDU2YjJhM2YyMWYyMzg2YmU5ZiIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MCwibWF4X2NoYXJ0cyI6OCwibWF4X2FjdGl2ZV9hbGVydHMiOjQwMCwibWF4X3N0dWR5X29uX3N0dWR5IjoyNH0.S0wxDL7c1NV5H477QEgMAdVb0HejdwBYfqpeFhWjHXrlMED8AT-UJJ3ozKUGyqZYVW0yVvrYzCEdbabYGXnQWKAoXEnz2lZsgU--0yHNZUp3R5yjCEnDcVkk0GLqSrKIFsYhuGzavL2sK6bY9gGrHiggzC2ADU6RlzeVz6SvkpI"
	print('______BEGIN222222222____')

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
		FROM_PWD = "qhyhtfschqvsbwla" 
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
						obj2 = re.findall(r'\w+://elite.finviz.com/quote.ashx\?t=([A-Z]+)', msg.as_string())
						print('obj')
						print(obj)
						print(obj2)
						if obj!=[]:
							for i in range(len(obj)):
								self.stockSymbolList.append(obj[i])
						if obj2!=[]:
							for i in range(len(obj2)):
								self.stockSymbolList.append(obj2[i])
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

	def round_time(self, dt):
		hour = dt.hour
		if hour < 1:
			return dt.replace(hour=1, minute=0, second=0, microsecond=0)
		elif hour < 6:
			return dt.replace(hour=1, minute=0, second=0, microsecond=0)
		elif hour < 11:
			return dt.replace(hour=6, minute=0, second=0, microsecond=0)
		elif hour < 16:
			return dt.replace(hour=11, minute=0, second=0, microsecond=0)
		else:
			return dt.replace(hour=16, minute=0, second=0, microsecond=0)


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



	def Supertrend(self, some_symbol, intrval, tv=tv0):
		
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

		if intrval=="1hr":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_1_hour, n_bars=200, extended_session=True)
		elif intrval=="4hr":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_4_hour, n_bars=200, extended_session=True)
		elif intrval=="1d":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_daily, n_bars=500, extended_session=False)
		elif intrval=="1w":
			df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_weekly, n_bars=500, extended_session=False)
		elif intrval=="2d":
			x2D=madeupintervalobj('2D')
			df=tv.get_hist(some_symbol, exchange=exch, interval = x2D, n_bars=500, extended_session=False)
		elif intrval=="10weeks":
			df=tv.get_hist(some_symbol, exchange=exch, interval = x10W, n_bars=500, extended_session=False)
		elif intrval=="5hr_ExS":
			x5H=madeupintervalobj('5H')
			df=tv.get_hist(some_symbol, exchange=exch, interval = x5H, n_bars=500, extended_session=True)
		elif intrval=="5hr_":
			x5H=madeupintervalobj('5H')
			df=tv.get_hist(some_symbol, exchange=exch, interval = x5H, n_bars=500, extended_session=False)

		try:
			high = df['high']
			low = df['low']
			close = df['close']
			open = df['open']
		except:
			try:
				try:
					prefix=tv.search_symbol(some_symbol)[0]['prefix']
				except:
					pass
				if intrval=="1hr":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_1_hour, n_bars=300, extended_session=True)
				elif intrval=="4hr":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_4_hour, n_bars=300, extended_session=True)
				elif intrval=="1d":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_daily, n_bars=500, extended_session=False)
				elif intrval=="2d":
					x2D=madeupintervalobj('2D')
					df=tv.get_hist(some_symbol, exchange=prefix, interval = x2D, n_bars=500, extended_session=False)
				elif intrval=="1w":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_weekly, n_bars=500, extended_session=False)
				elif intrval=="10weeks":
					df=tv.get_hist(some_symbol, exchange=prefix, interval = x10W, n_bars=500, extended_session=False)
				elif intrval=="5hr_":
					x5H=madeupintervalobj('5H')
					df=tv.get_hist(some_symbol, exchange=exch, interval = x5H, n_bars=500, extended_session=False)
				elif intrval=="5hr_ExS":
					x5H=madeupintervalobj('5H')
					df=tv.get_hist(some_symbol, exchange=exch, interval = x5H, n_bars=500, extended_session=True)

				try:
					high = df['high']
					low = df['low']
					close = df['close']
					open = df['open']
				except:
					if intrval=="5hr_":
						df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_5_minute, n_bars=1500, extended_session=False)
						df['rounded_time'] = df.index.map(self.round_time)
						df = df.groupby('rounded_time').agg({
							'open': 'first',
							'high': 'max',
							'low': 'min',
							'close': 'last'
						})
					elif intrval=="5hr_ExS":
						df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_5_minute, n_bars=1500, extended_session=True)
						df['rounded_time'] = df.index.map(self.round_time)
						df = df.groupby('rounded_time').agg({
							'open': 'first',
							'high': 'max',
							'low': 'min',
							'close': 'last'
						})
					else:
						pass
			except:
				pass
		

		df_new=self.ST(df)
		final_lowerband=df_new[0]
		final_upperband=df_new[1]
		
		if intrval=="5hr_ExS" or intrval=="5hr_":
			try:
				five_hour_ALERT=self.HH(final_upperband, open, close, high) 
			except:
				five_hour_ALERT=False
			
			if five_hour_ALERT==True:
					if intrval=="5hr_ExS":
						supertrend_signal5="5H_ExS_ALERT"
					elif intrval=="5hr_":
						supertrend_signal5="5H_ALERT"
			else:
				supertrend_signal5="no alert"



		if intrval=="5hr_ExS" or intrval=="5hr_":
			supertrend_signal=supertrend_signal5
		else:
			supertrend_signal=""
			try:
				if np.isnan(final_lowerband[-1]) and np.isnan(final_lowerband[-2]) and np.isnan(final_lowerband[-3])  and not np.isnan(final_lowerband[-4]) and not np.isnan(final_upperband[-1]) and not np.isnan(final_upperband[-2]) and not np.isnan(final_upperband[-3]) and np.isnan(final_upperband[-4]):
					supertrend_signal="Sell"
				elif (not np.isnan(final_upperband[-1]) and np.isnan(final_upperband[-2]) and not np.isnan(final_lowerband[-2])) or (not np.isnan(final_upperband[-2]) and np.isnan(final_upperband[-3]) and not np.isnan(final_lowerband[-3])) or (not np.isnan(final_upperband[-3]) and np.isnan(final_upperband[-4]) and not np.isnan(final_lowerband[-4])) or (not np.isnan(final_upperband[-3]) and not np.isnan(final_upperband[-4]) and (abs(final_upperband[-3]-final_upperband[-4])<0.001) and not np.isnan(final_lowerband[-5])) or (not np.isnan(final_upperband[-3]) and not np.isnan(final_upperband[-4]) and not np.isnan(final_upperband[-5]) and (abs(final_upperband[-3]-final_upperband[-4])<0.001) and (abs(final_upperband[-4]-final_upperband[-5])<0.001) and not np.isnan(final_lowerband[-6])) or (not np.isnan(final_upperband[-3]) and not np.isnan(final_upperband[-4]) and not np.isnan(final_upperband[-5]) and not np.isnan(final_upperband[-6]) and (abs(final_upperband[-3]-final_upperband[-4])<0.001) and (abs(final_upperband[-4]-final_upperband[-5])<0.001) and (abs(final_upperband[-5]-final_upperband[-6])<0.001) and not np.isnan(final_lowerband[-7])):
					supertrend_signal="Sell"
				elif intrval=="2d" and (not np.isnan(final_lowerband[-1]) and not np.isnan(final_lowerband[-2]) and np.isnan(final_lowerband[-3]) and not np.isnan(final_upperband[-3]) ) : 
				#(not np.isnan(final_lowerband[-1]) and np.isnan(final_lowerband[-2]) and np.isnan(final_upperband[-1])) or
				#not np.isnan(final_lowerband[-1]) and not np.isnan(final_lowerband[-2]) and not np.isnan(final_lowerband[-3]) and np.isnan(final_lowerband[-4]) and np.isnan(final_upperband[-1]) and np.isnan(final_upperband[-2]) and np.isnan(final_upperband[-3]) and not np.isnan(final_upperband[-4]):
					supertrend_signal="Buy"
				elif intrval=="1w" and (not np.isnan(final_lowerband[-1]) and np.isnan(final_lowerband[-2]) and np.isnan(final_upperband[-1])):
				#or (not np.isnan(final_lowerband[-1]) and not np.isnan(final_lowerband[-2]) and np.isnan(final_lowerband[-3]) and not np.isnan(final_upperband[-3]) ) )
					supertrend_signal="Buy"
				# New buy logic for 1hr	
				elif intrval=="1hr" and np.isnan(final_upperband[-1]) and np.isnan(final_upperband[-2]) and np.isnan(final_upperband[-3]) and not np.isnan(final_upperband[-4]) and not np.isnan(final_lowerband[-1]) and not np.isnan(final_lowerband[-2]) and not np.isnan(final_lowerband[-3]) and np.isnan(final_lowerband[-4]):
					supertrend_signal="Buy"
				elif intrval=="1hr" and (not np.isnan(final_lowerband[-1]) and np.isnan(final_lowerband[-2]) and not np.isnan(final_upperband[-2])) or (not np.isnan(final_lowerband[-2]) and np.isnan(final_lowerband[-3]) and not np.isnan(final_upperband[-3])) or (not np.isnan(final_lowerband[-3]) and np.isnan(final_lowerband[-4]) and not np.isnan(final_upperband[-4])) or (not np.isnan(final_lowerband[-3]) and not np.isnan(final_lowerband[-4]) and (abs(final_lowerband[-3]-final_lowerband[-4])<0.001) and not np.isnan(final_upperband[-5])) or (not np.isnan(final_lowerband[-3]) and not np.isnan(final_lowerband[-4]) and not np.isnan(final_lowerband[-5]) and (abs(final_lowerband[-3]-final_lowerband[-4])<0.001) and (abs(final_lowerband[-4]-final_lowerband[-5])<0.001) and not np.isnan(final_upperband[-6])) or (not np.isnan(final_lowerband[-3]) and not np.isnan(final_lowerband[-4]) and not np.isnan(final_lowerband[-5]) and not np.isnan(final_lowerband[-6]) and (abs(final_lowerband[-3]-final_lowerband[-4])<0.001) and (abs(final_lowerband[-4]-final_lowerband[-5])<0.001) and (abs(final_lowerband[-5]-final_lowerband[-6])<0.001) and not np.isnan(final_upperband[-7])):
					supertrend_signal="Buy"	
				else:
					supertrend_signal="Mixed"
			except:
				print('problems at line 370')

		return supertrend_signal

	def Resistance(self,some_symbol, tv=tv0):
		american=["NASDAQ", "NYSE", "Arca", "OTC", "DJ", "SP", "CBOE", "CBOT", "CME GLOBEX", "COMEX", "NYMEX", "ICEUS", "FairX", "ECONOMY"]

		exch=tv.search_symbol(some_symbol)[0]['exchange']

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

		df=tv.get_hist(some_symbol, exchange=exch, interval = Interval.in_weekly, n_bars=500, extended_session=False)
		df=df[df.index > dateutil.parser.parse("2020-01-01")]

		try:
			today_open=df.iloc[-1]['open']
			today_close=df.iloc[-1]['close']
			today_max=max(today_open,today_close)

			df_x=df.drop(df.tail(1).index,inplace=False)
			close = df_x['close']
			open = df_x['open']
			volume = df_x['volume']

			volume_spike=df_x['volume'].max()
			volume_prev_day=df_x[df_x.index==df_x['volume'].shift(-1).idxmax()]['volume'][0]

			spike_open=df_x[df_x['volume']==volume_spike]['open'][0]
			spike_close=df_x[df_x['volume']==volume_spike]['close'][0]
		except:
			prefix=tv.search_symbol(some_symbol)[0]['prefix']
			
			try:
				df=tv.get_hist(some_symbol, exchange=prefix, interval = Interval.in_weekly, n_bars=500, extended_session=False)
				df=df[df.index > dateutil.parser.parse("2020-01-01")]
				today_open=df.iloc[-1]['open']
				today_close=df.iloc[-1]['close']
				today_max=max(today_open,today_close)

				df_x=df.drop(df.tail(1).index,inplace=False)
				close = df_x['close']
				open = df_x['open']
				volume = df_x['volume']

				volume_spike=df_x['volume'].max()
				volume_prev_day=df_x[df_x.index==df_x['volume'].shift(-1).idxmax()]['volume'][0]
				spike_open=df_x[df_x['volume']==volume_spike]['open'][0]
				spike_close=df_x[df_x['volume']==volume_spike]['close'][0]
			
			except:
				pass


		try:
			if round(volume_spike/volume_prev_day,0)>=50:
				resistance=max(spike_open,spike_close)
				if today_max>resistance:
					resistance_crossed=True
				else:
					resistance_crossed=False
			else:
				resistance_crossed=False
		except:
			resistance_crossed=False
			pass

		return resistance_crossed


	def HH(self,fin_upp, df_open, df_close, df_high):
		nan_mask = fin_upp.isna()
		nan_groups = nan_mask.diff().fillna(0).cumsum()
		nan_groups = nan_groups[nan_mask]
		five_hour_alert=False

		if not nan_groups.empty:
			last_group = nan_groups.groupby(nan_groups).last()
			last_group_index = last_group.index[-1]
			start_index = nan_groups[nan_groups == last_group_index].index[1] #because TradingView puts "My Long Entry" 1 bar after actual green Supertrend
			diff=df_close[start_index:]-df_open[start_index:]
			end_index=diff[diff < 0].index.min()

		highest_high=max(df_high[start_index:end_index])
		end_green=nan_groups[nan_groups == last_group_index].index[-1]
		all_highs_of_green_curve=df_high[start_index:end_green]

		try:
			if np.isnan(fin_upp[-1]) and np.isnan(fin_upp[-2]):
				if max(all_highs_of_green_curve)-highest_high>0:
					if (all_highs_of_green_curve.idxmax()-start_index).days<=5:
						if (df_high.index[-1]-all_highs_of_green_curve.idxmax()).days<=5:
								#ALERT!!!
								five_hour_alert=True
								print("ALERT	ON 5-HOUR CHART!!!!!")
						else:
							five_hour_alert=False
			else:
				five_hour_alert=False
		except:
			five_hour_alert=False

		return five_hour_alert



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
		infolist4 = []
		infolist5 = []
		infolist_5H=[]
		infolist_5HX=[]

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
			# Adding new 1 hr
			try:
				signal_1hr=self.Supertrend(stockSymbol,"1hr")
			except:
				signal_1hr=""
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
				signal_5hr=self.Supertrend(stockSymbol,"5hr_")
			except:
				signal_5hr=""	
			try:
				signal_5hr_exs=self.Supertrend(stockSymbol,"5hr_ExS")
			except:
				signal_5hr_exs=""

			try:
				if signal_5hr=="5H_ALERT":
					infolist_5H.append(stockSymbol)
				elif signal_5hr_exs=="5H_ExS_ALERT":
					infolist_5HX.append(stockSymbol)
			except:
				pass


			try:
				if ( (stockSymbol.lower() in docfile_list) or (stockSymbol.upper() in docfile_list) ):	
					infolist2.append(stockSymbol)
			except:
				pass

			try:
				if self.Resistance(stockSymbol)==True:
					infolist5.append(stockSymbol)
			except:
				pass

			print(stockSymbol, end = ' ')
			print(signal_4hr, end = ' ')
			print(signal_1d, end = ' ')
			print(signal_1w, end = ' ')
			print("signal_2d:",signal_2d, "||||",end = ' ')
			print(signal_10weeks)
			#signal_4hr=="Sell" or
			#signal_1d=="Sell" or 
			if  signal_1w=="Sell" or signal_10weeks=="Sell":
				infolist.append(stockSymbol)
			
			if  signal_1w=="Buy":
				infolist3.append(stockSymbol)

			if  signal_2d=="Buy":
				infolist4.append(stockSymbol)



		print("______________________")
		print("______________________")
		print("BUY 1wBuy INFOLIST3=", infolist3)
		print("BUY 2dBuy INFOLIST4=", infolist4)
		print("______________________")
		print("______________________")
		print('Resistance crossed for:', infolist5)

		if infolist!=[]:
			infolist=list(set(infolist))
			#infolist=["*"]
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
			server.login("high.risk.stocks@gmail.com", "qhyhtfschqvsbwla")
			print("SUCCESS at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block___')
			
			server.quit()
		
		if infolist2!=[]:
			infolist2=list(set(infolist2))
			#infolist2=["*"]
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
			server.login("high.risk.stocks@gmail.com", "qhyhtfschqvsbwla")
			print("SUCCESS2 at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block2___')

			# Send SMS
			sms_text = f'Cross referenced with doc file: {mail_content}'
			send_sms(from_=from_, to=to, body=sms_text)
			
			server.quit()
		
		#1W Buy
		if infolist3!=[]:
			infolist3=list(set(infolist3))
			#infolist3=["*"]
			mail_content = "Stock Symbol\n"
			for sym in infolist3:
				mail_content += f"{sym}\n"
			print('___entered if block___')
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = 'Buy signal for 1W timeframe'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['high.risk.stocks@gmail.com', 'mike@mihfinancial.ca']
			msg['To'] = ", ".join(recipients)
			# Send the message via our own SMTP server.
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "qhyhtfschqvsbwla")
			print("SUCCESS3 at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block2___')
			
			server.quit()

		#2D buy
		if infolist4!=[]:
			infolist4=list(set(infolist4))
			#infolist4=["*"]
			mail_content = "Stock Symbol\n"
			for sym in infolist4:
				mail_content += f"{sym}\n"
			print('___entered if block___')
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = 'Buy signal for 2D timeframe'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['high.risk.stocks@gmail.com', 'mike@mihfinancial.ca']
			msg['To'] = ", ".join(recipients)
			# Send the message via our own SMTP server.
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "qhyhtfschqvsbwla")
			print("SUCCESS4 at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block2___')
			
			server.quit()

		#Resistance crossed notification
		if infolist5!=[]:
			infolist5=list(set(infolist5))
			#infolist4=["*"]
			mail_content = "Stock Symbol\n"
			for sym in infolist5:
				mail_content += f"{sym}\n"
			print('___entered if block___')
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = 'Resistance crossed signal for the following stocks'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['high.risk.stocks@gmail.com', 'mike@mihfinancial.ca']
			msg['To'] = ", ".join(recipients)
			# Send the message via our own SMTP server.
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "qhyhtfschqvsbwla")
			print("SUCCESS5 at log into high.risk.stocks")
			server.send_message(msg)
			
			print('___exited if block2___')
			
			server.quit()

		if infolist_5H!=[]:
			infolist_5H=list(set(infolist_5H))
			mail_content = "Stock Symbol\n"
			for sym in infolist_5H:
				mail_content += f"{sym}\n"
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = '5H High (REGULAR hours) crossed for the following stocks'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['high.risk.stocks@gmail.com', 'mike@mihfinancial.ca']
			msg['To'] = ", ".join(recipients)
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "qhyhtfschqvsbwla")
			server.send_message(msg)
			server.quit()

		if infolist_5HX!=[]:
			infolist_5HX=list(set(infolist_5HX))
			mail_content = "Stock Symbol\n"
			for sym in infolist_5HX:
				mail_content += f"{sym}\n"
			msg = EmailMessage()
			msg.set_content(mail_content)
			msg['Subject'] = '5H High (EXTENDED hours) crossed for the following stocks'
			msg['From'] = 'high.risk.stocks@gmail.com'
			recipients = ['high.risk.stocks@gmail.com', 'mike@mihfinancial.ca']
			msg['To'] = ", ".join(recipients)
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("high.risk.stocks@gmail.com", "qhyhtfschqvsbwla")
			server.send_message(msg)
			server.quit()

		print("=======")


bet = StockStatusBot(Config())
