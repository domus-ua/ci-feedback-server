import os
import json
import logging
import requests 
from datetime import datetime

logging.basicConfig(level=logging.INFO, filename=f'{os.path.dirname(os.path.abspath(__file__))}/notification.log', filemode='a', format='%(asctime)s %(levelname)s:%(message)s')

# Expo server parameters
EXPO_URL = 'https://exp.host/--/api/v2/push/send'
EXPO_HEADERS = {
    'Host': 'exp.host',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/json'
}

# Flask server
FLASK_SERVER = 'https://ci-flask-server.herokuapp.com/'
FLASK_TOKENS = FLASK_SERVER + 'tokens'
FLASK_STATUS = FLASK_SERVER + 'build-info'



def send_notification(token, title, body):
    payload = {
        'to': token,
        'title': title,
        'body': body
    }
    
    try:
        response = requests.post(url=EXPO_URL, data=json.dumps(payload), headers=EXPO_HEADERS)
        logging.info(f"User notified with success! Response: {response}")
    except e:
        logging.warning(e)

if __name__ == '__main__':
    
    # start cronjob
    logging.info("------------------------------")
    logging.info("Start cronjob")
    logging.info("------------------------------")

    # today date
    today = datetime.today().strftime("%Y-%m-%d")
    logging.debug(f"Today date: {today}")

    # get EXPO tokens
    tokens = requests.get(FLASK_TOKENS).json()
    
    # get current build from FLASK SERVER
    build_info = requests.get(FLASK_STATUS).json()

    
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/last_build.json', 'r+') as f:
        # open the last build status
        last_build = json.loads(f.read())
        
        # current pipelines
        for pipeline in build_info:
            
            last_status = last_build[pipeline]
            current_status = build_info[pipeline]

            # users to be notified
            notified = 0

            logging.info(f"{pipeline} pipeline: {current_status.upper()}")

            # if this pipeline has failed for the first time, a notification is sent to every logged in user
            if current_status == 'failed' and last_status != 'failed':
                for token in tokens:
                    notified += 1
                    pipeline_name = pipeline if pipeline != 'rest_api' else 'rest api'
                    send_notification(token, "Domus build status", f"Your {pipeline_name} pipeline has failed!")

        # override the previous build status with the current build status
        f.seek(0)
        f.write(json.dumps(build_info))
        f.truncate()



logging.info(f"Notified {notified} user devices")
logging.info("------------------------------")
logging.info("Finish cronjob")
logging.info("------------------------------")
