import re, json
# def addslashes(s):
#     s = s.replace( "\n", "\\n" )
#     s = s.replace( "\r\n", "\\n" )
#     d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
#     s = ''.join(d.get(c, c) for c in s)
#     return " ".join( s.split() )
# def stripslashes(s):
#     r = re.sub(r"\\(n|r)", "\n", s)
#     r = re.sub(r"\\", "", r)
#     return r

s = """{ "action": "DELETE_TABLE", "databaseName": "prijm_news", "tableName": "login \ antorher logs"}"""
s = s.replace("\\", "\\\\")
print(s)
# x = json.loads(s.replace('\r\n', '\\r\\n').replace('\n', '\\n'))
x = json.loads(s)

print( x )


# ns = addslashes(s)
# print( ns )

# print('-----------')

# print( stripslashes(ns) )

# print( " ".join( s.split() ) )
# print( r''+s )

# print( stripslashes(s) )

# print( s.encode('string_escape') )