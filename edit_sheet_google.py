import gspread
import json
import pprint
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope) # get email and key from creds


file = gspread.authorize(credentials) # authenticate with Google

sheet = file.open("Monitor Error").sheet1
content = sheet.get_all_records()
pp = pprint.PrettyPrinter()
pp.pprint(content.__len__())
pp.pprint(content[848])


# List some error can have when setup
# https://github.com/burnash/gspread/issues/513
