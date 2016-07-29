import re
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

s = """efvrwev
sdc
sdc sdvd   "  sd"vsd sdvsdvsdv
sdcsd
c \n\n ascascasc"""

# ns = addslashes(s)
# print( ns )

# print('-----------')

# print( stripslashes(ns) )

print( " ".join( s.split() ) )

# print( stripslashes(s) )

# print( s.encode('string_escape') )