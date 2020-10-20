import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str
        return conn
    except Error as e:
        print(e)
 
    return None

def insertInSubject(conn, subject):
    """
    Create a new project into the projects table
    :param conn:
    :param subject:
    :return: subject id
    """
    sql = ''' INSERT INTO subject(subjectName,code)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, subject)
    return cur.lastrowid

def insertInSyllabus(conn, syl):
    """
    Create a new project into the projects table
    :param conn:
    :param syl:
    :return: syllabus id
    """
    sql = ''' INSERT INTO syllabus(topic, topicHead, subjectId)
              VALUES(?,?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, syl)
    return cur.lastrowid

def insertInFigure(conn, fig):
    """
    Create a new project into the projects table
    :param conn:
    :param fig:
    :return: figure id
    """
    sql = ''' INSERT INTO figure(figName, figLink)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, fig)
    return cur.lastrowid

def insertInQuestionPaper(conn, qPaper):
    """
    Create a new project into the projects table
    :param conn:
    :param qPaper:
    :return: QuestionPaper id
    """
    sql = ''' INSERT INTO question_paper(session, year, subjectId)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, qPaper)
    return cur.lastrowid

def insertInQuestion(conn, q):
    """
    Create a new project into the projects table
    :param conn:
    :param q:
    :return: question id
    """
    sql = ''' INSERT INTO question(qNo, qText, hasFig, figId,
            syllabusId, qPaperId, marks)
            VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, q)
    return cur.lastrowid

def updateInSubject(conn, subject):
    """
    Create a new project into the projects table
    :param conn:
    :param subject:
    """
    sql = ''' UPDATE subject
                SET subjectName = ?,
                code = ?
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, subject)

def updateInSyllabus(conn, syl):
    """
    Create a new project into the projects table
    :param conn:
    :param syl:
    """
    sql = '''UPDATE syllabus
            SET topic = ?,
            subjectId = ?
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, syl)

def updateInFigure(conn, fig):
    """
    Create a new project into the projects table
    :param conn:
    :param fig:
    """
    sql = '''UPDATE figure
            SET figName = ?,
            figLink = ?
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, fig)

def updateInQuestionPaper(conn, qPaper):
    """
    Create a new project into the projects table
    :param conn:
    :param qPaper:
    """
    sql = ''' UPDATE question_paper
            SET session = ?,
            year = ?,
            subjectId = ?
              WHERE id = ?  '''
    cur = conn.cursor()
    cur.execute(sql, qPaper)

def updateInQuestion(conn, q):
    """
    Create a new project into the projects table
    :param conn:
    :param q:
    """
    sql = '''UPDATE question
            SET qNo = ?,
            qText = ?,
            hasFig = ?,
            figId = ?,
            syllabusId = ?,
            qPaperId = ?,
            marks = ?
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, q)

def deleteRow(conn, tableName, i):
    """
    Delete a row in tableName by id i
    :param conn:  Connection to the SQLite database
    :param tableName: Name of the table to delete rows from
    :param i: id of the row
    :return:
    """
    sql = "DELETE FROM "+tableName+" WHERE id=?"
    cur = conn.cursor()
    cur.execute(sql, (i,))

def deleteAllRows(conn, tableName):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :param tableName: Name of the table to delete rows from
    :return:
    """
    sql = 'DELETE FROM '+tableName
    cur = conn.cursor()
    cur.execute(sql)

def updateAnyTable(conn, tableName, column, i):
    # TODO
    pass

def getGrpId(g):
    grp = {'A': 1, 'B':2, 'C':3}
    r = grp.get(g.upper(), 0)
    return r

def getSubjectId(sub):
    subject = {'engineering management': 5,
               'society and environment':4,
                'material science and engineering': 3,
                'fundamentals of design and manufacturing': 1,
                'computing and informatics': 2,
               'material science':3}
    r = subject.get(sub.lower(), 0)
    return r

def main():
    database = "app.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new subject
        pass

if __name__ == '__main__':
    main()



# grp, are static tables, once populated, they will not be updated
# grp = {'A': 1, 'B':2, 'C':3}

# following tables can be updated as per requirement
# but only from here manually
'''
subject = {'Engineering Management': 5,
'Society and Environment':4,
'Material Science and Engineering': 3,
'Fundamentals of Design and Manufacturing': 1,
'Computing and Informatics': 2}


sub = ['Fundamentals of Design and Manufacturing',
               'Computing and Informatics',
               'Material Science and Engineering',
               'Society and Environment',
               'Engineering Management']
code = ['AD 301', 'AD 303', 'AD 302', 'AD 304', 'IC 402']
'''

# dynamic tables
# these can be updated using functions
# syllabus
# questionPaper, figure, question
