import requests
from bs4 import BeautifulSoup
import csv
import os
import json

with open('./csv_files/copy_wikiEntities.csv', 'r') as file:
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

        # Write the output to a separate json file for each entity
        output_filename = 'img_data.txt'
        output_file_exists = os.path.isfile(output_filename)

        with open(output_filename, 'a') as file:
            if not output_file_exists:
                file.write('{')
            else:
                file.write(', ')

            file.write('"' + entity_name + '": ')
            json_text = json.dumps(text.strip(), ensure_ascii=False)
            file.write("\"" + json_text.replace('"', ' ') + "\"")

        print(entity_name + ' done')
