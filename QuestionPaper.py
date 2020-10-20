'''
Stores the complete question paper of one subject,
on one session using Question objects
'''
import datetime
import Question
import re
import Marks
import logging
from database import addToDB

'''
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

##uncomment this to stop log prints
'''
logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug("This is a debug log")
#logger.info("This is an info log")
#logger.error("An error occurred")
#logger.critical("This is critical")

currYear = datetime.datetime.now().year

class QuestionPaper:
    
    def __init__(self, **kwargs):
        self.newQn = 0
        self.year = kwargs.get('year', '2009')
        self.session=kwargs.get('session','S')
        self.subject=kwargs.get('subject',None)
        self.rawdata=kwargs.get('rawdata', '')
        ## contains list of Question objects
        self.groupA=[]
        self.groupB=[]
        self.groupC=[]
        self.id=0

    def setData(self, fullData):
        self.rawdata = fullData

    def setSubject(self, sub):
        self.subject = sub

    def setSessionYear(self, time):
        '''time parameter is of the format
        Winter 2018
        as read directly from raw text
        case-insensitive matching: re.I'''
        m = re.match(r'(Winter|Summer).+(\d\d\d\d)', time, re.I)
        if m:
            logger.info("Session found as per regex: "+str(m.group(1)))
            if (m.group(1)[0] == 'W') or (m.group(1)[0] == 'w'):
                self.session = 'W'
            else:
                self.session = 'S'
            self.year = m.group(2)
        logger.debug("Session as set: "+self.session+self.year)

    def insertInDB(self):
        database = "database/app.db"
        # create a database connection
        conn = addToDB.create_connection(database)
        with conn:
            subId = addToDB.getSubjectId(self.subject)
            if subId == 0:
                try:
                    raise ValueError("Subject not updated")
                except ValueError as e:
                    print e.args
                    return
            q = (self.session, self.year, subId)
            self.id = addToDB.insertInQuestionPaper(conn, q)
        print "Question Paper id: "+str(self.id)+", Session: "+self.session+self.year
        logger.debug("New row inserted in DB table QuestionPaper!")
        #logger.debug("self.id: "+str(self.id))

    def analyseHead(self):
        '''Analyses header of the Question paper
        to find session, year and subject name.
        And update them.
        It calls self.analyseQuestions(data) with the
        rest of sliced data, removing header.
        '''
        if self.rawdata=='':
            try:
                raise ValueError('RawData not added')
            except ValueError as err:
                logger.debug(str(err.args))
                return
        
        ## data = self.rawdata.splitlines()
        ## we will not split based on newline but based on regex
        
        ## Standard layout
        ## SUMMER 2019
        line1 = re.match(r'(Winter\s\d{4}|Summer\s\d{4})', self.rawdata, re.I)
        logger.debug(str(line1.group(0)))
        self.setSessionYear(line1.group(0))
        # find the first occurrence of \n after index 2
        index = self.rawdata.find("\n", 2)
        logger.debug(str(index))
        # find the second occurrence of \n, first occurrence after index
        index2 = self.rawdata.find("\n", index+1)
        logger.debug(str(index2))
    	## Subject Name + Code(Optional)
        sub = self.rawdata[index+1:index2]
        # remove subject code from sub, if applicable, and set subject
        i = sub.find("(")
        if i>0:
            sub = sub[:i]
        self.subject=sub
        logger.debug(str(sub))
        print sub
        self.insertInDB()

        
        ## Some data (optional)
	## Group[\s\-]+A
        index = self.rawdata.find("\nGroup A", index2)
        if index==-1:
            index = self.rawdata.find("\nGROUP A", index2)
        if index==-1:
            index = self.rawdata.find("\nGROUP-A", index2)
        if index==-1:
            index = self.rawdata.find("\nGroup-A", index2)
        if index==-1:
            index = self.rawdata.find("\nGROUP-A", index2)
        logger.debug(str(index))
        data = self.rawdata[index:]
        self.analyseQuestions(data)

    def analyseQuestions(self, data):
        '''
        Reads each *complete* question from data
        and calls analyseQuestion to break them into
        sub-questions

        Displays the contents of group C and takes input from user
        whether there are MCQs in Group C. If yes,
        it leaves out Group C altogether.
        '''
        ## Search for all match of group A/B/C. z is a list
        z = re.findall(r'\n([Gr][Rr][Oo][Uu][Pp]\s*[\-\s]\s*[ABC])', data)
        if len(z)==0:
            return
        #len(z) should always be 3
        logger.info("Inside analyseQuestions:"+str(len(z)))
        iA = data.find(z[0])
        logger.debug(str(iA))
        iB = data.find(z[1], iA)
        logger.debug(str(iB))
        iC = data.find(z[2], iB)
        logger.debug(str(iC))
        iN = len(data)-1

        ## Find the first question, to find pattern
        q = re.search(r'\n([\(]?1[\.\)])\s*', data)
        if not q:
            try:
                raise ValueError("searching for Question 1 found nothing!", q)
            except ValueError as err:
                logger.debug(str(err.agrs))
                return
        q = q.group(0).strip()
        p = findPattern(q)
        logger.debug("pattern p:"+str(p))
        ## Group A: Questions 1-4
        index = iN
        i = iB
        for q in range(4, 0, -1):
            ## Find the last question in Group A
            index = data.rfind("\n"+construct(p, q), iA, min(iB, index))
            logger.debug("index of last Q of Group A: "+str(index))
            ## Calls analyseQuestion() for further
            ## analysis and Question obj creation
            logger.debug(str(data[index:i].strip()))
            self.analyseQuestion(data[index:i].strip(), q, p, '', 'A')
            logger.debug(str(q))
            i = index
        ## Group B: Questions 5-8
        index = iN
        i = iC
        for q in range(8, 4, -1):
            ## Find the last question in Group A
            index = data.rfind("\n"+construct(p, q), iB, min(iC, index))
            ## Calls analyseQuestion() for further
            ## analysis and Question obj creation
            self.analyseQuestion(data[index:i].strip(), q, p, '', 'B')
            logger.debug(str(data[index:i].strip()))
            logger.debug(str(q))
            i = index
        ## Group C: Questions 9 onwards
        qList = []
        index = iC
        for q in range(9, 13):
            ## Search for each question in data
            ## if found, append its index to qList
            index = data.find("\n"+construct(p, q), index, iN)
            if not (index == -1):
                qList.append(index)
        qList.append(iN)
        ## We have the starting index of each question
        ## along with iN in the end
        
        for i in range(len(qList)-1):
            d = data[qList[i]:qList[i+1]].strip()
            print d
            t = raw_input("Does this contain MCQ or Matching Qs? (0 or 1)")
            if int(t) == 0:
                self.analyseQuestion(data[qList[i]:qList[i+1]].strip(), 9+i,
                                      p, '', 'C')
            logger.debug(str(data[qList[i]:qList[i+1]].strip()))
            logger.debug(str(9+i))
        
    def analyseQuestion(self, q, n, p, nParent='', group='A',
                         recur=False, marks=[0, 0]):
        ''' Recursive
        q=question string, n=Qno. of current Q, p=pattern
        nParent=Full Q no.(with pattern) of the parent Q, iff this Q is a sub-Q

        For example:
        3.(a)(1)
        When 3 is passed:
        n=3, p='.'

        When (a) is passed:
        n=a, p='()', nParent='3.', recur=True

        When (1) is passed:
        n=1, p='()', nParent='3.(a)', recur=True
        
        Receives one full question at a time
        Analyses it for sub-questions.
        For each subQuestion, calls itself recursively
        until one LAQ is found.
        
        It also works by analysing the way marks is given.
        Calls self.newLAQ to create new Question object
        and to take necessary further actions
        
        Base Case:
        No subQuestion, marks present at the end, or marks received
        Else:
        Call self.analyseQuestion()
        '''
        ## Save Question data q
        qData = q
        ## Find index of n, to remove it from q
        index = q.find(construct(p, n), 0, 10)
        logger.debug("nParent as rcvd.: "+nParent)
        if recur:
            nParent = nParent+construct(p, n)
        else:
            nParent = nParent+str(n)
        logger.debug("nParent+n: "+nParent)
        
        ## Remove n and question pattern p from question data q.
        ## Now we have only question data and marks
        if recur:
            pass
        else:
            q = q[index+len(construct(p, n)):]
        logger.debug("q:"+ str(q))

        ## Search for first sub-question, using regeX
        sub = re.search(r'\s(\(?[aAiI1][\)\.])', q)
        if sub:
            sub = sub.group(1)
            logger.debug("sub:"+ str(sub))
        else:
            ## No sub-questions, Base Case

            if marks == [0, 0]:
                q, marks = self.LAQmarks(q)
            #qN = nParent+construct(p, n)
            #print 'New LAQ called'
            self.newLAQ(q, marks, nParent)
            return

        ## Sub questions are present
        ## Flag, marks not found yet
        ## this if-else condition is unnecessary
        if not (marks[0] == 0):
            mFlag = True
        else:
            mFlag = False

        ## Set pattern
        p = findPattern(sub)
        logger.debug("sub:"+str(sub)+"p:"+str(p))
        ## Are there common instructions?
        i = q.find(sub)
        instrxn = ''
        if not (0 <= i <= 4):
            ## Common Instructions present
            instrxn = q[:i]
            q = q[i:].strip()
            logger.debug("q:"+ str(q))
            ## Check for marks at the end of instruction
            m = re.findall(r'\n(\(?[\w\s]*\d+[\*\+x]?\d*[\w\s\d]*\)?)\s', instrxn)
            if m:   #marks found, no recursive call then
                logger.info("Marks found in instruction")
                m = m[len(m)-1]
                logger.debug("m:"+m)
                ## remove the marks part from instrxn
                j = instrxn.find(m)
                instrxn = instrxn[:j]
                logger.debug("instrxn:"+instrxn)
                ## call function to analyse marks
                marks = Marks.marks(m)
                ## based on that, set a variable to store the number of Qs
                ## and marks and use it further
                logger.debug(str(marks))
                mFlag = True          

        # sub contains first sub-question found, e.g., '(a)'
        # find index of sub, this is the starting index
        i = q.find(sub)
        logger.debug("index of sub:"+ str(i))
        ## Search for the indices of all sub questions
        ## add them to the dict qList
        ## i contains the index of first sub-question
        nexti=i
        qList = {}
        nQ=sub
        #logger.debug(str(q))
        while(nexti > -1):
            qList[nQ]=nexti
            nQ = findNextQ(removePattern(str(nQ), p))
            logger.debug("next Q found: "+ str(nQ))
            nQ = construct(p, nQ)
            logger.debug("nQ:"+ str(nQ))
            nexti = q.find(nQ)
            logger.debug(nexti)
        logger.debug("qList"+ str(qList))

        ## generate 2 lists from qList
        qList1 = [x for x in qList.keys()]
        # sort
        qList1 = qSort(qList1)
        qList2 = []
        for each in qList1:
            qList2.append(qList[each])
        ## add last index in qList2 as well to extract last part
        qList2.append(len(q))
        ## qList1 contains all the subQuestions found(along with pattern)
        ## qList2 contains the starting indices of each subQuestion
        ## and the last index
        logger.debug("qList1:"+ str(qList1))
        logger.debug("qList2:"+ str(qList2))
        
        if mFlag and not(marks[0] == len(qList1)):
            ## For Group C, sometimes marks is given as 20M
            ## find out individual marks for each subQuestion
            marks[0] = len(qList1)
            marks[1] = int(marks[1]/marks[0])

        ## mFlag is True means, marks already found
        ## slice each question and use marks[2]
        if mFlag:
            ## slice each question and use marks[2]
            # TODO
            pass
        
        for i in range(len(qList1)):
            eachQ = q[qList2[i]:qList2[i+1]]
            index = eachQ.find(qList1[i], 0, 10)
            eachQ = eachQ[index+len(qList1[i]):]
            logger.debug("\n\nSliced Q: "+ str(eachQ))
            qN = removePattern(qList1[i], p)
            #nPar = nParent+qList1[i]
            logger.debug(instrxn+'\s'+eachQ)
            logger.debug("n: "+str(qN)+" p: "+p+" nParent: "+nParent)
            self.analyseQuestion(instrxn+'\s'+eachQ, qN, p, nParent, group,
                                 True, marks)

    def LAQmarks(self, q):
        '''
        returns question statement and marks
        q=Q statement of LAQ
        '''
        q.strip("\n").strip("\s")
        logger.debug("Inside LAQmarks, q:")
        logger.debug(str(q))
        logger.debug("q ended here")
        #z = re.findall(r'[\s\n]\(?([\w\s\d\n]*\d+\)?[\s\n]*)', q)
        z = re.findall(r'\n(\(?[\w\s]*\d+[\w\s\d]*\)?)\s*', q)
        logger.debug("z:"+ str(z))
        if z:
            z = str(z[len(z)-1])
            z.strip("\n")
            logger.debug("After strip() newline, z:"+str(z))
        logger.debug("Type(z):"+ str(type(z)))
        s = str(q)
        i = s.rfind(z)
        marks = Marks.marks(z)
        logger.debug("Marks:"+ str(marks))
        s = s[:i].strip()
        logger.debug("After splitting based on marks, q:"+ str(s))
        return s, marks

    def newLAQ(self, qData, m,  qN='', group='A'):
        '''
        finds relevant data required to create
        a new object of Question.Question
        returns them as dict
        '''
        ## TODO
        self.newQn = self.newQn+1
        #print "new LAQ created"
        #print "\n********\nnew LAQ created\n********\n"+str(qN)+q+str(m)+"\n"
        index = qData.find('[Figure_Here]')
        size = 13
        if index > -1:
            #has figure
            hasFigure=True
            qData = qData[:index]+qData[index+13:]
            logger.debug("Question data final: "+qData)
        else:
            hasFigure=False
        q = Question.Question(marks=m[1], laq=qData, qNo=qN,
                              session=self.session, year=self.year,
                              subject=self.subject, hasFig=hasFigure)
        #print "Question data final:"+qData
        if hasFigure:
            q.setFigName
        if group=='A':
            self.groupA.append(q)
        elif group=='B':
            self.groupB.append(q)
        else:
            self.groupC.append(q)

        q.setSyllabus()
        #print q.syllabus
        q.insertInDB(self.id)
        
