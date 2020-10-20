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

def queryQuestionTable(conn, subId = 0):
    '''Query from question table, syllabusId and
    sum of marks belonging to
    one syllabusId
    Show on screen a mapping of syllabusId,
    syllabus topic, and marks'''
    cur = conn.cursor()
    cur.execute('''SELECT question.syllabusId, topic, topicHead,
                     SUM(marks)
                    FROM question
                INNER JOIN syllabus ON syllabus.id = question.syllabusId
                WHERE qPaperId BETWEEN 21 AND 38
                GROUP BY
                 question.syllabusId
                ORDER BY
                 SUM(marks) DESC;''')
    rows = cur.fetchall()

    cur.execute('''SELECT * FROM syllabus_topic''')
    syl_headers = cur.fetchall()
    head = dict(syl_headers)
    printQueriedData(rows, head)

def printQueriedData(rows, header):
    
    print "Querying data from database..."
    print "Data arranged according to important topics in past 10 years:"
    print "\n----------------------------"
    print "\nMain Topic->Sub topic: Marks"
    print "\n----------------------------"

    totalMarks = 0
    for each in rows:
        #print each[3]
        totalMarks = totalMarks + each[3]
    #print totalMarks
        
    i = 0
    res = []
    for row in rows:
        print str(header[row[2]]+"->"+row[1]+": "+str(row[3]))
        if i<5:
            res.append(str(header[row[2]]+"->"+row[1]+": "+str(row[3])))
            i = i+1

    print "\n--------------------------------------------------------"
    print "\nFrom this data, we confer the 5 most important topics are:"
    print "\n--------------------------------------------------------"
    for each in res:
        print each


def main():
    database = "app.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        queryQuestionTable(conn)

if __name__ == '__main__':
    main()
