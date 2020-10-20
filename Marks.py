import re

def marks(line):
    '''
    Returns the number of questions and
    marks of each question as a list of len 2
    5x4 => [5, 4] : 5 questions of 4 marks each
    5M => [1, 5] : 
    '''
    
    if not(type(line) == str) or line=='':
        try:
            raise ValueError('invalid line for marks', line)
        except ValueError as err:
            print err.args
    else:
        ## remove brackets and trailing spaces, if present
        line = line.strip().strip("(").strip(")").strip()
        #print "brackets removed:", line
        
        ## for (S 2016 20M ), without brackets S 2016 20M
        z = re.findall(r'.+\d{4}\s(.+)', line)
        #print "z:", z
        if z:
            line = z[0]
            #print "line 26:", line
            
        ## Search for letter M
        i = line.find('M')
        if i > -1:
            line = line[:i]
            #print "letter M removed, line:", line
            
        ## Search for +
        if line.find('+') > -1:
            line = line.split('+')
        ## there may be trailing whitespaces, remove them
        if type(line) == list:
            sumQ = 0
            for i in range(len(line)):
                ## remove trailing whitespaces using some inbuilt str function
                ## convert each item into int
                line[i] = line[i].strip()
                line[i] = int(line[i])
                sumQ = sumQ + line[i]
            #print "split based on +, line: ", line
            ## presence of + means it is LAQ
            ## return no. of questions=1, marks=sum of all in list
            return [1, sumQ]
        
        ## Search for 'x', 4x2 M
        if line.find('x') > -1:
            i = line.find('x')
            line = line.split('x')
        else:
            i = line.find('X')
            line = line.split('X')
        if i>-1:
            #print line
            ## remove trailing whitespaces, convert to int
            for i in range(len(line)):
                line[i] = int(line[i].strip())
            return line

        ## Search for '*', 10*2 means 10Qs of 2 marks each
        line = str(line[0])
        if line.find('*') > -1:
            i = line.find('*')
            line = line.split('*')
            #print line
            for i in range(len(line)):
                #print line[i]
                line[i] = int(line[i].strip())
            return [line[1], line[0]]
        
        ## None matches, default 1 question and marks is in line
        #print "line[0]:", line[0]
        return [1, int(line[0])]



#r = '(7+ 7 +6M)'
#r = '8M'
#r = '2+3'
#r = '2x 3'
#r = '\n(2x3)'
#r = '(2)'
r = '(S 2016 20M )'
#r = '(2X3 M )'
#r = '10*2'
#r = '( 10M)'
print marks(r)
