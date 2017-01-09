import os, re, shutil
from leandbHelper   import *
from leandbTable    import createTable
from leandbDocument import fetchData
from leandbDocument import multiIndexDigger
from leandbDocument import diggIndex

def deleteData( commandJsonObj, databaseStorage ):
    pathEnding        = pathEndWith()
    tableAbsolutePath =  databaseStorage+commandJsonObj['databaseName']+pathEnding+commandJsonObj['tableName']
    tableConfigFile   = tableAbsolutePath+pathEnding+'_ldb'+pathEnding
    tableSystemID     = tableConfigFile+'id'
    ret               = {}
    # Fetch all docs matching provided conditions
    fetchedData = fetchData( commandJsonObj, databaseStorage )

    if fetchedData['status_type'] == True:
        if fetchedData['data'] != []:
            for item in fetchedData['data']:
                # Find all the indexes that need to be deleted
                # find all indexes
                indexes = os.listdir(tableConfigFile+'_index'+pathEnding)
                for singleIndex in indexes:
                    # Check if we have an index file for the updateable
                    # find the index key name
                    indexPath = databaseStorage+commandJsonObj['databaseName']+pathEnding+commandJsonObj['tableName']+pathEnding+'_ldb'+pathEnding+'_index'+pathEnding+singleIndex
                    # Check if the index file is exists
                    if os.path.isfile(indexPath):
                        f = open(indexPath,"r+")
                        d = f.readlines()
                        f.seek(0)
                        for i in d:
                            rgxp = re.compile( '(".*?").*?(".*?")', re.IGNORECASE|re.DOTALL )
                            rgxp = rgxp.search( i )
                            if rgxp:
                                docID = dequote( rgxp.group(1) ).strip()
                                if docID.strip() != item['_id'].strip():
                                    f.write(i)
                        f.truncate()
                        f.close()



                try:
                    # delete the document
                    os.remove(tableAbsolutePath+pathEnding+item['_id']+'.ldb')
                except Exception as e:
                    return {
                        'status_type': False,
                        'status_message': 'Error occured while deleting documents. ' + str(e.args)
                    }
        else:
            ret = {
                'status_type': False,
                'status_message': 'No document was found to delete! Make sure all conditions are indexed.'
            }
            if 'missing_indexes' in fetchedData:
                ret['missing_indexes'] = fetchedData['missing_indexes']
            return ret
    else:
        fetchedData['status_message'] = 'Unable to delete documents.'
        return fetchedData
    fetchedData['status_message'] = 'Data and document deleted successfully'
    return fetchedData