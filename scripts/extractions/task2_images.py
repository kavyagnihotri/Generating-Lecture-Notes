#wrong?

import csv
import requests
import numpy as np
from bs4 import BeautifulSoup as bs

newFile = open('wiki3Images.csv', 'w')
writer = csv.writer(newFile)
# rows = []

with open('wikiImage.csv', 'r') as wikiFile:
    reader = csv.reader(wikiFile)
    header = next(reader)
    header.append('imageURL2')
    header.append('imageURL3')
    writer.writerow(header)

    writer = csv.writer(wikiFile)
    writer.writerow(header)
    
    cnt = 0
    for r in reader:
      cnt += 1
      print(cnt)

      link=r[1]
      res = requests.get(url=link)
      soup = bs(res.content, 'html.parser')
      
      image = soup.select('table.infobox td.infobox-image img[src]') # images in the infobox includes vcard, vevent type
      image2 = soup.select('div.thumb.tright img[src]')       # webpages which don't have a infotable picture
      images = image + image2
      
      imageURL2 = ''
      imageURL3 = ''
      if len(images) > 1: 
        imageURL2 = images[1]['src']
        if 'https:' not in imageURL2:
          imageURL2 = 'https:' + images[1]['src']
          print(imageURL2)

        if len(images) > 2:
          imageURL3 = images[2]['src']
          if 'https:' not in imageURL3:
            imageURL3 = 'https:' + images[2]['src']
            print(imageURL3)

      imageURL1 = ''
      if len(r) == 3:
        imageURL1 = r[2]
      row = [r[0], link, imageURL1, imageURL2, imageURL3]
      writer.writerow(row)      

newFile.close()
