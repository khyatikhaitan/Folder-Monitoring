import os
import time
from datetime import datetime,timedelta
import smtplib
from email.message import EmailMessage

MONITORED_DIR='Absolute Path of the folder to be monitored'
SENDER="sender's email id"
RECIPIENT="recipient's email id"
APP_PWD='Generate the app password and paste it without spaces and not the id password'
TIME_INTERVALS=10


def find_recent_files(directory,minutes):
    current_time = datetime.fromtimestamp(time.time())
    recent_files=[]
    for file in os.listdir(directory):
        filepath=os.path.join(directory,file)
        print(filepath)
        if os.path.isfile(filepath):
            mod_time=os.path.getmtime(filepath)
            mod_time=datetime.fromtimestamp(os.path.getmtime(filepath))
            print(current_time)
            print(mod_time)
            print(current_time-mod_time)
            print(minutes*60)
            if current_time-mod_time<timedelta(minutes=minutes):
                recent_files.append(file)
    return recent_files

def send_email(file_list):
    msg=EmailMessage()
    msg['Subject']='📂 New Files Detected in Folder'
    msg['From']=SENDER
    msg['To']=RECIPIENT
    msg.set_content(f"The following new file(s) were added in the last {TIME_INTERVALS} minutes:\n\n" + "\n".join(file_list))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(SENDER,APP_PWD)
            smtp.send_message(msg)
            print("✅ Email alert sent.")
    except Exception as e:
        print("❌ Failed to send email:", e)
def main():
    recent_files=find_recent_files(MONITORED_DIR,TIME_INTERVALS)
    if recent_files:
        print("📂 New Files Found: ",recent_files)
        send_email(recent_files)
    else:
        print("No New Files")

if __name__ == '__main__':
    main()