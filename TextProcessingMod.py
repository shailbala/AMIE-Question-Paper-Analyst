import re
import QuestionPaper
from database import addToDB

def readFromFile(fileN, loc=''):
    '''
    reads file fileN from location loc
    '''
    rawdata=''
    try:
        with open(loc+fileN, 'r') as f:
            rawdata = f.read()
    except IOError:
        print "Could not read file:", loc+fileN
    ## Search for the text Winter/Summer yyyy
    header = re.findall(r'(Winter.+\d{4}|Summer.+\d{4})', rawdata, re.I)
    print header
    indices = []
    i = 0
    for each in header:
        i = rawdata.find(each, i)
        if i>-1:
            indices.append(i)
    ## We have the indices of starting point of each Question Paper
    ## in one text
    ## Use it to call QuestionPaper.QuestionPaper()
    for i in range(len(indices)-1):
        r = rawdata[indices[i]:indices[i+1]]
        print "New Question Paper"
        print header[i]
        q = QuestionPaper.QuestionPaper(rawdata=r)
        q.analyseHead()

## these all passed successfully
loc = 'QuestionPaper/'
#readFromFile('Computing and Informatics', loc)
#readFromFile('Fundamentals of Design and Manufacturing')
readFromFile('Material Science and Engineering', loc)
#readFromFile('Society and Environment')
        
#to test
#readFromFile('')
