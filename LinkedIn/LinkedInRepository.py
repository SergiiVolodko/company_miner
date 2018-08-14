# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# from company_miner.common.BrowserFactory import BrowserFactory
# from company_miner.LinkedIn.LinkedAuthorizationService import LinkedAuthorizationService

from linkedin import linkedin
from time import sleep
import random

class LinkedInRepository:

    application = {}

    def __init__(self, linkedin_application):
        self.application = linkedin_application

    def find_company_by_name(self, company_name):
        sleep(random.random() / 3)
        selectors=[{'companies': ['id', 'name', 'website-url', 'universal-name', 'type', 'specialties']}] #'universal-name','size', 'description'
        response = self.application.search_company(selectors = selectors, params={'keywords': company_name})
        #print response;
        if response['companies']['_total'] == 0:
            return None
        companies = response['companies']['values']

        return None if len(companies)<0 else companies[0]

# if __name__ == "__main__":
#     browser = BrowserFactory.create()

#     linkedin_email = "volodkony@gmail.com"
#     linkedin_pass = "Austin1989"
#     api_key = "7740mhgfaxg07m"
#     api_secret = "xh7SowgeS13gRN34"
#     token = LinkedAuthorizationService(browser).refresh_token(api_key, api_secret, linkedin_email, linkedin_pass)

#     application = linkedin.LinkedInApplication(token=token)
#     repo = LinkedInRepository(application)
#     #print repo.find_company_by_name("Microsoft")
#     print(repo.find_company_by_name("Exact"))
