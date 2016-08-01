import json
from sys import platform as _platform

def pathEndWith():
    if( _platform == 'win32' ):
        pathEndsWith = "\\"
    else:
        pathEndsWith = "/"
    return pathEndsWith

def readJson(filePath):
    try:
        with open( filePath ) as confRawData:
            configData = json.load( confRawData )
            # validate path settings
            pathEndWithString = pathEndWith()
            if( not configData['storage_path'].endswith( pathEndWithString ) ):
                configData['storage_path'] += pathEndWithString
            return configData
    except Exception as e:
        return False

def writeJson( jsonData, filePath ):
    try:
        with open( filePath, 'w' ) as outFile:
            json.dump( jsonData, outFile )
            return True
    except Exception as e:
        return False

"""
    This method would read the leandb_starter_conf.json file
    return a json dumps of all informations it found.
"""
def starterConf():
    return readJson( 'conf/leandb_starter_conf.json' )
"""
    Remove all whitespaces/multiple whitespaces from a string
"""
def stripWhiteSpaces(stringValue):
    return " ".join( stringValue.split() )
"""
    Prepare string for as a index value
"""

def safeEscapedString( s ):
    s = s.replace( "\\", "\\\\" )
    s = s.replace( "\r\n", "\\n" )
    s = s.replace( "\n", "\\n" )
    s = s.replace( "\a", "\\a" )
    s = s.replace( "\b", "\\b" )
    s = s.replace( "\f", "\\f" )
    s = s.replace( "\n", "\\n" )
    s = s.replace( "\r", "\\r" )
    s = s.replace( "\t", "\\t" )
    s = s.replace( "\v", "\\v" )
    s = s.replace( "\\", "\\\\" )
    s = s.replace( "'", "\'" )
    s = s.replace( "\a", "\\a" )
    s = s.replace( '"', '\"' )
    return s

def encodeIndexString( stringValue ):
    s = " ".join( stringValue.split() )
    return safeEscapedString( s )