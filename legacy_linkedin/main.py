import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import string
from company_miner.common.BrowserFactory import BrowserFactory
from company_miner.common.CsvRepository import CsvRepository
from company_miner.common.JsonRepository import JsonRepository
from company_miner.LinkedIn.LinkedAuthorizationService import LinkedAuthorizationService
from company_miner.LinkedIn.LinkedInRepository import LinkedInRepository
from linkedin import linkedin
import datetime

dir_name = os.path.dirname(os.path.abspath(__file__))

def mine(credentials, csv_file):
    start_time = datetime.datetime.now()
    print("----- Loading companies from CSV...", start_time.time())
    data = CsvRepository.load_only_first_column(csv_file, "name")
    #print(data[42])
    linkedin_email = credentials["linkedin_email"]
    linkedin_pass = credentials["linkedin_pass"]
    apps = credentials["apps"]
    api_apps = [
                {'api_key':apps[0]['api_key'],'api_secret':apps[0]['api_secret'], 'from_i':0, 'to_i': 500},
                {'api_key':apps[1]['api_key'],'api_secret':apps[1]['api_secret'], 'from_i':500, 'to_i': 1000},
                {'api_key':apps[2]['api_key'],'api_secret':apps[2]['api_secret'], 'from_i':1000, 'to_i': 1500},
                {'api_key':apps[3]['api_key'],'api_secret':apps[3]['api_secret'], 'from_i':1500, 'to_i': 2000},
                {'api_key':apps[4]['api_key'],'api_secret':apps[4]['api_secret'], 'from_i':2000, 'to_i': 2500},
                {'api_key':apps[5]['api_key'],'api_secret':apps[5]['api_secret'], 'from_i':2500, 'to_i': 3000},
                {'api_key':apps[6]['api_key'],'api_secret':apps[6]['api_secret'], 'from_i':3000, 'to_i': 3500},
                {'api_key':apps[7]['api_key'],'api_secret':apps[7]['api_secret'], 'from_i':3500, 'to_i': 4000},
                {'api_key':apps[8]['api_key'],'api_secret':apps[8]['api_secret'], 'from_i':4000, 'to_i': 4500},
                {'api_key':apps[9]['api_key'],'api_secret':apps[9]['api_secret'], 'from_i':4500, 'to_i': 5000},
                {'api_key':apps[10]['api_key'],'api_secret':apps[10]['api_secret'], 'from_i':5000, 'to_i': 5500},
                ]
    total_found = 0
    for app in api_apps:
        from_i = app['from_i']
        to_i =  app['to_i']
        print("----- Fetching companies between:", from_i, to_i, datetime.datetime.now() - start_time)
        data_chunk = data[from_i:to_i]
        companies = fetch_companies(data_chunk, linkedin_email, linkedin_pass,app['api_key'], app['api_secret'], from_i)
        file_name = "found_companies({0}-{1})[{2}].csv".format(from_i, to_i, len(companies))
        result_file = os.path.join(dir_name, "data_mining", file_name)
        total_found += len(companies)
        CsvRepository.save(companies, result_file)

    print("Total found :", total_found)
    print("Script completed.", datetime.datetime.now() - start_time)


def fetch_companies(data, linkedin_email, linkedin_pass, api_key, api_secret, index_shift):   
    sample = []
    i = 0
    not_on_linkedin_count = 0
    no_specialties_count = 0

    try:
        print("----- Authorizing to Linkedin api...")
        linkedin_repo = reinit_linkedin_repo(linkedin_email, linkedin_pass, api_key, api_secret)

        print("----- Searching companies...")
        printable = set(string.printable)
        for company_name in data:
            i += 1
            if(i % 100 is 0):
                print("Searching... Processed : {}, Not found {}, Collected {}".format(i, not_on_linkedin_count, len(sample)))

            try:
                linkedin_data = linkedin_repo.find_company_by_name(company_name)
            except Exception as ex:
                print(ex)
                linkedin_repo = reinit_linkedin_repo(linkedin_email, linkedin_pass, api_key, api_secret)
                linkedin_data = linkedin_repo.find_company_by_name(company_name)

            if linkedin_data is None:
                not_on_linkedin_count += 1
                continue

            company = {}
            linkedin_name = linkedin_data['name'] if 'name' in linkedin_data.keys() else None
            linkedin_name = "".join([с for с in linkedin_name if с in printable])
            company['linkedin_name'] = linkedin_name
            company['linkedin_url'] = "www.linkedin.com/company/"+str(linkedin_data['id']) if 'id' in linkedin_data.keys() else None
            company['website'] = linkedin_data['websiteUrl'] if 'websiteUrl' in linkedin_data.keys() else None

            if not 'specialties' in linkedin_data.keys() or linkedin_data['specialties']['_total'] == 0:
                no_specialties_count += 1
                continue
            
            company_specialties_words = (' '.join(linkedin_data['specialties']['values'])).lower().split()
            software_specialties = ["software", "technology", "investment", "cloud", "data"]
            intercetions = list(set(company_specialties_words) & set(software_specialties))
            if  len(intercetions) > 0:
                company['specialties'] = " ".join(intercetions)
                print(company)
                sample.append(company)
    except :
        print("Failed at: ", index_shift + i)
        raise
    finally :
        print("Total processed : ", i)
        print("Not found count : ", not_on_linkedin_count)        
        print("No specialties count : ", no_specialties_count)
        print("Sample size : ", len(sample))
        return sample

def reinit_linkedin_repo(linkedin_email, linkedin_pass, api_key, api_secret):
    browser = BrowserFactory.create()
    auth_service = LinkedAuthorizationService(browser)
    token = auth_service.refresh_token(api_key, api_secret, linkedin_email, linkedin_pass)
    browser.quit()
    application = linkedin.LinkedInApplication(token=token)
    return LinkedInRepository(application)

if __name__ == "__main__":
    creds_file = os.path.join(dir_name, "linkedin_credentials.json")
    caredentials = JsonRepository.load(creds_file)

    csv_file = os.path.join(dir_name, "data_mining", "london_companies.csv")
    mine(caredentials, csv_file)