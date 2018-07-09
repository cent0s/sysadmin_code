
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


def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build ('gmail', 'v1', http=http)
    return service


def get_all_mess(name_label):
    id_label = get_id_label(name_label)
    service = get_service()
    repond_id_message=service.users().messages().list(userId="me",labelIds=id_label).execute()
    messages = []
    if 'messages' in repond_id_message:
        messages.extend(repond_id_message['messages'])
    while 'nextPageToken' in repond_id_message:
      page_token = repond_id_message['nextPageToken']
      repond_id_message = service.users().messages().list(userId="me",
                                                 labelIds=id_label,
                                                 pageToken=page_token).execute()
      messages.extend(repond_id_message['messages'])
    return messages

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
    path = "/home/tuandk/gmailapi/mail_check/check_mail_RKT.txt"
    file = open(path,"a")
    file.write(str_kq)
    file.close()

def check_mail_WMC(token,room,name_label,name_label_readed):
    list_id = get_all_mess(name_label)
    if len(list_id) > 0:
        add_key_file("Yes")
        for id in list_id:
            move_mail(id["threadId"],name_label,name_label_readed)
            subject_mail_error = get_subject(id["id"])
            message = "@VNOPStuandaokhac,@OMKhanhPhamDuy,@VNOManhnguyenquang,@VNOPSOMThoTranVan,@OMTuyenTranManh,@OMCuongNguyenChinh,@OMChienTranVan,@OMDatLuuTien.We have mail Rakuten.Please, check"
            hipchat_notify(token,room,message,"red")
    else:
        add_key_file("No")


if __name__ == '__main__':
    name_label = "11.RAKUTEN_MAIL"
    name_label_readed = "11.RAKUTEN_MAIL/11.RAKUTEN_MAIL_READED"
    token = "TsXL8TffD4No2VbAz4fgCc3xpYP0X4du8wfstHV5"
    room = "1494538"
#    token = "HoihlJx6zgLbhSAoBcpMr7zE5BCuayGSBlcsvF6U"
#    room = "3657870"
    check_mail_WMC(token,room,name_label,name_label_readed)
