import re
def dequote( s ):
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

def diggIndex( database, table, index, databaseStorage, matchAgainst, comparisonType, pathEnding ):
    indexPath = databaseStorage+database+pathEnding+table+pathEnding+'_ldb'+pathEnding+'_index'+pathEnding+index
    # read each line
    documentCollections = [] 
    with open( indexPath ) as indexData:
        for item in indexData:
            # using regular expression to prepare index data columns
            rgxp = re.compile( '(".*?").*?(".*?")', re.IGNORECASE|re.DOTALL )
            rgxp = rgxp.search( item )
            if rgxp:
                docID = dequote( rgxp.group(1) ).strip()
                columnData = dequote( rgxp.group(2) ).strip()
                # equal comparison
                if comparisonType == 'eq':
                    if columnData in matchAgainst:
                        documentCollections.append( docID )
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
                            documentCollections.append( item )
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

print( diggIndex( 'goldposts', 'posts', 'category', 'F:\\leandata\\', [ 'Politics', 'World News' ], 'neq', '\\' ) )