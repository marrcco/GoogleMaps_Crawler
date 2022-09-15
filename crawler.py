import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import configparser
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import json


class GMapsCrawler:
    IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

    # storing all XPATHS and PATHS values in config.ini file so it's easier to keep it updated if XPATHs changes
    config = configparser.ConfigParser()
    config.read("config.ini")
    ALL_OBJECTS_DIV_XPATH = config["gmaps_crawler"]["all_objects_div_xpath"]
    DRIVER_XPATH = config["gmaps_crawler"]["chrome_driver_path"]
    NEXT_PAGE_BUTTON = config["gmaps_crawler"]["next_page_button_xpath"]
    TITLE_XPATH = config["gmaps_crawler"]["object_title_xpath"]
    GMAPS_LOC_XPATH = config["gmaps_crawler"]["gmaps_location_xpath"]
    RATING_XPATH = config["gmaps_crawler"]["rating_xpath"]
    REVIEWS_XPATH = config["gmaps_crawler"]["reviews_xpath"]
    WEBSITE_URL_XPATH = config["gmaps_crawler"]["website_url_xpath"]


    def __init__(self,list_of_objects=[]):
        self.list_of_objects = list_of_objects


    # function setting up selenium webdriver
    def selenium_setup(self):
        option = Options()
        option.headless = True
        option.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(self.DRIVER_XPATH,options=option)
        return driver

    # function crawl object takes gmaps object(location) as input and scrapes data about selected object such as:
    # object name, gmaps location, rating, reviews, website url
    # and it stores it in dictionary
    def crawl_object(self,object_div):
        try:
            object_name = object_div.find_element_by_xpath(self.TITLE_XPATH).get_attribute("innerHTML")
        except:
            object_name = ""

        try:
            gmaps_location = object_div.find_element_by_xpath(self.GMAPS_LOC_XPATH).get_attribute("data-url")
            gmaps_location = f"https://www.google.com{gmaps_location}"
        except:
            gmaps_location = ""

        try:
            rating = object_div.find_element_by_xpath(self.RATING_XPATH).get_attribute("innerHTML")
        except:
            rating = ""

        try:
            reviews = object_div.find_element_by_xpath(self.REVIEWS_XPATH).get_attribute("innerHTML")
        except:
            reviews = ""

        try:
            website_url = object_div.find_element_by_xpath(self.WEBSITE_URL_XPATH).get_attribute("href")
        except:
            website_url = ""

        object_dict = {
            "name": object_name,
            "rating": rating,
            "reviews" : reviews,
            "website": website_url,
            "gmaps_location": gmaps_location
        }
        return object_dict

    # function crawl page takes gmaps list url as input and it loops through all locations and pages
    # and it calls crawl_object() function in order to scrape each location/object
    # it stores all data in list_of_objects list
    def crawl_page(self,url):
        driver = self.selenium_setup()
        driver.get(url)
        driver.implicitly_wait(5)

        next_page_exists = True
        while(next_page_exists):
            all_objects_div = WebDriverWait(driver,5,ignored_exceptions=self.IGNORED_EXCEPTIONS).until(EC.presence_of_all_elements_located((By.XPATH, self.ALL_OBJECTS_DIV_XPATH)))
            for object_div in all_objects_div:
                object_dict = self.crawl_object(object_div)
                print(object_dict)
                self.list_of_objects.append(object_dict)
            try:
                WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, self.NEXT_PAGE_BUTTON))).click()
                time.sleep(5)

            except:
                next_page_exists = False
        return self.list_of_objects

    # function transform_to_dataframe() converts list_of_objects list into pandas Dataframe
    def transform_to_dataframe(self):
        if(len(self.list_of_objects) > 0):
            df = pd.DataFrame(self.list_of_objects)
        else:
            raise Exception("Crawler did not scrape anything.\nTry calling crawl_page() function again")
        return df


    # function transform_to_json() converts list_of_objects list into JSON object
    def transform_to_json(self):
        if(len(self.list_of_objects) > 0):
            json_file = json.dumps(self.list_of_objects, indent=1)
        else:
            raise Exception("Crawler did not scrape anything.\nTry calling crawl_page() function again")
        return json_file



crawler = GMapsCrawler()
crawler.crawl_page("https://www.google.com/search?rlz=1C5CHFA_enRS980RS980&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2&tbm=lcl&q=tennis%20courts%20in%20netherlands&rflfq=1&num=10&sa=X&ved=2ahUKEwi_2c7l6pP6AhUKYPEDHeb5DQEQjGp6BAgLEAE&biw=1440&bih=704&dpr=2&rlst=f#rlfi=hd:;si:;mv:[[52.438552699999995,5.1060174],[51.489187799999996,4.5038522]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2")
df = crawler.transform_to_dataframe()
json = crawler.transform_to_json()