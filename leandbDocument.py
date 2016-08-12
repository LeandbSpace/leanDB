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
                # docID.truncate()
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
        # set default value for limit if any limits are not provided
        if 'limit' in commandJsonObj:
            count = int( commandJsonObj['limit']['count'] )
            skip = int( commandJsonObj['limit']['skip'] )
        else:
            count = 100
            skip = 0
        # set default value for columns if not given
        if 'columns' not in commandJsonObj:
            commandJsonObj['columns'] = '*'
        # read id index
        iterationCounts = 0
        _rawDocIdLists = []
        thisResultSet = []
        """
            If the query have "where" conditions then using the diggIndex() function this will
                fetch all documents ID (ID represents the file name of each doc).
            If there was no where conditions then skip this part and
                go through the default table pid list.
        """
        if 'where' in commandJsonObj:
            if commandJsonObj['where'] != '':
                # Pass the where arguments in the diggIndex() function with necessary informations via param
                thisDataPacket = multiIndexDigger( commandJsonObj['databaseName'], commandJsonObj['tableName'], 
                    databaseStorage, commandJsonObj['where'], pathEnding )
                if thisDataPacket['status_type'] == True:
                    _rawDocIdLists += thisDataPacket['documents']
        # Remove duplicate doc ID's

        # Fetch all the doc using their id, decode the json
        # If the doc file didnt exists then skip that

        # Implement sort operations among all the data fetched above

        # Limit number of data item to return

        # Strip columns/index items according to the query
        # If there is no columns specified then return all avialable elements

        # with open( tableAbsolutePath+pathEnding+'_ldb'+pathEnding+'_index'+pathEnding+'pid' ) as _id:
        #     for item in _id:
        #         thisResultSet.append(readJson( str(tableAbsolutePath+pathEnding+item+'.ldb').replace('\n', '') ))
        #         iterationCounts = iterationCounts + 1
        # resultSet['items'] = thisResultSet
        # resultSet['iterations'] = iterationCounts
        # return resultSet
        return str(_rawDocIdLists)
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
        # print("Indexes")
        # print(indexes)
        # Start working with all the comparison operations
        for comparisonType in indexes:
            # If the current index is a list, then we would run a loop
            # or if the current index is a dict, then we would simply start working with its indexes
            # print("Comparison Type")
            # print(comparisonType)
            thisComparisonCommand = command[comparisonType]
            # print("This Comparison Command")
            # print(thisComparisonCommand)
            if isinstance( thisComparisonCommand, list ):
                # print("Comparison Command is a list")
                # This command should include multiple condition of same comparison type
                for cmdItem in thisComparisonCommand:
                    # Type of cmdItem should be dict
                    for indexName in cmdItem.keys():
                        # Grab all the doc id that meets the conditions
                        documentCollections += diggIndex( database, table, indexName, storage, cmdItem[indexName], comparisonType, pathend )
            elif isinstance( thisComparisonCommand, dict ):
                # print("Comparison command is a dict")
                # This command should include only one condition
                for indexName in thisComparisonCommand.keys():
                    # print("Index Name")
                    # print(indexName)
                    # print("diggIndex( "+database+", "+table+", "+indexName+", "+storage+", "+thisComparisonCommand[indexName]+", "+comparisonType+", "+pathend+" )")
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
    # print("Index Path")
    # print(indexPath)
    # read each line
    documentCollections = []
    with open( indexPath ) as indexData:
        # print("Index Data")
        # print(indexData)
        for item in indexData:
            # print("Item in index data")
            # print(item)
            # using regular expression to prepare index data columns
            rgxp = re.compile( '(".*?").*?(".*?")', re.IGNORECASE|re.DOTALL )
            rgxp = rgxp.search( item )
            if rgxp:
                docID = dequote( rgxp.group(1) ).strip()
                columnData = dequote( rgxp.group(2) ).strip()
                # print("DOC ID")
                # print(docID)
                # print("Column Data")
                # print(columnData)
                # equal comparison
                if comparisonType == 'eq':
                    # print("In Equal check")
                    if columnData == matchAgainst:
                        # print("-------> Expected column found")
                        documentCollections.append( docID )
                        # print("Document Collections")
                        # print(documentCollections)
                # greater than comparison
                elif comparisonType == 'gt' :
                    for thisVal in matchAgainst:
                        try:
                            if matchAgainst > int(columnData):
                                documentCollections.append( docID )
                        except Exception as e:
                            continue
                # less than comparison
                elif comparisonType == 'lt' :
                    for thisVal in matchAgainst:
                        try:
                            if matchAgainst < int(columnData):
                                documentCollections.append( docID )
                        except Exception as e:
                            continue
                # between comparison
                elif comparisonType == 'bt' :
                    for rangeList in matchAgainst:
                        try:
                            if rangeList[0] <= int(columnData) <= rangeList[1]:
                                documentCollections.append( docID )
                        except Exception as e:
                            continue
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
