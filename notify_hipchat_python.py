#!/usr/bin/python

from __future__ import print_function
import requests
import sys
import json
import os


def hipchat_notify(token, room, message, color='yellow', notify=False,
                   format='text', host='api.hipchat.com'):
    """Send notification to a HipChat room via API version 2
    Parameters
    ----------
    token : str
        HipChat API version 2 compatible token (room or user token)
    room: str
        Name or API ID of the room to notify
    message: str
        Message to send to room
    color: str, optional
        Background color for message, defaults to yellow
        Valid values: yellow, green, red, purple, gray, random
    notify: bool, optional
        Whether message should trigger a user notification, defaults to False
    format: str, optional
        Format of message, defaults to text
        Valid values: text, html
    host: str, optional
        Host to connect to, defaults to api.hipchat.com
    """

    if len(message) > 10000:
        raise ValueError('Message too long')
    if format not in ['text', 'html']:
        raise ValueError("Invalid message format '{0}'".format(format))
    if color not in ['yellow', 'green', 'red', 'purple', 'gray', 'random']:
        raise ValueError("Invalid color {0}".format(color))
    if not isinstance(notify, bool):
        raise TypeError("Notify must be boolean")

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

#def send_content_hipchat(token, room):
#       message = str(os.getloadavg())
#       hipchat_notify(token,room,message,"red")

if __name__ == '__main__':
        token = 'p45CptgxUGc0qvlxSWCyZPR7C60WhxrPLNYXHDQx'
        room = '4090741'
        message = str(os.getloadavg())
try:
        hipchat_notify(token,room,message,"red")
except Exception as e:
        msg = "[ERROR] HipChat notify failed: '{0}'".format(e)
        print(msg, file=sys.stderr)
        sys.exit(1)
