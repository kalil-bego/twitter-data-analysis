from source.DataTwitter import DataTwitter
from resources.content import content

print(content['author_string'])
print(content['alert_message_string'])
data = DataTwitter(query = input(content['input_string']), limit = int(input(content['input_limit'])))
data.save_csv_archive(data.find_recent_tweets(), content['archive_name'], content['fieldnames'])
data.show_word_cloud(content['archive_name'])