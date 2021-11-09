from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome Driver를 이용하여 그룹웨어 접근.
options = webdriver.ChromeOptions()
# options.add_argument('--headless') # 창 없는 모드 ( no window )
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome( './chromedriver.exe', options=options )
url = 'http://www.cgv.co.kr/ticket/?MOVIE_CD=20027683&MOVIE_CD_GROUP=20027683'
driver.get( url )
print( driver.page_source )
# //*[@id="theater_area_list"]/ul/li[1]/div/ul/li[24]/a/text()
# <a href="#" onclick="theaterListClickListener(event);return false;">용산아이파크몰<span class="sreader"></span></a>
# theater_area_list > ul > li.selected > div > ul > li:nth-child(24) > a
# document.querySelector("#theater_area_list > ul > li.selected > div > ul > li:nth-child(24) > a")

ticket_iframe = driver.find_element( by=By.CSS_SELECTOR, value="iframe[id='ticket_iframe']")
driver.switch_to.frame( ticket_iframe )
theater_area_list = driver.find_element( by=By.CSS_SELECTOR, value="div[id='theater_area_list']" )
yongsan = theater_area_list.find_element( by=By.CSS_SELECTOR, value="li[data-index='119']" )
yongsan.click()

date_list = driver.find_element( by=By.CSS_SELECTOR, value="div[id='date_list']")
IwantThisDay = date_list.find_element( by=By.CSS_SELECTOR, value="li[date='20211113']" )
IwantThisDay.click()

time_list_nano = driver.find_element( by=By.CSS_SELECTOR, value="div[class='section section-time']" )


time.sleep( 3 )