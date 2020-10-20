import datetime
from database.Syllabus import ProcessSyllabus
from database import addToDB
import logging

'''
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
'''
##uncomment this to stop log prints

logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

'''
Year and session:
Winter2019 = W, 2019
Summer2019 = S, 2019
default: S, 2009

Subject: string

hasFig = does the question needs a figure?
default False

Type of Question:
LAQ-Long Answer Type Qs, DEFAULT
MCQ-Multiple Choice Type Qs

Marks
default 0

LAQ = string
MCQ = List of 5 items:
index 0: Question
indices 1-4: Options 1-4

Subject and their abbreviations for calculating fig name:
Fundamentals of Design and Manufacturing: FDM
Computing and Informatics: CI
Material Science: MS
Society and Environment: SE
Engineering Management: EM
More to be added
'''

class Question:
    currYear = datetime.datetime.now().year
    
    def __init__(self, **kwargs):
        self.type = kwargs.get('type', 'LAQ')
        self.marks = kwargs.get('marks', 0)
        self.laq=kwargs.get('laq', '')
        self.mcq=[]
        self.session=kwargs.get('session','S')
        self.year=kwargs.get('year', 2009)
        self.subject=kwargs.get('subject',None)
        self.hasFig=False
        self.figName=''
        ## example: qNo = '1(b)(iii)'
        self.qNo=kwargs.get('qNo','')
        ## TO DO
        self.id=''
        self.syllabus=''
        
    
    def setType(self, qType):
        '''
        qType receives string value 'LAQ' or 'MCQ', or int values such that
        every odd value means 'LAQ', and even value means 'MCQ'.
        '''
        if type(qType) == str and (qType=='LAQ' or qType == 'MCQ'):
            self.type = qType
        elif type(qType) == int:
            if qType % 2 == 0:
                self.type = 'MCQ'
            elif qType % 2 == 1:
                self.type = 'LAQ'

    def setMarks(self, marks):
        if marks > 20:
            try:
                raise ValueError('Marks of this question crosses 20', marks)
            except  ValueError as err:
                print(err.args)
        else:
            self.marks = marks

    def setSummer(self):
        self.session='S'

    def setWinter(self):
        self.session='W'

    def setYear(self, year):
        if 2009 <= year <= currYear:
            self.year = year

    def setQ(self, qStatement):
        '''
        qStatement is a string
        '''
        if self.type == 'LAQ':
            self.laq=qStatement
        else:
            self.mcq = qStatement.splitlines()
        if not(type(self.mcq) == list):
            try:
                raise TypeError('Not MCQ, check question statement')
            except TypeError as err:
                print(err.args)
        elif not(len(self.mcq) == 5):
            try:
                raise ValueError('Number of options is not five, but: ',
                                 len(self.mcq))
            except ValueError as err:
                print(err.args)

        
    def setFigName(self):
        namelist = {'Fundamentals of Design and Manufacturing': 'FDM',
                    'Computing and Informatics': 'CI',
                    'Material Science': 'MS',
                    'Material Science and Engineering': 'MS',
                    'Society and Environment': 'SE',
                    'Engineering Management': 'EM'}
        
        if self.subject == None:
            ##
            pass
        else:
            self.figName = namelist[self.subject]+"-"+self.session+self.year+'Q'+self.qNo

    def setSyllabus(self):
        self.syllabus = ProcessSyllabus.processSyllabus(self.laq, self.subject)
        logger.debug(str(self.syllabus))
        #print "Inside Question.py, setSyllabus, Question is: "+self.laq

    def insertInDB(self, qPaperiD = 0):
        database = "database/app.db"
        # create a database connection
        conn = addToDB.create_connection(database)
        with conn:
            if self.hasFig:
                fig = (self.figName, )
                figId = addToDB.insertInFigure(conn, fig)
            else:
                figId = 0
            t = (self.qNo, self.laq, self.hasFig, figId,
                 self.syllabus, qPaperiD, self.marks)
            logger.debug(str(t))
            addToDB.insertInQuestion(conn, t)
            
        