def construct(pat, n):
    '''
    pat is a string, n is string
    Returns a constructed question number using
    pattern pat and question number n
    if pat=".", n=a
    return a.
    if pat=(), n=1
    return (1)
    '''
    if not(type(n) == str):
        n = str(n)
    if len(pat) == 0:
        try:
            raise ValueError("Construct issue, pattern not found")
        except ValueError as e:
            logger.warning(str(e.args))
            return n
    elif len(pat) == 1:
        return n+pat
    elif len(pat) == 2:
        return pat[0]+n+pat[1]
        
def findPattern(q):
    '''
    returns a string containing only pattern, works on digits as well as
    alphabets
    e.g., 1.=>.
    1)=>)
    (A)=>()
    '''
    pat = re.search(r'([^\s\d\w]*)[\d\w]+([^\s\d\w]+)', q)
    if pat:
        pat = pat.group(1)+pat.group(2)
        return pat
    else:
        return ''

def removePattern(q, pat=''):
    '''
    returns Q No., using the pattern pat
    q=(a)
    pat='()'
    returns 'a'
    If nothing matches or found, returns '0' as error
    '''
    if pat=='':
        pat = findPattern(q)
    q.strip()
    if len(pat)==0:
        try:
            raise ValueError("Pattern not found")
        except ValueError as err:
            logger.warning(str(err.args))
        return q
    elif len(pat)==1:
        return q[:len(q)-1]
    elif len(pat)==2:
        return q[1:len(q)-1]
    else:
        return '0'
    

