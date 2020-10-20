from PIL import Image as PI
from pytesseract import *
import io

# for comparison
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


## import os
## os.getcwd()
## os.chdir('/Documents/ProjectAMIEpy/')
## path = "./Documents/ProjectAMIEpy/"

## image_pdf = Image(filename="AMIE\ section\ B\ old\ question\ paper.pdf",resolution=300)

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = image_to_string(PI.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


def compare(textRead, actualText):
    ravg = 0.0
    rlist = textRead.splitlines()
    alist = actualText.splitlines()
    if len(rlist) > len(alist):
        size = len(alist)
    else:
        size = len(rlist)
    for i in range(size):
        rline = rlist[i]
        aline = alist[i]
        ## print rline
        ## print "\n"
        ## print aline
        sim = similar(rline, aline)
        ## print sim
        ravg = ravg + sim
        ## print "\n"
    return ravg/size


image_list=['1', '2', '3', '4', '5', '6', '7']
ext = '.png'



for each in image_list:
    image_file = each+ext
    readText = ocr_core(image_file)
    #### Compare the results with the actual
    actualText = open('TextFor'+each).read()
    print "\n**********\nComparison of"+each
    print compare(readText, actualText)
    # print readText

