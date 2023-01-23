import schedule
import ftplib
import os
import shutil
import time

def OpenFTP():
    ftpHost = "localhost"
    ftpPort = 21
    ftpUsername = "username"
    ftpPassword = "password"

    ftp = ftplib.FTP()

    ftp.connect(ftpHost, ftpPort)

    ftp.login(ftpUsername, ftpPassword)

    remoteWorkingDirectory = "ftp"

    # listing the files in the working directory
    fnames = []
    try:
        fnames = ftp.nlst(remoteWorkingDirectory)
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            fnames = []
        else:
            raise

    ftp.cwd("ftp")

    # iterating over the files in the working directory
    for i in fnames:
        i = i.replace("ftp/","" )
        with open(i, "wb") as file:
            ftp.retrbinary(f"RETR {i}",file.write)

    # moving the files from the local directory to the internal directory
    srcFolder = os.getcwd()
    destFolder =(r"C:\Users\InternalNetwork")
    files = os.listdir(srcFolder)
    os.chdir(srcFolder)
    for file in files:
        if os.path.isfile(file):
            full_dest = os.path.join(destFolder, file)
            shutil.move(file,destFolder)

    ftp.quit()

schedule.every(1).day.at("9:00").do(OpenFTP())

while True:
    schedule.run_pending()
    time.sleep(1)