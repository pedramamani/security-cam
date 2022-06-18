from constants import *
import cv2
import time
import datetime
import os
import numpy as np
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def setup():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())


def uploadAll():
    service = build('drive', 'v3', credentials=Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES))

    for fileName in os.listdir(ASSETS_DIR):
        if fileName.endswith('.avi'):
            metadata = {'name': fileName, 'parents': [DRIVE_FOLDER_ID]}
            media = MediaFileUpload(ASSETS_DIR / fileName)
            service.files().create(body=metadata, media_body=media, fields='id').execute()
            del media  # to release the file handle so we can delete it
            os.remove(ASSETS_DIR / fileName)
            print(f'uploaded file "{fileName}" and removed local copy\n')


if __name__ == '__main__':
    uploadAll()
