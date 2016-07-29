"""
    Handel all the documents (json files) that has the data
    -> View data
    -> Insert data
    -> Edit data
    -> Delete data

    @return
        When document created successfully (data inserted) then it will return the id of that document, which
        is helpful for refferencing this document in other queries
"""
from leandbHelper import *
import os
import shutil

def insertData( commandJsonObj, databaseStorage ):
    ret = {}
    missing = False
    missedItems = []

    pathEnding = pathEndWith()

    tableAbsolutePath =  databaseStorage+commandJsonObj['databaseName']+pathEnding+commandJsonObj['tableName']
    tableConfigFile = tableAbsolutePath+pathEnding+'_ldb'+pathEnding
    tableSystemID = tableConfigFile+'id'

    # validate the query
    if( not commandJsonObj['databaseName'] or commandJsonObj['databaseName'] == "" ):
        missing = True
        missedItems.append("databaseName")
    if( not commandJsonObj['tableName'] or commandJsonObj['tableName'] == "" ):
        missing = True
        missedItems.append("tableName")
    if( not commandJsonObj['data'] ):
        missing = True
        missedItems.append("data")

    if( missing == False ):
        # Attempt to cretate a new table directory
        # If the database was not found then it will 
        # try to create the database directory first and then table dir.
        if( not os.path.isdir( tableAbsolutePath ) ):
            try:
                os.makedirs( tableAbsolutePath )
                ret['status'] = [
                    { 'status_type': True },
                    { 'status_message': 'Table '+commandJsonObj['tableName']+' created successfully' }
                ]
            except Exception as e:
                ret['status'] = [
                    { 'status_type': False },
                    { 'status_message': 'Error while creating table: '+str(e.args) }
                ]
                # exit because there was trouble while creating the database and table directories
                return ret
        # descide the document id
        try:
            with open( tableSystemID, 'r+' ) as docID:
                # currentID = int( docID.read() )
                currentID = docID.read()
                docID.seek(0)
                documentID = str(int(currentID)+1)
                docID.write( documentID )
                docID.close()
        except Exception as e:
            ret['status'] = [
                { 'status_type': False },
                { 'status_message': 'Error while writing document id. ' + str(e.args) }
            ]
            # exit because there was trouble
            return ret
        # create the data file
        try:
            writeJson( commandJsonObj['data'], tableAbsolutePath+pathEnding+documentID+'.ldb' )
        except Exception as e:
            ret['status'] = [
                { 'status_type': False },
                { 'status_message': 'Error while writing document: '+str(e.args) }
            ]
            # exit because there was trouble
            return ret
        # create primary id index
        with open( tableAbsolutePath+pathEnding+'_ldb'+pathEnding+'_index'+pathEnding+'pid', 'a+' ) as pkid:
            print( documentID, file=pkid )
        # check for index items
        if '_index' in commandJsonObj:
            # split using comma to find individual index elements
            indexTags = str(commandJsonObj['_index']).split(',')
            for indexItem in indexTags:
                # create individual index documents
                indexItem = stripWhiteSpaces( indexItem )
                try:
                    with open( tableAbsolutePath+pathEnding+'_ldb'+pathEnding+'_index'+pathEnding+indexItem, 'a+' ) as pkid:
                        print( '"'+documentID+'" "'+encodeIndexString( commandJsonObj['data'][indexItem] )+'"', file=pkid )
                except Exception as e:
                    ret['status'] = [
                        { 'status_type': True },
                        { 'status_message': 'Error while writing index for "'+indexItem+'": '+str(e.args) }
                    ]
        ret['id'] = documentID
    else:
        ret['status'] = [
            { 'status_type': False },
            { 'status_message': 'Error while inserting data: '+str( missedItems )+' values are missing' }
        ]
    return ret

def fetchData( commandJsonObj, databaseStorage ):
    # is database and table exists
    # is there is any where conditions
    # is there is a limit tag
    