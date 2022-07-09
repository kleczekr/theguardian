import pandas as pd
import requests
import time
from datetime import datetime, timedelta

today = datetime.now()
yesterday = (today - timedelta(1)).strftime('%Y-%m-%d')
print(yesterday)

df = pd.read_csv('extended.csv')
key = 'GUARDIAN_API_KEY'
name_list = ['Justin Trudeau', 'Theresa May', 'Boris Johnson', 'Emmanuel Macron',
             'Angela Merkel', 'Jacinda Ardern', 'Bernie Sanders']


def get_df(list_of_names):
    '''
    the function receives a list of names
    (if it is a single name, it still should be
    in a list) and returns a dataframe containing
    all the articles published on The Guardian
    about the mentioned names in the timespan
    2014-present.
    '''
    list_of_articles = []
    for name_ in list_of_names:
        print(name_)
        name_query = '%20AND%20'.join(name_.lower().split())
        json_ = requests.get(
            f'https://content.guardianapis.com/search?q={name_query}&from-date={yesterday}&page-size=50&api-key={key}').json()
        response = json_['response']
        try:
            results = response['results']
            for article in results:
                article['name'] = name_
                list_of_articles.append(article)
        except:
            print('*'*60)
            print(f'There was an issue processing the page')
            print(response)
            print('*'*60)
            time.sleep(10)
            time.sleep(1)
    df_part = pd.DataFrame.from_dict(list_of_articles)
    return df_part


df_part = get_df(name_list)

print(df_part)

df = pd.concat([df, df_part])

df.to_csv('extended.csv', index=False)
# ncftpput -u CLIENT -p PASSWORD ftp.deite.org public_html/theguardian /home/pi/projects/theguardian/extended.csv
