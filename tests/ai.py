with open( 'id', 'r+' ) as docID:
    currentID = docID.read()
    docID.seek(0)
    docID.write( str( int(currentID)+1 ) )
    docID.close()
print (currentID)