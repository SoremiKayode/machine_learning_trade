from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os


auth_instance = GoogleAuth()

auth_instance.LocalWebserverAuth()
drive = GoogleDrive(auth_instance)

path = "eur_usd_processed.csv"
f = drive.CreateFile({"title": path})
f.Upload()