def findNextQ(q):
    '''Returns the next Q No. for any of the following series:
    a, A, 1, i, I
    Returns '0' if none found
    '''
    romanList = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii',
                 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi',
                 'xvii', 'xviii', 'xix', 'xx']
    RomanList = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
                 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI',
                 'XVII', 'XVIII', 'XIX', 'XX']
    aList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
             'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
    AList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    nList=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
           '12', '13', '14', '15', '16', '17', '18', '19', '20']
    logger.debug("Inside FindNextQ:"+ str(q))
    logger.debug("type(q):"+ str(type(q)))
    q.strip()
    for i in range(19):
        if aList[i] == q:
            logger.info("Next q found: "+ str(aList[i+1]))
            return aList[i+1]
        elif AList[i] == q:
            logger.info("Next q found: "+ str(AList[i+1]))
            return AList[i+1]
        elif nList[i] == q:
            logger.info("Next q found: "+ str(nList[i+1]))
            return nList[i+1]
        elif romanList[i] == q:
            logger.info("Next q found: "+ str(romanList[i+1]))
            return romanList[i+1]
        elif RomanList[i] == q:
            logger.info("Next q found: "+ str(RomanList[i+1]))
            return RomanList[i+1]
    else:
        return '0'

def qSort(l):
    '''
    returns sorted list
    l is a simple list of questions, along with pattern
    Uses python's inbuilt sort function
    '''
    l.sort()
    l1 = list(l)
    pat = findPattern(l1[0])
    logger.debug(str(pat))
    st = ''
    # remove pattern from l1
    for i in range(len(l1)):
        l1[i] = removePattern(l1[i], pat)
        st = st+l1[i]
    #
    if st.find('a')>-1 or st.find('A')>-1:
        # not roman, not numeric
        # default sort function works well
        pass
    elif st.find('1')>-1:
        # numeric
        for i in range(len(l1)):
            l1[i] = int(l1[i])
        l1.sort()
    else:
        # roman numerals
        # map each numeral to integer, sort integer
        # make new list as per sorted integers
        s = {}
        rList = {1:'i', 2:'ii', 3:'iii', 4:'iv', 5:'v', 6:'vi', 7:'vii',
                     8:'viii', 9:'ix', 10:'x', 11:'xi', 12:'xii', 13:'xiii',
                     14: 'xiv', 15:'xv', 16:'xvi', 17:'xvii', 18:'xviii',
                     19:'xix', 20:'xx'}
        for each in l1:
            s[rList.keys()[rList.values().index(each.lower())]] = each
        l1 = []
        for each in s.keys():
            l1.append(each)
        l1.sort()
        l2 = []
        for each in l1:
            item = construct(pat, s[each])
            l2.append(item)
        return l2        
    
    ## construct back list and return
    for i in range(len(l1)):
        l1[i] = construct(pat, l1[i])
    return l1


