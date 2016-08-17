"""
    Handle the database directory
    -> Create if not found the selected database
    -> Delete Database
    -> Rename Database
"""
from leandbHelper import *
import os
import shutil

# fetch and assign leandb configuration data
# configData = starterConf()

def createDatabase( databaseName, databaseStorage ):
    ret = {}
    databaseAbsolutePath =  databaseStorage+databaseName
    # check if the database exists or not
    if( not os.path.isdir( databaseAbsolutePath ) ):
        try:
            os.makedirs( databaseAbsolutePath )
            ret['status'] = {
                'status_type': True,
                'status_message': 'Database '+databaseName+' created successfully'
            }
        except Exception as e:
            ret['status'] = { 
                'status_type': False,
                'status_message': 'Error: '+str(e.args) 
            }
    else:
        ret['status'] = [
            { 'status_type': True },
            { 'status_message': 'Database already created' }
        ]

    return ret

def deleteDatabase( databaseName, databaseStorage ):
    ret = {}
    try:
        shutil.rmtree( databaseStorage+databaseName )
        ret['status'] = [
            { 'status_type': True },
            { 'status_message': 'Database '+databaseName+' deleted successfully' }
        ]
    except Exception as e:
        ret['status'] = [
            { 'status_type': False },
            { 'status_message': 'Error: '+str(e.args) }
        ]
    return ret

def renameDatabase( oldDatabaseName, newDatabaseName, databaseStorage ):
    ret = {}
    try:
        os.rename( databaseStorage+oldDatabaseName, databaseStorage+newDatabaseName )
        ret['status'] = [
            { 'status_type': True },
            { 'status_message': 'Database '+oldDatabaseName+' renamed to '+newDatabaseName+' successfully' }
        ]
    except Exception as e:
        ret['status'] = [
            { 'status_type': False },
            { 'status_message': 'Error: '+str(e.args) }
        ]
    return ret