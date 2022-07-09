import pandas as pd
import requests
import time

key = 'GUARDIAN_API_KEY'

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
    number_of_pages = requests.get(f'https://content.guardianapis.com/search?q={name_query}&from-date=2018-01-01&page=1&page-size=50&api-key={key}').json()['response']['pages']
    for i in range(1, number_of_pages+1):
      json_ = requests.get(f'https://content.guardianapis.com/search?q={name_query}&from-date=2018-01-01&page={i}&page-size=50&api-key={key}').json()
      response = json_['response']
      try:
        results = response['results']
        for article in results:
          article['name'] = name_
          list_of_articles.append(article)
        print(f'Finished processing the page {i} out of {number_of_pages} (i.e. {round(i/number_of_pages*100, 2)}%) pertaining to {name_}')
        time.sleep(1)
      except:
        print('*'*60)
        print(f'There was an issue processing the page {i} of the results pertaining to {name_}')
        print(response)
        print('*'*60)
        time.sleep(10)
    time.sleep(2)
  df = pd.DataFrame.from_dict(list_of_articles)
  return df

name_list = ['Justin Trudeau', 'Theresa May', 'Boris Johnson', 'Emmanuel Macron', \
             'Angela Merkel', 'Jacinda Ardern', 'Bernie Sanders']

df = get_df(name_list)

df.to_csv('extended.csv', index=False)