## to test
## text = ['Winter 2018', 'Summer 2018']
#dat = "SUMMER 2019\nFUNDAMENTALS OF DESIGN AND MANUFACTURING\nTime: Three hours\nMaximum marks: 100\nAnswer FIVE questions, taking ANY TWO from Group A,\nANY TWO from Group B and ALL from Group C.\nAll parts of a question (a, b, etc) should be answered at one place.\nAnswer should be brief and to-the-point and be supplemented with neat sketches. Unnecessary long\nanswers may result in loss of marks.\nAny missing data or wrong data may be assumed suitably\nFigures on right-hand side margin indicate full marks.\nGroup A\n1. (a) What is design? Name the check list for engineering design problems.\n8\n(b) How design by evolution is different from routine design?\n8\n(c) How artificial intelligence can be used in designing a product?\n4\n2. (a) Explain the various methods of design communication.\n8\n(b) What is product life cycle? Illustrate with a suitable example, the various stages of product life cycle.\n8\n(c) Describe the process of brainstorming.\n4\n3. (a) with suitable diagrams briefly explain sand casting processes.\n8\n(b) Describe following type of sand :\n8\n(1) Loam Sand (2) Facing Sand (3) Backing sand (4) Parting sand.\n(c) Why riser are used in casting?\n4\n4. (a) What is rolling and types of rolling in metal working ? For which type of products the method is suitable.\n8\n(b) Explain progressive die and compound die with suitable diagram.\n8\n(c) What is the purpose of heat treatment of forging?\n4\nGroup B\n5. (a) Differentiate between shaping , planning and slotting as regards to relative tool and work motions.\n8\n(b) The following data from the orthogonal cutting test is available:\nRake angle = 10degree, chip thickness ratio = 0.35, uncut chip thickness = 0.51, width of cut = 3mm, yield shear stress of work material = 285 N/mm 2 , Mean friction Coefficient on tool face = 0.65. Determine cutting force, Normal force and Shear force on the tool.\n8\n(c) Following is the data available on cutting speed and too life. Determine the Taylors constant and tool life exponent.\n4\n(1) V = 150 m/min, T = 60 min\n(2) V = 200 m/min, T = 23 min\n6. (a) Describe different types of centre less grinding. For which type of product manufacturing they are quite suitable. Write down the limitation of the process.\n8\n(b) Compare and contrast electro-discharge machining and electrochemical machining processes.\n8\n(c) What process would you recommend to make many small holes in a very hard alloy when the holes will be used for cooling and venting?\n4\n7. (a) What is computer Aided process planning (CAPP)? How is it superior to manual Process planning? Explain.\n8\n(b) What are the guidelines to design for producibility in case of casting and forging?\n8\n(c) Describe the welding process commonly used to weld rail track with the aid of a neat diagram.\n4\n8. (a) Explain briefly with an example the OPTIZ classification system.\n8\n(b) Discuss the basic element of an industrial robot.\n8\n(c) What is cluster analysis?\n4\nGroup C\n9. Answer the following :\n10x2\n(1) What is Organizational need?\n(2) What is concurrent engineering?\n(3) For what carbon dioxide casting are used for?\n(4) What is the effect of temperature in metal forming?\n(5) Define oblique cutting.\n(6) Honing is used for?\n(7) Carburizing flame are used for welding which type of materials?\n(8) Define AS & RS.\n(9) Function of dielectric in EDM.\n(10) Define Robust design."
#dat = "Winter 2018\nCOMPUTING AND INFORMATICS\nTime: Three hours.\nMaximum Mark: 100\nAnswer FIVE questions, taking ANY TWO from Group A,\nANY TWO from Group B and ALL from Group C\nAll parts of a question (a,b,c etc.) should be answered at one place.\nAnswer should be brief and to-the-point and be supplemented with neat sketches. Unnecessary long\nanswers may result in loss of marks.\nAny missing or wrong data may be assumed suitably giving proper justification\nFigures on the right-hand side margin indicate full marks.\nGroup A\n1. (a) Write the properties of an algorithm. Write an algorithm to check whether a given integer is odd or even. Verify that the properties are satisfied with the above algorithm.\n(5)\n(b) Write a program in C to find the sum of digits of a given integer using macros.\n(5)\n(c) Illustrate the use of switch, case and break statement in C with examples.\n(5)\n(d) Write the difference between call-by-value and call-by-reference. Which among these is a better option of parameter passing. Justify your answer with necessary example.\n(5)\n2. (a) Write a program in C to reverse a string without using function strrev(). Specify the name of header files that defines string function in C.\n(10)\n(b) Write a program in C to find the median of 20 elements stored in an unsorted array A[20].\n(10)\n3. (a) What do you understand by DBMS and DBA? Write different data base models which data base model in practical and used in application. Explain the role of DBA in DBMS.\n(8)\nb) How a client-server architecture is different from peer-peer architecture? Explain with examples.\n(6)\n(c) Which protocol stack is used for the Internet? Explain briefly the function of each layer of protocol stack.\n(6)\n4. (a) What do you understand by information system? Explain five phases of information system. Explain the design of information system using SDLC.\n(8)\n(b) What do you mean by diagramming a business process? Explain with an appropriate diagram.\n(6)\n(c) How office automation cell of an organisation improves the business process?\n(6)\nGroup B\n5. (a) Arrange various storage devices in a digital computer in increasing order of their retrieval speed and storage capacity. Define seek time and latency with respect to various storage devices.\n(7)\n(b) Why DRAMS are slower as compared to SRAM? Specify the used of SRAM and DRAM in a digital computer.\n(6)\n(c) Illustrate the mechanism to read and write a data type in both fixed and movable head disk system.\n(7)\n6. (a) Differentiate between paging and segmentation specify the hardware needed to implement paging and segmentation.\n(7)\n(b) What is disk cache? How it is different from cache memory used in hierarchical memory system?\n(6)\n(c) Explain the comparison between block, page, and segment in memory management system.\n(7)\n7. (a) What are the universal logic gates? Develop a 3-to-8 6 decoder using universal logic gates.\n(5)\n(b) Justify that a flip-flop is a sequential logic device with appropriate example.\n(5)\n(c) What is the role of clock in a digital computer? Is it possible to have different clock for different components in a digital computer? Justify answer with example.\n(5)\n(d) Increasing clock speed of a digital computer will not improve the performance. Justify.\n(5)\n8. (a) Write an algorithm to convert a 3-digit hexadecimal number to its corresponding octal number.\n(4)\nb) Convert: (i) (53AB) 16 , to (?) 8 ,\n(ii) (6293) 10 , to (?) 4\n(4)\n(c) Write the truth table of a full adder and the corresponding logic circuit with minimal number of logic gates.\n(8)\n(d) What do you understand by tristate device? Explain with examples.\n(4)\nGroup C\n9. Answer the following:\n10 x 2\n(i) Justify the use of a shared bus for address, data and control signals\n(ii) Write at least two common characteristics of high level languages.\n(iii) Give an example of macros used in language C.\n(iv) Justify that an information system is more than a computer\n(v) Differentiate between syntax and semantic errors in a program.\n(vi) Write the name of registers used for storing the base address of a page and a segment respectively in a computer system.\n(vii) Write at least two differences between compiler and interpreters\n(viii) What is the difference between user and Kernel space?\n(ix) What do you mean by command line arguments?\n(x) What do you mean by payload in a TCP/IP packet format?\n"
#q = QuestionPaper(rawdata=dat)
#q.analyseHead()
