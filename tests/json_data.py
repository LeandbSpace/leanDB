import json
rawJson = """{
    "action": "INSERT_DATA",
    "databaseName": "prijm_news",
    "tableName": "news",
    "data": {
        "title": "A test news",
        "author": "Hasan",
        "moderators": [
            { "name": "Shoy" },
            { "name": "Mays" },
            { "name": "Homy" }
        ],
        "news": "The day was so cute, i was waiting for a .."
    },
    "_index": "title, author"
}"""

jsn = json.loads(rawJson)

# print (jsn['_action'])
if 'action' in jsn:
    print('found')
else:
    print('not fund')



print( jsn['data']['moderators'][1]['name'] )