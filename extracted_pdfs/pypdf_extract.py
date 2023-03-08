# using development version, getting error while trying to get images
# pip install pypdf[image]
# zsh: no matches found: pypdf[image]

from pypdf import PdfReader

reader = PdfReader("samples/insertionSortSimple.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
count = 0

for image_file_object in page.images:
    with open(str(count) + image_file_object.name, "wb") as fp:
        fp.write(image_file_object.data)
        count += 1

# print(text)
