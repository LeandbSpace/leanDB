from leandbHelper import *
from leandbTable import createTable
from leandbDocument import fetchData
from leandbDocument import multiIndexDigger
from leandbDocument import diggIndex
import os, re
import shutil

def updateData( commandJsonObj, databaseStorage ):

    pathEnding = pathEndWith()

    tableAbsolutePath =  databaseStorage+commandJsonObj['databaseName']+pathEnding+commandJsonObj['tableName']
    tableConfigFile = tableAbsolutePath+pathEnding+'_ldb'+pathEnding
    tableSystemID = tableConfigFile+'id'
    # print( tableAbsolutePath + "\n" + tableConfigFile + "\n" + tableSystemID )

    ret = {}
    if( not commandJsonObj['data'] or commandJsonObj['data'] == "" ):
        ret['status'] = {
            'status_type': False,
            'status_message': 'Error while updating data: No updatable data was provided'
        }
        return ret
    elif ( not isinstance( commandJsonObj['data'], dict ) ):
        # item must be a dict type
        ret['status'] = {
            'status_type': False,
            'status_message': 'Error while updating data: updatable data must be with valid key( data dictionary )'
        }
        return ret
    else:
        # Fetch all docs matching all conditions
        fetchedData = fetchData( commandJsonObj, databaseStorage )
        if fetchedData['status_type'] == True:
            if fetchedData['data'] != []:
                for item in fetchedData['data']:
                    # Lets update this document
                    # Find all the keys that need to be updated
                    for updateable in commandJsonObj['data'].keys():
                        # Check if we have an index file for the updateable
                        # find the index key name
                        indexPath = databaseStorage+commandJsonObj['databaseName']+pathEnding+commandJsonObj['tableName']+pathEnding+'_ldb'+pathEnding+'_index'+pathEnding+updateable
                        # Check if the index file is exists
                        if os.path.isfile(indexPath):
                            f = open(indexPath,"r+")
                            d = f.readlines()
                            f.seek(0)
                            for i in d:
                                if i.strip() == '"'+item['_id']+'" "'+item[updateable]+'"'.strip():
                                    i = '"'+item['_id']+'" "'+commandJsonObj['data'][updateable]+'"\n'
                                f.write(i)
                            f.truncate()
                            f.close()
                        item[updateable] = commandJsonObj['data'][updateable]
                    try:
                        writeJson( item, tableAbsolutePath+pathEnding+item['_id']+'.ldb' )
                    except Exception as e:
                        return {
                            'status_type': False,
                            'status_message': 'Error while update, ' + str(e.args)
                        }
            else:
                ret = {
                    'status_type': False,
                    'status_message': 'No document was found to update! Make sure all conditions are indexed.'
                }
                if 'missing_indexes' in fetchedData:
                    ret['missing_indexes'] = fetchedData['missing_indexes']
                return ret
        else:
            fetchedData['status_message'] = 'Unable to update documents.'
            return fetchedData
        fetchedData['status_message'] = 'Data updated successfully'
        return fetchedData