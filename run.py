import os
from requests import get
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import json

class AMFBot:
    def __init__(self, twitter_user, twitter_pwd):
        self.twitter_user = twitter_user
        self.twitter_pwd = twitter_pwd
        self.options = Options()
        self.options.add_argument("--lang=en")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def open(self):
        bot = self.bot
        bot.get("https://www.like4like.org/")
        print("Opened the browser.")
        bot.execute_script("document.body.style.zoom='50%'")
        # Load the cookies from the JSON file
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
        # Add the cookies to the non-headless browser
        for cookie in cookies:
            bot.add_cookie(cookie)
        time.sleep(3)
        # Refresh the page
        bot.refresh()
        print("Refreshed the page.")
        time.sleep(3)
        self.twtlk()

    def twtlk(self):
        bot = self.bot
        bot.get("https://www.like4like.org/free-twitter-followers.php")
        bot.execute_script("document.body.style.zoom='50%'")
        print("Opened the website.")
        time.sleep(8)
        while True:
            try:
                bot.find_element(By.CSS_SELECTOR, "a[class^='cursor earn_pages_button profile_view_img']").click()
                print("Clicked on the element.")
                time.sleep(3)
                bot.switch_to.window(bot.window_handles[1])
                break
            except Exception as e:
                print("Element not found. Refreshing the page and trying again.")
                bot.refresh()
                time.sleep(3)

        # window
        try:
            log_btn = WebDriverWait(bot, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="button"]//span[text()="Log in"]'))
            )
            if log_btn.is_displayed():
                log_btn.click()
                print("Clicked on the login button.")
                usuario = WebDriverWait(bot, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
                )
                usuario.send_keys(self.twitter_user)
                bot.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]').click()
                print("Entered Twitter username and clicked Next.")
                time.sleep(3)
                senha = bot.find_element(By.XPATH, "//input[@type='password']")
                senha.send_keys(self.twitter_pwd)
                bot.find_element(By.XPATH, '//div[@role="button" and @data-testid="LoginForm_Login_Button"]').click()
                follow = WebDriverWait(bot, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="button" and @data-testid="confirmationSheetConfirm"]'))
                )
                if follow.is_displayed():
                    follow.click()
                    print("Clicked on the confirmation button.")
                time.sleep(8)
            else:
                follow = bot.find_element(By.XPATH, '//div[@role="button" and @data-testid="confirmationSheetConfirm"]')
                if follow.is_displayed():
                    follow.click()
                    print("Clicked on the confirmation button.")
                time.sleep(8)

        except Exception as e:
            bot.close()
            bot.switch_to.window(bot.window_handles[0])
            time.sleep(8)
            bot.get("https://www.like4like.org/free-twitter-followers.php")
            bot.execute_script("document.body.style.zoom='50%'")
            print("Refreshed the page after an exception.")
            self.twttwo()

        # window
        bot.close()
        bot.switch_to.window(bot.window_handles[0])
        time.sleep(3)
        self.twttwo()

    def twttwo(self):
        bot = self.bot
        confirm = bot.find_element(By.CSS_SELECTOR, "a[class^='cursor pulse-checkBox']")
        if confirm.is_displayed():
            confirm.click()
            print("Clicked on the confirmation checkbox.")
            time.sleep(3)
            bot.find_element(By.CSS_SELECTOR, "a[class^='cursor earn_pages_button profile_view_img']").click()
            bot.switch_to.window(bot.window_handles[1])
            print("Clicked on the element in the second window.")
        else:
            bot.find_element(By.CSS_SELECTOR, "a[class^='cursor earn_pages_button profile_view_img']").click()
            bot.switch_to.window(bot.window_handles[1])
            time.sleep(8)
            print("Clicked on the element in the second window.")

        while True:
            try:
                follow = WebDriverWait(bot, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="button" and @data-testid="confirmationSheetConfirm"]'))
                )
                if follow.is_displayed():
                    follow.click()
                    print("Clicked on the confirmation button.")
                time.sleep(8)
                break
            except Exception as e:
                print("Element not found. Refreshing the page and trying again.")
                bot.refresh()
                time.sleep(3)

        # window
        bot.close()
        bot.switch_to.window(bot.window_handles[0])
        time.sleep(3)
        self.twttwo()

twitter_user = 'a'
twitter_pwd = '@a'
ed = AMFBot(twitter_user, twitter_pwd)
ed.open()

