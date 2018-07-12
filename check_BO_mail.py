from __future__ import print_function
import httplib2
import os


import requests
import sys
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret_nta.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'credentialv_modify.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#def total_mess_pl():
#    credentials = get_credentials()
#    http = credentials.authorize(httplib2.Http())
#    service = discovery.build ('gmail', 'v1', http=http)
#    respond_id_message=service.users().messages().list(userId="me",labelIds="Label_7").execute()
#    total_mess = 0 + respond_id_message["resultSizeEstimate"]
#    while 'nextPageToken' in respond_id_message:
#        page_token = respond_id_message['nextPageToken']
#        respond_id_message = service.users().messages().list(userId="me",
#                                                 labelIds="Label_7",
#                                                 pageToken=page_token).execute()
#        total_mess += respond_id_message["resultSizeEstimate"]
#    return total_mess

def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build ('gmail', 'v1', http=http)
    return service

def get_id_message_news(name_label):
    label_id = get_id_label(name_label)
    service = get_service()
    repond_id_message=service.users().messages().list(userId="me",labelIds=label_id).execute()
    if repond_id_message["resultSizeEstimate"] == 0:
        return 0
    else:
        list_id = []
        list_id.extend(repond_id_message['messages'])
        return list_id

def get_id_label(name_label):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build ('gmail', 'v1', http=http)
    repond_id_label=service.users().labels().list(userId="me").execute()
    list_id_label = repond_id_label["labels"]
    for id_label in list_id_label:
            if id_label["name"] == name_label:
                    return id_label["id"]

def move_mail(id_thread,name_label,name_label_readed):
    id_name_label = get_id_label(name_label)
    id_name_label_readed = get_id_label(name_label_readed)
    request_body = {
       'removeLabelIds': [ id_name_label ],
       'addLabelIds': [ id_name_label_readed ]
        }
    service = get_service()
    thread = service.users().threads().modify(userId="me",id=id_thread,body=request_body).execute()

## Function show Subject of Message
def get_subject(id_message):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build ('gmail', 'v1', http=http)
    respond_subj = service.users().messages().get(userId="me",id=id_message).execute()
    for id_subject in respond_subj["payload"]["headers"]:
        if id_subject["name"] == "Subject":
                    return  (id_subject["value"])



def hipchat_notify(token,room,message, color='yellow', notify=False,
                   format='text', host='api.hipchat.com'):
    url = "https://{0}/v2/room/{1}/notification".format(host, room)
    headers = {'Content-type': 'application/json'}
    headers['Authorization'] = "Bearer " + token
    payload = {
        'message': message,
        'notify': notify,
        'message_format': format,
        'color': color
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)

def add_key_file(str_kq):
    path = "/home/tuandk/gmailapi/mail_check/check_BO.txt"
    file = open(path,"a")
    file.write(str_kq)
    file.close()

def get_message(token,id_room,name_label,name_label_readed):
    list_id_message = get_id_message_news(name_label)
    if list_id_message == 0:
        message = "@VNOPStuandaokhac,@OMKhanhPhamDuy,@VNOManhnguyenquang,@VNOPSOMThoTranVan,@OMTuyenTranManh,@OMCuongNguyenChinh,@OMChienTranVan,@OMDatLuuTien  ERROR don't have mail BO, Please check"
        add_key_file("Yes")
        hipchat_notify(token,id_room,message,"red")
    else:
        for id in list_id_message:
            move_mail(id["threadId"],name_label,name_label_readed)
            message = get_subject(id["id"])
            hipchat_notify(token,id_room,message)
        add_key_file("No")
if __name__ == '__main__':
    name_label = "1.2.TRS_PL_MAIL_DAILY/TRS_PL_MAIL_BO"
    name_label_readed = "1.2.TRS_PL_MAIL_DAILY/TRS_PL_MAIL_DAILY_BO_READED"
    token = "OORzIqAGeNZHnT1nLu6PyNZ0GiedgfFfpUun0Tmy"
    room_id = "3746779"
    get_message(token,room_id,name_label,name_label_readed)
    
    
    ===============================================================
Content file client_secret_nta.json

    {"installed":
{"client_id":"531666323436-39t2movog2dqg30aqfafemnff36g5jo8.apps.googleusercontent.com",
"project_id":"modular-decoder-160719","auth_uri":"https://accounts.google.com/o/oauth2/auth",
"token_uri":"https://accounts.google.com/o/oauth2/token",
"auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
"client_secret":"HUn5F8ILV_QYVHm4k7mCsNjA",
"redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}
}
