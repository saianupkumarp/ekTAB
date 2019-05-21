from gevent import monkey
monkey.patch_all()
from flask import make_response, request
from pySMP import model
import sqlite3 as sql3
import os
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
    
def run_task(file_id, args):
    if args['app_mode'] == 'dsk':
        conn_string = 'Driver=QSQLITE;Database={}'.format(os.path.join(settings.UPLOAD_PATH, 'db', file_id))
    elif args['app_mode'] == 'web':
        # TODO POSTGRES
        conn_string = "DUMMY"

    thisSMP = model.SMP()
    thisSMP.setDatabase(conn_string)
    try:
        scenID = thisSMP.runModel(tuple(args['sqlFlags']),os.path.join(settings.UPLOAD_PATH, 'csv', file_id+'.csv'),args['seed'],args['saveHist'],tuple(args['modelParams']))
        # Get Data Dimensions
        actorCnt = thisSMP.getNumActors()
        dimensionCnt = thisSMP.getNumDimensions()
        stateCnt = thisSMP.getNumStates()
        posHists = thisSMP.getPositionHistory()

        # Delete the input file
        delete_input_file(file_id, 'csv')
        # returning the result set
        return (scenID, actorCnt, dimensionCnt, stateCnt, posHists)
    except Exception as e:
        print (e)
        print ("Error while running the model")
        err = thisSMP.getLastError()
        return err

def dictTup(arg_list):
    val_tup = []
    for dic_arg in arg_list:
        val_tup.extend(dic_arg.values())
    return tuple(val_tup)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

def delete_input_file(file_id, path):
    os.remove(os.path.join(settings.UPLOAD_PATH, path, file_id+'.csv'))
    return