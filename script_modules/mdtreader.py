import string

EOF = ''
closType = '}'
typename = 'typename='
membername = 'membername='

def OpenMDTFile(filename):
    return open(filename, 'r')

def OpenResultFile(filename):
    return open(filename, 'w')

def LastChar(str):
    return str[len(str)-1]

def GetClassName(str):
    strClass = string.replace(str, typename, '')
    return string.replace(str, '\'', '')

def GetMemberName(str):
    strClass = string.replace(str, membername, '')
    return string.replace(str, '\'', '')

def WriteHeader(resultOFile, strClassName):
    resultOFile.write('select from %s\n' % (strClassName))
    resultOFile.write('(\n')

def WriteMember(resultOFile, strMemberName):
    resultOFile.write('  %s,\n' % (strMemberName))

def ProcessFile(mdtOFile, resultOFile):
    global EOF, typename

    while LastChar(str) != EOF:
        str = string.lower(string.strip(mdtOFile.readline()))
        if string.find(str,typename):
            WriteHeader(resultOFile, GetClassName(str))
            while LastChar(str) != closType:
                if string.find(str,membername):
                    WriteMember(resultOFile, GetMemberName(str))
