import os
import csv
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

# Check if folder 'csv_files' exists, create it if not
if not os.path.exists('csv_files'):
    os.makedirs('csv_files')

path = 'csv_files/wikiImagesWithText.csv'
outputFile = open(path, 'w')
writer = csv.writer(outputFile)
header = ['entity_name', 'entity_URI', 'imageURL', 'imageCaption', 'imageURL', 'imageCaption', 'imageURL', 'imageCaption']
writer.writerow(header)

with open('csv_files/wikiEntities.csv') as f:
    reader = csv.reader(f)
    next(reader)

    for name, link in tqdm(reader):
        res = requests.get(url=link)
        soup = bs(res.content, 'html.parser')

        imageURL1, imageURL2, imageURL3, text1, text2, text3  = '', '', '', '', '', ''
        count = 0

        # image in the infobox includes vcard, vevent type
        image1 = soup.select_one('table.infobox td.infobox-image img[src]')
        if image1:
            count += 1
            imageURL1 = image1['src']
            if 'https:' not in imageURL1:
                imageURL1 = 'https:' + image1['src']
            text1 = soup.select_one('table.infobox div.infobox-caption, table.infobox caption.infobox-title')
            text1 = text1.text.strip().replace('\n', ' ') if text1 else ''

        # webpages which don't have a infotable picture
        images = soup.select('div.thumb.tright')
        imgs = []
        if images:
            for img in images:
                # Extract the image URL
                count += 1
                img_url = ''
                temp_img = img.find('img')
                if temp_img:
                    img_url = temp_img['src']
                    if img_url and 'https:' not in img_url:
                        img_url = 'https:' + img_url
                else:   
                    continue
                
                # Extract the text description, if available
                text = img.find('div', class_='thumbcaption')
                if text is not None:
                    text = text.text.strip().replace('\n', ' ')

                img = {"url": img_url, "caption": text}
                imgs.append(img)

                if count > 3:
                    break

        if imgs:
            imageURL2 = imgs[0]['url']
            text2 = imgs[0]['caption']
            if len(imgs) > 1:
                imageURL3 = imgs[1]['url']
                text3 = imgs[1]['caption']
                if imageURL1 == '' and len(imgs) > 2:
                    imageURL1 = imgs[2]['url']
                    text1 = imgs[2]['caption']

        row = [name, link, imageURL1, text1, imageURL2, text2, imageURL3, text3]
        writer.writerow(row)

outputFile.close()
