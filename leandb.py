from leandbHelper import *
from leandbDatabase import *
from leandbTable import *
from leandbDocument import *
from leandbUpdate import *
from leandbDelete import *
from bottle import route, run, post, request
import json

# fetch and assign leandb configuration data
configData = starterConf()

# default controller for the ip
@route( '/', method='GET')
def index():
    return '{ "status" : 1 }'

# method to handle a database
# db = database
@route( '/query', method = 'POST' )
def query():
    try:
        command = json.loads(request.forms.get('cmd'))
    except Exception as e:
        return "[ { 'status_type': False }, { 'status_message': 'Error Fucked up: '"+str(e.args)+" } ]"
    # Translate the query json file and map them to action
    if( command['action'] == 'CREATE_DATABASE' ):
        return createDatabase( command['databaseName'], configData['storage_path'] )
    elif( command['action'] == 'DELETE_DATABASE' ):
        return deleteDatabase( command['databaseName'], configData['storage_path'] )
    elif( command['action'] == 'RENAME_DATABASE' ):
        return renameDatabase( command['databaseName'], command['newDatabaseName'], configData['storage_path'] )
    elif( command['action'] == 'CREATE_TABLE' ):
        return createTable( command, configData['storage_path'] )
    elif( command['action'] == 'RENAME_TABLE' ):
        return renameTable( command, configData['storage_path'] )
    elif( command['action'] == 'DELETE_TABLE' ):
        return deleteTable( command, configData['storage_path'] )
    elif( command['action'] == 'INSERT_DATA' ):
        return insertData( command, configData['storage_path'] )
    elif( command['action'] == 'FETCH_DATA' ):
        return fetchData( command, configData['storage_path'] )
    elif( command['action'] == 'UPDATE_DATA' ):
        return updateData( command, configData['storage_path'] )
    elif( command['action'] == 'DELETE_DATA' ):
        return deleteData( command, configData['storage_path'] )

# run the server, get server informations from leandb conf file
run(
    host = configData['serv_ip'],
    port = configData['serv_port'],
    debug = configData['debug'] 
)
