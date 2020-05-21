import os
from crontab import CronTab 

username = os.getenv('USER')

# get crontab
cron = CronTab(user=username)

# remove old notifications cronjobs 
cron.remove_all(comment='notification')

# create new cronjobs 
job = cron.new(command=f'python3 {os.path.dirname(os.path.abspath(__file__))}/notification.py', comment='notification')

# running cronjob every minute
job.minute.every(1)

# save changes to crontab
cron.write()
