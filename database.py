import sqlite3
from itsdangerous import json
import pandas as pd

def connect_to_db():

    conn = sqlite3.connect("database.db")
    return conn

def create_details_db_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS animation (
                name TEXT,
                gender TEXT,
                weight TEXT,
                height TEXT,
                videoname TEXT
            );
        ''')
        conn.commit()
        print("Details table created successfully")
    except:
        print("Table creation failed - details data")

def create_humanModel_db_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS humanModel (
                index INTEGER,
                id INTEGER,
                time INTEGER NOT NULL,
                parts TEXT,
                joint TEXT,
                label INTEGER,
                x REAL NOT NULL,
                y REAL NOT NULL,
                z REAL NOT NULL,
                angle TEXT,
                analysis REAL,
                status TEXT
            );
        ''')


        conn.commit()
        print("Table created successfully")
    except:
        print("Table creation failed - human model")



def create_animation_db_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS animation (
                range TEXT,
                data TEXT,
                layout TEXT,
                frames TEXT
            );
        ''')
        conn.commit()
        print("Table created successfully")
    except:
        print("Table creation failed - animation data")
        

def create_2Danimation_db_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS twoDanimation (
                range TEXT,
                data TEXT,
                layout TEXT,
                frames TEXT
            );
        ''')

        conn.commit()
        print("Table created successfully")
    except:
        print("Table creation failed - 2D animation data")

def create_3Danimation_db_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS threeDanimation (
                range TEXT,
                data TEXT,
                layout TEXT,
                frames TEXT
            );
        ''')

        conn.commit()
        print("Table created successfully")
    except:
        print("Table creation failed - 3D animation data")

def create_graph_db_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS graph (
                range TEXT,
                e TEXT
            );
        ''')

        conn.commit()
        print("Table created successfully")
    except:
        print("Table creation failed - graph data")

