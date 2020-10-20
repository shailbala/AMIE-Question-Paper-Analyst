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
        return conn
    except Error as e:
        print(e)
 
    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        print type(e)

def main():
    database = "app.db"

    createSubjectTable = '''CREATE TABLE IF NOT EXISTS subject (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            subjectName text NOT NULL,
                            code text NOT NULL
                        ); '''
 
    createSyllabusTable = """ CREATE TABLE IF NOT EXISTS syllabus (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            topic text NOT NULL,
                            subjectId integer NOT NULL,
                            FOREIGN KEY (subjectId) REFERENCES subject (id)
                        ); """
 
    createGroupTable = """CREATE TABLE IF NOT EXISTS grp (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            type text NOT NULL
                        ); """
    
    createFigureTable = """CREATE TABLE IF NOT EXISTS figure (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            figName text NOT NULL,
                            figLink text
                        );"""

    createQuestionPaperTable = """CREATE TABLE IF NOT EXISTS questionPaper (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            session text NOT NULL,
                            year text NOT NULL,
                            subjectId integer NOT NULL,
                            FOREIGN KEY (subjectId) REFERENCES subject (id)
                        );"""
    
    createQuestionTable = """CREATE TABLE IF NOT EXISTS question (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            qNo text NOT NULL,
                            qText text NOT NULL,
                            hasFig BOOLEAN NOT NULL CHECK (hasFig IN (0,1)),
                            figId integer NOT NULL,
                            syllabusId integer NOT NULL,
                            qPaperId integer NOT NULL,
                            marks integer NOT NULL,
                            FOREIGN KEY (figId) REFERENCES figure (id),
                            FOREIGN KEY (syllabusId) REFERENCES syllabus (id),
                            FOREIGN KEY (qPaperId) REFERENCES questionPaper (id)
                        );"""
 
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create
        create_table(conn, createSubjectTable)
        create_table(conn, createSyllabusTable)
        create_table(conn, createGroupTable)
        create_table(conn, createFigureTable)
        create_table(conn, createQuestionPaperTable)
        create_table(conn, createQuestionTable)
    else:
        print("Error! cannot create the database connection.")
 
if __name__ == '__main__':
    main()
