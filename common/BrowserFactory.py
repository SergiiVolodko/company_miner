from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile

class BrowserFactory:
    @staticmethod
    def create():
        gecko_path = "C:\\Tools\\geckodriver.exe"

        browser = webdriver.Firefox(executable_path=gecko_path)
        browser.set_page_load_timeout(90)

        return browser