def create_analysis_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS analysis(
                frame INTEGER,
                leftkneeangle REAL,
                rightkneeangle REAL,
                leftelbowangle REAL,
                rightelbowangle REAL,
                pelvisalign REAL,
                shoulderalign REAL,
                bodyalign REAL
            )
        ''')
        conn.commit()
        print("Table created successfully")
    except:
        print("Table creation failed - analysis data")

def insert_humanModel_data(conn, df):
    try:
        """
        cur = conn.cursor()
        cur.execute("INSERT INTO humanModel (Time, Parts, Joint, Label, X, Y, Z) VALUES (?, ?, ?, ?, ?)", 
                    (df['Time'],   
                    df['Parts'], df['Joint'], df['Label'],   
                    df['X'], df['Y'], df['Z']) )
        """

        #cur.executemany("INSERT INTO humanModel VALUES (?,?, ?,?,?,?,?,?)", df)
        df.to_sql(name='humanModel', con=conn, if_exists='replace')
        conn.commit()
    except:
        print("Human Model: ",conn().rollback())
        raise Exception(conn().rollback())

def insert_details_data(conn, details):
    try:
        cur = conn.cursor()
       
        detail = json.loads(details)
        cur.execute("REPLACE INTO animation ('name','gender','weight','height','videoname') VALUES (?,?,?,?,?) ",(detail[0],detail[1],detail[2],detail[3],detail[4]))

        conn.commit()
    except:
        raise Exception(conn().rollback())

def insert_animation_data(conn, figs):
    try:
        cur = conn.cursor()
        for f in figs:
            fig = json.loads(figs[f])
            cur.execute("REPLACE INTO animation ('range','data','layout','frames') VALUES (?,?,?,?) ",(f, json.dumps(fig['data']),json.dumps(fig['layout']),json.dumps(fig['frames'])))

        conn.commit()
    except:
        print("Anime: ",conn().rollback())
        raise Exception(conn().rollback())

def insert_2Danime_data(conn, figs):
    try:
        cur = conn.cursor()
        for f in figs:
            fig = json.loads(figs[f])
            cur.execute("REPLACE INTO twoDanimation ('range','data','layout','frames') VALUES (?,?,?,?) ",(f, json.dumps(fig['data']),json.dumps(fig['layout']),json.dumps(fig['frames'])))

        conn.commit()
    except:
        raise Exception(conn().rollback())

def insert_3Danime_data(conn, figs):
    try:
        cur = conn.cursor()
        for f in figs:
            fig = json.loads(figs[f])
            cur.execute("REPLACE INTO threeDanimation ('range','data','layout','frames') VALUES (?,?,?,?) ",(f, json.dumps(fig['data']),json.dumps(fig['layout']),json.dumps(fig['frames'])))

        conn.commit()
    except:
        raise Exception(conn().rollback())

def insert_graph_data(conn, graphs):
    try:
        cur = conn.cursor()
        for g in graphs:
            e = json.loads(graphs[g]['E'])

            cur.execute("REPLACE INTO graph ('range', 'e') VALUES (?,?) ",(g, json.dumps(e)))

        conn.commit()
    except:
        print("Graph: ",conn().rollback())
        raise Exception(conn().rollback())

def insert_analysis_data(conn, data):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO analysis ('frame','leftkneeangle','rightkneeangle','leftelbowangle','rightelbowangle','pelvisalign','shoulderalign','bodyalign') VALUES (?,?,?,?,?,?,?,?) ",
                (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
        )
        conn.commit()
    except:
        raise Exception(conn().rollback())

def dropTable(conn, tableName):
    cursor = conn.cursor()
    str = "DROP TABLE IF EXISTS " + tableName
    cursor.execute(str)
    conn.commit()

    
def close(conn):
    conn.close()

def inithumanModelData(conn, df):
    create_humanModel_db_table(conn)
    insert_humanModel_data(conn, df)

def initAnimationData(conn, graphJson):
    dropTable(conn,"animation")
    create_animation_db_table(conn)
    insert_animation_data(conn, graphJson)

def init2DAnimationData(conn, graphJson):
    dropTable(conn, "twoDanimation")
    create_2Danimation_db_table(conn)
    insert_2Danime_data(conn, graphJson)

def init3DAnimationData(conn, graphJson):
    dropTable(conn, "threeDanimation")
    create_3Danimation_db_table(conn)
    insert_3Danime_data(conn, graphJson)

def initGraph(conn, graphJson):
    
    dropTable(conn, "graph")
    create_graph_db_table(conn)
    insert_graph_data(conn, graphJson)

def initDetails(conn, details):
    dropTable(conn, "details")
    create_details_db_table(conn)
    insert_details_data(conn, details)


def retrieveAnimationData(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM animation")
    rows = cur.fetchall()

    return rows

def retrieveDetailsData(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM details")
    rows = cur.fetchall()

    return rows

def retrieve2DAnimationFromRange(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM twoDanimation")
    rows = cur.fetchall()

    return rows

def retrieveGraph(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM graph")
    rows = cur.fetchall()

    return rows

def retrieveDataFrameFromFrame(conn,f):
    commandStr = "SELECT * FROM humanModel WHERE time='" + str(f) + "'"
    return pd.read_sql_query(commandStr, conn)

def retrieve3DAnimationFromRange(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM threeDanimation")
    rows = cur.fetchall()

    return rows

def retrieveAllAnalysis(conn):
    #cur = conn.cursor()
    commandStr ='select time,angle,analysis,status from humanModel where analysis is not null and trim(analysis," ")!=""'
    #cur.execute(commandStr)
    #rows = cur.fetchall()
    return pd.read_sql_query(commandStr, conn)

def retrieveAnalysisAverageFromLabel(conn, label):
    cur = conn.cursor()
    #str = "SELECT AVG(leftkneeangle), AVG(rightkeeangle), AVG(leftelbowangle), AVG(rightelbowangle), AVG(pelvisangle), AVG(shoulderalign), AVG(bodyalign), FROM analysis WHERE frame='" + f + "'"
    commandStr = "SELECT AVG(Analysis) FROM humanModel WHERE label=" + str(label)
    cur.execute(commandStr)
    rows = cur.fetchone()[0]
    return rows


if __name__ == '__main__':
    retrieve2DAnimationFromRange()