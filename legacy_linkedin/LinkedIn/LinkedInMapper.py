import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from company_miner.common.Utils import Utils
from company_miner.LinkedIn.LinkedInIndustries import *

class LinkedInMapper:
    @staticmethod
    def map_to_company(linkedin_data):
        company = {}
        linkedin_name = linkedin_data['name'] if 'name' in linkedin_data.keys() else None
        linkedin_name = Utils.to_only_letters_string(linkedin_name)
        company['linkedin_name'] = linkedin_name
        company['linkedin_url'] = "www.linkedin.com/company/"+str(linkedin_data['id']) if 'id' in linkedin_data.keys() else None
        company['linkedin_size'] = linkedin_data['size'] if 'size' in linkedin_data.keys() else None
        company['linkedin_website'] = linkedin_data['websiteUrl'] if 'websiteUrl' in linkedin_data.keys() else None
        company['description'] = Utils.to_only_letters_string(linkedin_data['description']) if 'description' in linkedin_data.keys() else None
        company['specialties'] = ""
        specialties = linkedin_data['specialties'] if 'specialties' in linkedin_data.keys() else None
        if not specialties is None:
            company['specialties'] = Utils.to_only_letters_string(" ".join(specialties['values']))

        company['industry'] = ""
        industries = linkedin_data['industries'] if 'industries' in linkedin_data.keys() else None
        if not industries is None:
            industry_code = str(industries["values"][0]["code"])
            company['industry'] = linkedin_industries[industry_code]

        return company