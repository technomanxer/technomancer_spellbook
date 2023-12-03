import csv
import os
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import requests

#this is where i put my keys for Canvas
with open(os.path.dirname(os.getcwd()) + '/access_keys.txt') as json_file:
    keys = json.load(json_file)

headers={
    'Authorization': "Bearer " + keys['prod']
}

#Edit the request so that your URL is used 
#repeat params to download multiple CSVs if needed

req = requests.post('<insert your API url>/reports/sis_export_csv', params={'parameters[<place CSV file you want to download here>]': True}, headers=headers)
json_re = req.json()
time.sleep(10)

id = json_re['id']
print("report " + str(id))

#check url for if the report is done.
done = False
file_url=""
while(not done):
    req = requests.get('<insert your API url>/reports/sis_export_csv/'+str(id), headers=headers)
    print("not done yet, sleeping for 30 secs")
    if(req.json()['status'] == 'complete'):
        file_url = req.json()['attachment']['url']
        break
    time.sleep(30)

#download the report!
req = requests.get(file_url)
open("sis_export.csv", 'wb').write(req.content)
