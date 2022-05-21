from DataTwitter import DataTwitter
from content import content

print(content['alert_message_string'])
data = DataTwitter(input(content['input_string']))
data.save_csv_archive(data.find_recent_tweets(), content['archive_name'], content['fieldnames'])