
import os
import pandas as pd
from time import sleep
from datetime import datetime, timedelta
from pymongo import MongoClient


data_folder = 'data'
fmt = '%Y-%m-%d'
sleep_time = 60

# Mongo DB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["NH3"]
col = db["raw_data"]

# Create target Directory
dir_path = os.path.dirname(os.path.realpath(__name__))
data_dir = dir_path + os.sep + data_folder
try:
    os.mkdir(data_dir)
    print("Directory " , data_dir ,  " Created ") 
except FileExistsError:
    print("Directory " , data_dir ,  " already exists")

# get date
files =  glob.glob(data_folder + '/*.csv')
if files:
	files.sort()
	last_date = files[-1].split('/')[-1].split('.')[0]
	start = datetime.strptime(last_date, fmt)
else:
	start = datetime.utcnow().date() - timedelta(365)

sleep(sleep_time)
end = datetime.utcnow().date()

while True:
	if start != end:
		days = [start + timedelta(i) for i in range((end-start).days)]

		for day in days:
			query = {'date_time': {'$gte': day, '$lte': day + timedelta(1)}}

			# load data
			cursor = col.find(query)
			df =  pd.DataFrame(list(cursor))
			print(day, flush=True)

			if not df.empty:
				# Delete the _id
				if '_id' in df: del df['_id']
				# save data
				print('data saved.')
				file_name = data_dir + os.sep + day.strftime(fmt)
				df.to_csv(file_name + '.csv', index=False)
			else:
				print('no data this day.')

	sleep(sleep_time)
	start, end = end, datetime.utcnow().date()
	print(datetime.utcnow())
