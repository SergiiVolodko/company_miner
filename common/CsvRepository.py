import csv
from itertools import zip_longest
import unicodecsv
from os import path

class CsvRepository:
    @staticmethod
    def save_dict_of_arrays(data_as_dict_of_arrays, file_path):
        keys = data_as_dict_of_arrays.keys()
        with open(file_path, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(keys)
            for each in zip_longest(*data_as_dict_of_arrays.values()):
                w.writerow(each)

    @staticmethod
    def save(input_list, file_path):
        if len(input_list) == 0:
            print("Nothing to save - the list is empty", file_path)
            return

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            fields = list(input_list[0].keys())
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(input_list)

    @staticmethod
    def load(file_path):
        if not path.exists(file_path):
            raise Exception("No file", file_path)

        result = []
        with open(file_path, "r", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_values in reader:
                result.append(row_values)
            print("Count of loaded rows : ", len(result))
        return result

    @staticmethod
    def load_only_one_column(file_path, column_name):
        if not path.exists(file_path):
            raise Exception("No file", file_path)

        result = []
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            for row_values in reader:
                value = row_values[column_name]
                result.append(value)
            print("Count of loaded rows : ", len(result))
        return result