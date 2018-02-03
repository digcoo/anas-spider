#encoding=utf-8

import traceback
import csv
import os
import jsonpickle as json

class FileUtils:

    @staticmethod
    def list_to_csv(data_array, csv_file_path, file_name):
	if not os.path.exists(csv_file_path):
	    os.makedirs(csv_file_path)
	csv_file = open(csv_file_path + '/' + file_name, 'wb')
	writer = csv.writer(csv_file)
	for line_data in data_array:
	    writer.writerow(line_data)
	csv_file.close()

