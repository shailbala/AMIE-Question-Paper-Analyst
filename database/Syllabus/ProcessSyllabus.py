import re
import json
import logging

'''
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
'''
##uncomment this to stop log prints

logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.CRITICAL)

logger = logging.getLogger(__name__)

def readJsonFromFile(fileN, loc=''):
    '''
    reads file fileN from location loc
    '''
    rawdata=''
    try:
        with open(loc+fileN, 'r') as f:
            rawdata = f.read()
    except IOError:
        print "Could not read file:", loc+fileN
    #print rawdata
    dat = json.loads(rawdata)
    return dat

def readFromFile(fileN, loc=''):
    '''
    reads file fileN from location loc
    '''
    rawdata=''
    try:
        with open(loc+fileN, 'r') as f:
            rawdata = f.read()
    
    except IOError as e:
        print e.args
        print "Could not read file:", loc+fileN
    #print rawdata
    return rawdata

'''
def processSyllabus(qData):
    #print "qData: ", qData
    #location = './Documents/ProjectAMIEpy/Syllabus/'
    location = 'Syllabus/'
    fileName = 'Reverse-Computing and Informatics'
    data = readJsonFromFile(fileName, location)
    #print data["C\+\+"]
    #print "Inside processSyllabus, data received"
    #print "Starting the actual test"
    for k, v in data.items():
        #print k, v
        #print k
        if re.search(str(k), qData, re.I):
            #print
            return v
    else:
        print qData
'''

def processSyllabus(qData, sub):
    #print "Inside ProcessSyllabus, qData: "+qData
    #print "Subject as received: "+sub
    if sub.lower() == 'computing and informatics':
        return processEachSyllabus('CItopics', qData)
    elif (sub.lower() == 'material science and engineering') or (sub.lower() == 'material science'):
        return processEachSyllabus('MStopics', qData)

def processEachSyllabus(fileName, qData):
    
    loc = '/database/Syllabus/'
    data = readFromFile(fileName, loc)
    #print data
    data = data.split("\n")
    if data[-1] == ['']:
        data.remove([''])
    d = {}
    for line in data:
        try:
            line = line.split(":")
            #print line
            line[1] = int(line[1].strip())
            d[line[0]] = line[1]
        except IndexError as e:
            #print e.args
            pass
    
    for k, v in d.items():
        #print k, v
        #print k
        if re.search(str(k), qData, re.I):
            #return id of syllabus
            logger.info("Id of Syllabus: "+str(v))
            #print "Matched phrase: ", k
            return v
    else:
        print "Question: "+qData
        #print "Enter the syllabus id for this Q: "
        #x = int(raw_input())
        #return x
        print "syllabus not found for above Q"
        return 0
        

# Dummy data
#q = "schmid"
#print processSyllabus('MStopics', q)
