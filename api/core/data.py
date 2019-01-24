import sqlite3 as sql3
import settings

def get_db(DATABASE):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql3.connect(DATABASE)
    return db

def get_data(DATABASE, queryType, filters=None):
    # queryString = [v if k == queryType else Null for query in settings.DB_QUERIES for k,v in query.items()]
    for query in settings.DB_QUERIES:
        for k,v in query.items():
            if k == queryType:
                con = sql3.connect(DATABASE)
                cur = con.cursor()
                queryString = v.format(**filters) if filters != None else v
                print (queryString)
                query = cur.execute(queryString)
                colname = [ d[0] for d in query.description ]
                datum = [dict(zip(colname, r)) for r in query.fetchall()]
                con.close()
    return datum
    