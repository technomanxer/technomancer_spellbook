#google drive API testing here.
#instructions to init are here: https://developers.google.com/drive/api/quickstart/python

import io
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload


import json

SCOPES = ['https://www.googleapis.com/auth/drive']
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

# Print first 100 files in my account
# files = DRIVE.files().list().execute().get('files', [])
# for f in files:
#     print(f['name'], f['mimeType'])

#code for this from https://developers.google.com/drive/api/guides/search-files
#grab and download file?
# page_token = None
# while True:
#     response = DRIVE.files().list(q="name='obj_stu_Mar_21_2022'",
#                                           spaces='drive',
#                                           fields='nextPageToken, files(id, name)',
#                                           pageToken=page_token).execute()
    
#     #response is a JSON object
#     #print(json.dumps(response, indent=4))
#     #get list of files, if files doesn't exist, then return empty string
#     for file in response.get('files', []):
#         # Process change
#         print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
#     page_token = response.get('nextPageToken', None)
#     if page_token is None:
#         break

# #obj file id
# file_id='XXXXXXXXXXXXXXXXXXXXXXX'
# #try : grab file
# request = DRIVE.files().get_media(fileId=file_id)
# fh = io.FileIO('obj_stu.json', 'wb')
# downloader = MediaIoBaseDownload(fh, request)
# done = False
# while done is False:
#     status, done = downloader.next_chunk()
#     print ("Download %d%%." % int(status.progress() * 100))

#close socket
DRIVE.close()

#parse json
# with open('obj.json', 'r') as json_file:
#     data = json.load(json_file)

with open('obj_stu.json', 'r') as json_file:
    data = json.load(json_file)
print(data['1195140'])
# print(type(data))
# print(len(data))
# print(data.keys())

#investigation results...
#key is email of the user.
#need to get the key to get the name of the user. thankfully python .keys() can get keys, then we can look at object.
# for d in data.keys():
#     print(data[d])