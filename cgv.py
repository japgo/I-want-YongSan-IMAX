from selenium import webdriver
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import slack_token
import slack_sdk

BOT_ID, BOT_TOKEN, CHANNEL_NAME = slack_token.get_bot_id_and_token_and_channel()
bot = slack_sdk.web.client.WebClient( token = BOT_TOKEN )
resp = bot.conversations_list()
channel_list = resp[ 'channels' ]
for channel in channel_list :
	# print( "channel : ", channel )
	if channel[ 'name' ] == CHANNEL_NAME :
		ch_info = channel

ch_id = ch_info[ 'id' ]


GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

local_test = False # False True

options = webdriver.ChromeOptions()
# url = 'http://www.cgv.co.kr/ticket/?MOVIE_CD=20027683&MOVIE_CD_GROUP=20027683'
url = 'http://www.cgv.co.kr/ticket/?MOVIE_CD=20027596&MOVIE_CD_GROUP=20027596'
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")


if local_test :
	driver = webdriver.Chrome( './chromedriver.exe', options=options )
	driver.get( url )

else:
	chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
	options.binary_location = chrome_bin
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
	driver.get( url )


#ticket_iframe = driver.find_element( by=By.CSS_SELECTOR, value="iframe[id='ticket_iframe']")
ticket_iframe = WebDriverWait( driver, 5 ).until( EC.visibility_of_element_located( ( By.CSS_SELECTOR, "iframe[id='ticket_iframe']" ) ) )
driver.switch_to.frame( ticket_iframe )
theater_area_list = driver.find_element( by=By.CSS_SELECTOR, value="div[id='theater_area_list']" )
time.sleep( 10 )
#yongsan = theater_area_list.find_element( by=By.CSS_SELECTOR, value="li[data-index='119']" )
yongsan = WebDriverWait( driver, 5 ).until( EC.element_to_be_clickable( ( By.CSS_SELECTOR, "li[data-index='118']" ) ) )
yongsan.click()


date_list = driver.find_element( by=By.CSS_SELECTOR, value="div[id='date_list']")
time.sleep( 1 )
IwantThisDay = date_list.find_element( by=By.CSS_SELECTOR, value="li[date='20211222']" )
#IwantThisDay = WebDriverWait( date_list, 5 ).until( EC.element_to_be_clickable( ( By.CSS_SELECTOR, "li[date='20211113']" ) ) )

while True:
	try:
		IwantThisDay.click()
		
		section_section_time = driver.find_element( by=By.CSS_SELECTOR, value="div[class='section section-time']" )
		col_body = section_section_time.find_element( by=By.CSS_SELECTOR, value="div[class='col-body']" )
		time.sleep( 2 )
		content_scroll_y = col_body.find_element( by=By.CSS_SELECTOR, value="div[class='content scroll-y']" )
		theaters = content_scroll_y.find_elements( by=By.CSS_SELECTOR, value="div[class='theater']" )
		for theater in theaters :
				name = theater.find_element( by=By.CSS_SELECTOR, value="span[class='name']" )
				print( name.text )
				if( str( name.text ).find( "IMAX" ) >= 0 ):
					count = theater.find_element( by=By.CSS_SELECTOR, value="span[class='count']" )
					time.sleep( 1 )
					print( f"count:{count.text}, day:{IwantThisDay.text}" )
	
					if( str( count.text ).find( "매진" ) >= 0 ):
						continue
 
					if( str( count.text ).find( "석" ) >= 0 ):
						str_cnt = str( count.text ).replace( "석", "" )
						int_cnt = int( str_cnt )
						if( 3 < int_cnt and int_cnt < 624 ):
							bot.chat_postMessage( channel=ch_id, text="떳다 IMAX!!!!! @wonyong.lee @goldjix " + name.text )

	except Exception as ex:
		print( repr( ex ) )
		
	print( "searching IMAX..." )
	time.sleep( 5 )