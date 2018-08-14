from linkedin import linkedin
from time import sleep
#from company_miner.common.BrowserFactory import BrowserFactory
from company_miner.common.JsonRepository import JsonRepository
from company_miner.common.HtmlHelper import HtmlHelper
import json
from selenium.webdriver.common.by import By

class LinkedAuthorizationService:
    browser = {}

    def __init__(self, auth_browser):
        self.browser = auth_browser

    # def get_token(self):
    #     stored_token = JsonRepository.load("token.json")
    #     if self.is_valid(stored_token):
    #         return stored_token['access_token']
    #     token = self.refresh_token()
    #     print("Saving token...")
    #     JsonRepository.save(token, "token.json")
    #     return token.access_token

    # def is_valid(self, token_json):
    #     if(token_json == None):
    #         print("No token json")
    #         return False
    #     try:
    #         print("Validating access token...")
    #         token = token_json['access_token']
    #         self.browser.get("https://www.linkedin.com/profile/view?id=sergey-volodko-a87960a9&authType=name&authToken={0}".format(token))
    #         resp_content = HtmlHelper.remove_all_tags(self.browser.page_source)
    #         sleep(10)
    #         if not "volodko" in resp_content.lower():
    #             print("Token is valid")
    #             return True            
    #         return False
    #     except Exception as e:
    #         print(e)
    #         return False

    def refresh_token(self, api_key, api_secret, linkedin_email, linkedin_pass):
        print("Refreshing the token...")
        RETURN_URL = "https://localhost:8000"

        authentication = linkedin.LinkedInAuthentication(api_key, api_secret, RETURN_URL, ['w_share'])
        print("Navigating to authorization url")
        self.browser.get(authentication.authorization_url)
        sleep(2)
        #raw_input("Please allow access manually and press Enter to continue...")
        print("Logging in")
        self.perform_login(linkedin_email, linkedin_pass)

        print("Extracting code")
        url = self.browser.current_url
        start = 'code='
        end = '&state='
        code = url[url.find(start)+len(start):url.find(end)]
        #print code
        authentication.authorization_code = code
        print("Getting the token")
        return authentication.get_access_token()

    def perform_login(self, linkedin_email, linkedin_pass):
        if(self.is_submit_page()):
            print("Fast login")
            try:
                self.browser.find_element_by_id("oauth__auth-form__submit-btn").click()
            except:
                pass
        else:
            print("Proper login")
            self.browser.find_element_by_name("session_key").clear()
            self.browser.find_element_by_name("session_key").send_keys(linkedin_email)
            self.browser.find_element_by_name("session_password").send_keys(linkedin_pass)
            
            print("Submitting form")
            sleep(1)
            try:
                self.browser.find_element_by_name("signin").click()          
                if(self.is_submit_page()):
                    self.browser.find_element_by_id("oauth__auth-form__submit-btn").click()
            except:
                pass

    def is_submit_page(self):
        sleep(2)
        submit_buttons = self.browser.find_elements(By.XPATH, "//button[@id='oauth__auth-form__submit-btn']")
        print("Submit buttons :", len(submit_buttons))
        return len(submit_buttons) > 0