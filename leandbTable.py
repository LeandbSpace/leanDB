"""
    Handle a table inside a database
    Both table and database fundamentally a directory.
    -> Create Table
    -> Delete Table
    -> Rename Table
"""

from leandbHelper import *
import os
import shutil

pathEndsWith = pathEndWith()

# fetch and assign leandb configuration data
# configData = starterConf()

def createTable( commandJsonObj, databaseStorage ):
    ret = {}
    missing = False
    missedItems = []

    if( not commandJsonObj['databaseName'] or commandJsonObj['databaseName'] == "" ):
        missing = True
        missedItems.append("databaseName")
    if( not commandJsonObj['tableName'] or commandJsonObj['tableName'] == "" ):
        missing = True
        missedItems.append("tableName")
    if( missing == False ):
        tableAbsolutePath =  databaseStorage+commandJsonObj['databaseName']+pathEndsWith+commandJsonObj['tableName']+pathEndsWith+'_ldb'+pathEndsWith+'_index'
        # Attempt to cretate a new table directory
        # If the database was not found then it will 
        # try to create the database directory first and then table dir.
        if( not os.path.isdir( tableAbsolutePath ) ):
            tableCreated = False
            try:
                os.makedirs( tableAbsolutePath )
                ret['status'] = { 
                    'status_type': True,
                    'status_message': 'Table '+commandJsonObj['tableName']+' created successfully' 
                }
                tableCreated = True
            except Exception as e:
                ret['status'] = { 
                    'status_type': False,
                    'status_message': 'Error while creating table: '+str(e.args)
                }
            # create table system id pointer
            if tableCreated == True:
                idFile = databaseStorage+commandJsonObj['databaseName']+pathEndsWith+commandJsonObj['tableName']+pathEndsWith+'_ldb'+pathEndsWith+'id'
                try:
                    with open( idFile, 'a+' ) as tsid:
                        print( '0', file=tsid )
                except Exception as e:
                    ret['status'] = { 
                        'status_type': False,
                        'status_message': 'Error on creating the system id.' 
                    }
        else:
            ret['status'] = { 
                'status_type': False,
                'status_message': 'Error while creating table: Table already exists' 
            }
    else:
        ret['status'] = { 
            'status_type': False,
            'status_message': 'Error while creating table: '+str( missedItems )+' values are missing' 
        }
    return ret
        


def deleteTable( commandJsonObj, databaseStorage ):
    ret = {}
    tableAbsolutePath =  databaseStorage+commandJsonObj['databaseName']+pathEndsWith+commandJsonObj['tableName']
    try:
        shutil.rmtree( tableAbsolutePath )
        ret['status'] = [
            { 'status_type': True },
            { 'status_message': 'Database '+commandJsonObj['tableName']+' deleted successfully' }
        ]
    except Exception as e:
        ret['status'] = [
            { 'status_type': False },
            { 'status_message': 'Error: '+str(e.args) }
        ]
    return ret

def renameTable( commandJsonObj, databaseStorage ):
    ret = {}
    try:
        os.rename( databaseStorage+commandJsonObj['databaseName']+pathEndsWith+commandJsonObj['tableName'], 
                  databaseStorage+commandJsonObj['databaseName']+pathEndsWith+commandJsonObj['newTableName'] )
        ret['status'] = [
            { 'status_type': True },
            { 'status_message': 'Database '+commandJsonObj['tableName']+' renamed to '+commandJsonObj['newTableName']+' successfully' }
        ]
    except Exception as e:
        ret['status'] = [
            { 'status_type': False },
            { 'status_message': 'Error: '+str(e.args) }
        ]
    return ret