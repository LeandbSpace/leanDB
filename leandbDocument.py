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
import os, re
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
                ret['status'] = {
                    'status_type': True,
                    'status_message': 'Table '+commandJsonObj['tableName']+' created successfully'
                }
            except Exception as e:
                ret['status'] = {
                    'status_type': False,
                    'status_message': 'Error while creating table: '+str(e.args)
                }
                # exit because there was trouble while creating the database and table directories
                return ret
        # descide the document id
        try:
            with open( tableSystemID, 'r+' ) as docID:
                currentID = docID.read()
                docID.seek(0)
                documentID = str(int(currentID)+1)
                docID.write( documentID )
                docID.close()
        except Exception as e:
            ret['status'] = {
                'status_type': False,
                'status_message': 'Error while writing document id. ' + str(e.args)
            }
            # exit because there was trouble
            return ret
        # create the data file
        # add the system document id with the json file
        commandJsonObj['data']['_id'] = documentID
        try:
            writeJson( commandJsonObj['data'], tableAbsolutePath+pathEnding+documentID+'.ldb' )
        except Exception as e:
            ret['status'] = {
                'status_type': False,
                'status_message': 'Error while writing document: '+str(e.args)
            }
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
                    ret['status'] = {
                        'status_type': True,
                        'status_message': 'Error while writing index for "'+indexItem+'": '+str(e.args)
                    }
        ret['id'] = documentID
        ret['status'] = {
            'status_type': True,
            'status_message': 'New data inserted successfully.'
        }
    else:
        ret['status'] = {
            'status_type': False,
            'status_message': 'Error while inserting data: '+str( missedItems )+' values are missing'
        }
    return ret

def fetchData( commandJsonObj, databaseStorage ):
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

    if( missing == False ):
        # validate if table and database are exists
        resultSet = {}
        # read id index
        iterationCounts = 0
        _rawDocIdLists = []
        thisResultSet = []        
        # Fetch all documents according to the where conditions
        if 'where' in commandJsonObj:
            if commandJsonObj['where'] != '':
                # Pass the where arguments in the diggIndex() function with necessary informations via param
                thisDataPacket = multiIndexDigger( commandJsonObj['databaseName'], commandJsonObj['tableName'], 
                    databaseStorage, commandJsonObj['where'], pathEnding )
                if thisDataPacket['status_type'] == True:
                    _rawDocIdLists += thisDataPacket['documents']
        else:
            # No where condition was given, go through the system doc id lists
            with open( tableAbsolutePath+pathEnding+'_ldb'+pathEnding+'_index'+pathEnding+'pid' ) as _id:
                for item in _id:
                    _rawDocIdLists.append( item )
        # Remove duplicate doc ID's
        _rawDocIdLists = list( set( _rawDocIdLists ) )
        # Fetch all the doc using their id, decode the json
        for item in _rawDocIdLists:
            try:
                thisDocData = readJson( str(tableAbsolutePath+pathEnding+item+'.ldb').replace('\n', '') )
                # Validate columns query and descide what columns to send
                # If no columns was set then it will send all the available columns
                if 'columns' in commandJsonObj:
                    if isinstance( commandJsonObj['columns'], list ):
                        # We have some columns to choose
                        refinedThisDocData = {}
                        for colitm in commandJsonObj['columns']:
                            # Check if this specific columns is exists in the document
                            if colitm in thisDocData:
                                refinedThisDocData[colitm] = thisDocData[colitm]
                            else:
                                # Given column was not found, so assign null as the value
                                refinedThisDocData[colitm] = None
                        # Push system doc _id
                        if '_id' not in commandJsonObj['columns']:
                            refinedThisDocData['_id'] = thisDocData['_id']
                        thisDocData = refinedThisDocData 
                thisResultSet.append( thisDocData )
                iterationCounts = iterationCounts + 1
            except:
                continue
        resultSet['data'] = thisResultSet
        resultSet['iterations'] = iterationCounts
        resultSet['status_type'] = True
        resultSet['status_message'] = 'Data fetched successfully'

        # Implement sort operations among all the data fetched above
        if 'sort' in commandJsonObj:
            # sort is in command object
            if isinstance( commandJsonObj['sort'], dict ):
                # sort is a dict
                for indexToOrder in commandJsonObj['sort'].keys():
                    reverseOrder = None
                    if str(commandJsonObj['sort'][indexToOrder]).lower() == 'asc':
                        # ascending order the index
                        reverseOrder = False
                    elif str(commandJsonObj['sort'][indexToOrder]).lower() == 'desc':
                        # descending order the index
                        reverseOrder = True
                    if reverseOrder != None:
                        # reverse order is valide in asc or desc
                        try:
                            # trying to sort the data
                            resultSet['data'] = sorted( resultSet['data'], key=lambda k:k[indexToOrder], reverse = reverseOrder )
                        except:
                            continue
        # Limit number of data item to return
        # set default value for limit if any limits are not provided
        if 'limit' in commandJsonObj:

            if 'skip' in commandJsonObj['limit']:
                skip = int( commandJsonObj['limit']['skip'] )
                resultSetLength = len( resultSet['data'] )
                if skip > 0:
                    for skipAble in range( 0, skip ):
                        del resultSet['data'][skipAble]

            if 'count' in commandJsonObj['limit']:
                count = int( commandJsonObj['limit']['count'] )
                if count > 0:
                    resultSetLength = len( resultSet['data'] )
                    if resultSetLength > count:
                        itr = 0
                        tmpData = []
                        while( itr < resultSetLength ):
                            if itr < count:
                                tmpData.append(resultSet['data'][itr])
                            itr += 1
                        resultSet['data'] = tmpData
        resultSet['data_set_count'] = len( resultSet['data'] )
        return resultSet
    else:
        ret['status'] = {
            'status_type': False,
            'status_message': 'Error while inserting data: '+str( missedItems )+' values are missing'
        }
    return ret

