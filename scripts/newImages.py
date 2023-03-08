import csv
import requests
import numpy as np
from bs4 import BeautifulSoup as bs

newFile = open('wiki3Images.csv', 'w')
writer = csv.writer(newFile)

with open('wikiImage.csv', 'r') as wikiFile:
    reader = csv.reader(wikiFile)

    header = next(reader)
    header.append('imageURL2')
    header.append('imageURL3')
    writer.writerow(header)

    cnt = 0
    for name,link,singleImage in reader:
      cnt += 1
      print(cnt)
      

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
          # print(imageURL2)

        if len(images) > 2:
          imageURL3 = images[2]['src']
          if 'https:' not in imageURL3:
            imageURL3 = 'https:' + images[2]['src']
            # print(imageURL3)
      
      row = [name, link, singleImage, imageURL2, imageURL3]
      writer.writerow(row)      

newFile.close()