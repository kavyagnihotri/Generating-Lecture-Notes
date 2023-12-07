import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

finalcsvlist=[]

i=0

with open('TeKnowbaseEntities.tsv') as f:
    tsv_file = csv.reader(f, delimiter="\t")
    next(tsv_file)
    for name,link in tsv_file:
      if 'wikipedia' not in link:
        continue

      res = requests.get(url=link)
      soup = bs(res.content, 'html.parser')

      csvlist=[]
      csvlist.append(name)
      csvlist.append(link)

      allformulas=soup.find_all("pre")
      tags=[]
      tags.extend((i.prettify() for i in allformulas))
      for each in tags:
        csvlist.append(each)
      
      finalcsvlist.append(csvlist)

      print(i)
      i += 1
      print(name)



df_final = pd.DataFrame(finalcsvlist)
df_final.to_csv("WikiPageWithPseudoCode.csv")
