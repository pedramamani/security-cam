from constants import *
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def uploadAll():
    service = build('drive', 'v3', credentials=Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES))

    for fileName in os.listdir(ASSETS_DIR):
        if fileName.endswith('.avi'):
            metadata = {'name': fileName, 'parents': [DRIVE_FOLDER_ID]}
            media = MediaFileUpload(ASSETS_DIR / fileName)
            service.files().create(body=metadata, media_body=media, fields='id').execute()
            del media  # to release the file handle so we can delete it
            os.remove(ASSETS_DIR / fileName)
            print(f'uploaded file "{fileName}" and removed local copy')


if __name__ == '__main__':
    uploadAll()
