import datetime
from functools import partial
import json
from re import sub
from canvasapi import Canvas
from canvasapi.exceptions import CanvasException
import csv
import os
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import requests

with open(os.path.dirname(os.getcwd()) + '/access_keys.txt') as json_file:
    keys = json.load(json_file)

headers={
    'Authorization': "Bearer " + keys['prod']
}

req = requests.Session()
req.headers.update(headers)


#process homeroom file
homeroomlist =[]
with open('homerooms.csv') as homerooms:
    read = csv.DictReader(homerooms)
    for x in read:
        homeroomlist.append(x)

#process sis_accounts
dict_account = dict()
with open('sis_accounts.csv') as sis_accounts:
    read = csv.DictReader(sis_accounts)
    for x in read:
        dict_account[x['account_id']] = x['name']

headers_f = ['name', 'student id', 'progress']       
#now for each homeroom we need to get bulk progress
for h in tqdm(homeroomlist):
    h_acc = h['account_id']
    bulk_prog = req.get("https://cms.instructure.com/api/v1/courses/sis_course_id:" + h['course_id']+"/users")    
    if len(bulk_prog.json()) == 0:
        continue
    bulk_prog = req.get("https://cms.instructure.com/api/v1/courses/sis_course_id:" + h['course_id']+"/bulk_user_progress?per_page=100")
    if bulk_prog.status_code !=200:
        tqdm.write(h['course_id'] + " does not have the content?")
        continue
    #means list is not empty, so let's go and process
    with open(dict_account[h_acc] + ".csv", 'a', newline="") as write_file:
        csvWriter = csv.DictWriter(write_file, fieldnames=headers_f)
        if os.path.getsize(dict_account[h_acc] + ".csv") == 0:
            csvWriter.writeheader()
        #process current json blob
        for x in tqdm(bulk_prog.json(), leave=False):
            temp_dict = dict()
            #calc progress
            temp_dict["progress"] = x['progress']['requirement_completed_count']/x['progress']['requirement_count'] * 100
            temp_dict['name']= x['display_name']

            #find student ID
            #tqdm.write(str(x['id']))
            st_id = requests.get('https://cms.instructure.com/api/v1/users/'+str(x['id']), headers=headers)
            #tqdm.write(st_id.text)
            temp_dict['student id'] = st_id.json()['login_id']
            csvWriter.writerow(temp_dict)

        #get next request:
        #print(bulk_prog.links)
        while bulk_prog.links['current']['url'] != bulk_prog.links['last']['url']:
            bulk_prog = req.get(bulk_prog.links['next']['url'])

            for x in tqdm(bulk_prog.json(), leave=False):
                temp_dict = dict()
            #calc progress
                temp_dict["progress"] = x['progress']['requirement_completed_count']/x['progress']['requirement_count'] * 100
                temp_dict['name']= x['display_name']

                #find student ID
                st_id = requests.get('https://cms.instructure.com/api/v1/users/'+str(x['id']), headers=headers)
                temp_dict['student id'] = st_id.json()['login_id']
                csvWriter.writerow(temp_dict)


    




#pulled homerooms

# #Edit the request so that your URL is used 

# req = requests.post('https://cms.instructure.com/api/v1/accounts/1446/reports/sis_export_csv', params={'parameters[courses]': True}, headers=headers)
# json_re = req.json()
# time.sleep(10)

# id = json_re['id']
# print("report " + str(id))

# #check url for if the report is done.
# done = False
# file_url=""
# while(not done):
#     req = requests.get('https://cms.instructure.com/api/v1/accounts/1446/reports/sis_export_csv/'+str(id), headers=headers)
#     print("not done yet, sleeping for 30 secs")
#     if(req.json()['status'] == 'complete'):
#         file_url = req.json()['attachment']['url']
#         break
#     time.sleep(30)

# #download the report!
# req = requests.get(file_url)
# open("sis_export.csv", 'wb').write(req.content)

# #homeroom codes
# hs_homeroom_code = '99329X0900'
# ms_homeroom_code = '99329Y0900'

# #filter code
# homerooms = []
# with open('sis_export.csv') as sis_file:
#     read = csv.DictReader(sis_file)
#     homerooms = [x for x in read if hs_homeroom_code in x['short_name'] or ms_homeroom_code in x['short_name']]

# print(homerooms)

# #read data from each homeroom
# filename='homerooms_'+str(datetime.date.today())+'.csv'
# with open(filename, 'w',  newline="") as import_file:
#     write_f = csv.DictWriter(import_file, fieldnames=homerooms[0].keys())
#     write_f.writeheader()
#     write_f.writerows(homerooms)