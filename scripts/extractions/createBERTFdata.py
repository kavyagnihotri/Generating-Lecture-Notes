import requests
from bs4 import BeautifulSoup
import json
import csv

with open('TeKnowbaseEntities.tsv') as f:
    tsv_file = csv.reader(f, delimiter="\t")
    next(tsv_file)
    ind = 0
    for name,link in tsv_file:
        if 'wikipedia' not in link:
            continue

        response = requests.get(url=link)
        soup = BeautifulSoup(response.content, 'html.parser')


        # Create a list to store the content with "P" or "O" tags
        content_list = []
        tag_list = []


        elem = soup.find_all(True)
        elem.insert(0,elem.pop())

        for element, e in zip(soup.find_all(True),elem):
            if element.name == 'span' and 'mwe-math-element' in element.get('class',[]):
                ind = len(tag_list)-1
                indend = ind - 30
                while ind>=indend:
                    tag_list[ind] = 'F'
                    ind -= 1
            else:
                # Get the text content of the element
                text = element.get_text().strip()
                if text:
                    # Add the text to the content list with the current tag
                    words = text.split()
                    res = []
                    for sub in words:
                        s = sub.replace("\n", "")
                        if s != "":
                            res.append(s)
                    for txt in res:
                        content_list.append(txt)
                        tag_list.append("O")


        # content_list.append({"tokens": content_list, "tags": tag_list})


        # Convert the content list to a JSON-serializable format
        output_json = json.dumps({"tokens": content_list, "tags": tag_list})
        # Save the JSON to a file
        with open('./FormulaData/wikipedia_content'+str(ind)+'.json', 'w', encoding='utf-8') as json_file:
            json_file.write(output_json)
        ind += 1
        # print("JSON data has been created and saved to 'wikipedia_content.json'.")
