import requests
from bs4 import BeautifulSoup
import csv
import os

with open('./csv_files/wikiEntities_copy.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        entity_name = row[0]
        url = row[1]
        
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        content_div = soup.find('div', {'class': 'mw-body-content'})

        if not content_div:
            content_div = soup.find('div', {'class': 'vector-body'})

        # Extract the text inside the content div
        text = ''
        for element in content_div.descendants:
            if element.name == 'img':
                text += "$IMG$"
            else:
                if hasattr(element, 'get_text'):
                    text += element.get_text()

        # Write the output to a text file
        output_filename = 'wikiHTML_Img.txt'
        output_file_exists = os.path.isfile(output_filename)

        with open(output_filename, 'a') as file:
            if not output_file_exists:
                file.write('{')
            else:
                # file.seek(-1, os.SEEK_END)
                # file.truncate()
                file.write(', ')

            file.write("'" + entity_name + "': ")
            file.write("'" + text.strip().replace("'", "\\'") + "'")
        print(entity_name + ' done')

    # with open(output_filename, 'a') as file:
    #     file.write('}')

