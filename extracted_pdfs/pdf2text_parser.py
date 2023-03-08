#       pdftotext.cpp:3:10: fatal error: 'poppler/cpp/poppler-document.h' file not found
#       #include <poppler/cpp/poppler-document.h>
#                ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#       1 error generated.
#       error: command '/usr/bin/clang' failed with exit code 1
#       [end of output]
  
#   note: This error originates from a subprocess, and is likely not a problem with pip.
# error: legacy-install-failure

# × Encountered error while trying to install package.
# ╰─> pdftotext


path = r"samples/insertionSortSimple.pdf"
#Using PDFtotext
import pdftotext
# Load your PDF
with open(path, "rb") as f:
    pdf = pdftotext.PDF(f)
# Read all the text into one string
pdftotext_text = "\n\n".join(pdf)
print(pdftotext_text)