def multiIndexDigger( database, table, storage, command, pathend ):
    """
        The digger function will
            - Read all where conditions
            - Will check if condition is a list or dict
                - If it is a dict then it will get its key, which is the index name for the condition
                - Pass that index name to the diggIndex function, along with necessary informations
                  OR
                - If it is a list, then we run a for loop, then for each dict we will follow the above steps.
    """
    documentCollections = []
    try:
        # find all comparison types eg. 'gt', 'eq', 'lt' etc..
        indexes = command.keys()
        # Start working with all the comparison operations
        for comparisonType in indexes:
            # If the current index is a list, then we would run a loop
            # or if the current index is a dict, then we would simply start working with its indexes
            thisComparisonCommand = command[comparisonType]
            if isinstance( thisComparisonCommand, list ):
                # Comparison Command is a list
                # This command should include multiple condition of same comparison type
                for cmdItem in thisComparisonCommand:
                    # Type of cmdItem should be dict
                    for indexName in cmdItem.keys():
                        # Grab all the doc id that meets the conditions
                        documentCollections += diggIndex( database, table, indexName, storage, cmdItem[indexName], comparisonType, pathend )
            elif isinstance( thisComparisonCommand, dict ):
                # Comparison command is a dict
                # This command should include only one condition
                for indexName in thisComparisonCommand.keys():
                    # Grab all the doc id that meets the conditions
                    documentCollections += diggIndex( database, table, indexName, storage, thisComparisonCommand[indexName], comparisonType, pathend )
    except expression as e:
        return {
            'status_type': False,
            'status_message': 'Error in "where" conditions: '+str(e.args)
        }
    # Document id should be collected
    return {
        'status_type': True,
        'status_message': 'All document ID fetched',
        'documents': documentCollections
    }

def diggIndex( database, table, index, databaseStorage, matchAgainst, comparisonType, pathEnding ):
    # find the index key name
    indexPath = databaseStorage+database+pathEnding+table+pathEnding+'_ldb'+pathEnding+'_index'+pathEnding+index
    # read each line
    documentCollections = []
    with open( indexPath ) as indexData:
        # Index Data
        for item in indexData:
            # Item in index data
            # using regular expression to prepare index data columns
            rgxp = re.compile( '(".*?").*?(".*?")', re.IGNORECASE|re.DOTALL )
            rgxp = rgxp.search( item )
            if rgxp:
                docID = dequote( rgxp.group(1) ).strip()
                columnData = dequote( rgxp.group(2) ).strip()
                # equal comparison
                if comparisonType == 'eq':
                    if columnData == matchAgainst:
                        # Expected column found
                        # Document Collections
                        documentCollections.append( docID )
                # greater than comparison
                elif comparisonType == 'gt' :
                    for thisVal in matchAgainst:
                        try:
                            if matchAgainst > int(columnData):
                                documentCollections.append( docID )
                        except:
                            pass
                # less than comparison
                elif comparisonType == 'lt' :
                    for thisVal in matchAgainst:
                        try:
                            if matchAgainst < int(columnData):
                                documentCollections.append( docID )
                        except:
                            pass
                # between comparison
                elif comparisonType == 'bt' :
                    for rangeList in matchAgainst:
                        try:
                            if rangeList[0] <= int(columnData) <= rangeList[1]:
                                documentCollections.append( docID )
                        except:
                            pass
                # not equal comparison
                elif comparisonType == 'neq' :
                    try:
                        if columnData not in matchAgainst:
                            documentCollections.append( docID )
                    except Exception as e:
                        continue
                # greater or equal comparison
                elif comparisonType == 'geq' :
                    for thisVal in matchAgainst:
                        try:
                            if matchAgainst >= int(columnData):
                                documentCollections.append( docID )
                        except Exception as e:
                            continue
                # less or equal comparison
                elif comparisonType == 'leq' :
                    for thisVal in matchAgainst:
                        try:
                            if matchAgainst <= int(columnData):
                                documentCollections.append( docID )
                        except Exception as e:
                            continue
            else:
                return None
    
    return documentCollections
