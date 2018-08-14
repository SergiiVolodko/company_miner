import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from company_miner.common.CsvRepository import CsvRepository

if __name__ == "__main__":
    print("Script started")
    all_companies = []
    current_folder = os.path.dirname(__file__)
    folder = os.path.join(current_folder, "Fetched-software-technology-investment-data")
    for filename in os.listdir(folder):
        print(filename)
        companies = CsvRepository.load(os.path.join(folder, filename))
        all_companies += companies

    print("Total loaded companies", len(all_companies))

    result_file = os.path.join(current_folder, "Fetched-software-technology-investment-data.csv")
    CsvRepository.save(all_companies, result_file)

    print("Script completed.")