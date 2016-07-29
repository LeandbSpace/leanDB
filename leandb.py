from leandbHelper import *
from leandbDatabase import *
from leandbTable import *
from leandbDocument import *
from bottle import route, run, post, request
import json

# fetch and assign leandb configuration data
configData = starterConf()

# method to handle a database
# db = database
@route( '/query', method = 'POST' )
def query():
    """
        To create a new database: { "action": "CREATE_DATABASE", "databaseName": "prijm_discussions" }
        Delete a database: { "action": "DELETE_DATABASE", "databaseName": "prijm_discussions" }
        Rename a database: { "action": "RENAME_DATABASE", "databaseName": "prijm_discussions", "newDatabaseName": "prijm_main" }
        Create a new table: { "action": "CREATE_TABLE", "databaseName": "prijm_news", "tableName": "news" }
        Rename a table: { "action": "RENAME_TABLE", "databaseName": "prijm_news", "tableName": "logs", "newTableName": "login_logs"}
        Delete a table: { "action": "DELETE_TABLE", "databaseName": "prijm_news", "tableName": "login_logs"}
        Insert data: 
            { "action": "INSERT_DATA", "databaseName": "prijm_news", "tableName": "news", "data": {
                    "title": "Are you lost yeay",
                    "author": "Hasan",
                    "moderators": [
                        { "name": "Shoy" },
                        { "name": "Mays" },
                        { "name": "Homy" }
                    ],
                    "news": "The day was so cute, i was waiting for a ..",
                    "post_status": "1",
                    "comments": "enabled"
                },
                "_index": "title, author, post_status, comments"
            }
        Fetch Data:
            { 
                "action": "FETCH_DATA", "databaseName": "prijm_news", "tableName": "news", 
                "conditions": {
                    "limit": {
                        "count": "10",
                        "skip": "0"
                    },
                    "where": [
                        { "id": "20" },
                        { "userid": "2" }
                    ]
                }
            }
    """
    try:
        command = json.loads(request.forms.get('cmd'))
    except Exception as e:
        return "[ { 'status_type': False }, { 'status_message': 'Error: '"+str(e.args)+" } ]"
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

# run the server, get server informations from leandb conf file
run(
    host = configData['serv_ip'],
    port = configData['serv_port'],
    debug = configData['debug'] 
)
