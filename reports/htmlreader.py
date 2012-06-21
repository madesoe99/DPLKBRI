def addPrefAndSufStr(inFName,outFName,prefStr,sufStr):
# menambahkan string prefStr di awal dan sufStr di akhir pada setiap baris	
	inOFile = open(inFName,'r')

	sumStr = ''
	str = inOFile.read(1)
	while (str <> ''):
		lineStr = ''
		while (str <> '') and (str <> '\n'):
			lineStr = lineStr + str
			str = inOFile.read(1)
		sumStr = sumStr + prefStr + lineStr + sufStr + '\n'
		str = inOFile.read(1)

	inOFile.close()

	if outFName <> '':
		outOFile = open(outFName, 'w')
		outOFile.write(sumStr)
		outOFile.close()
	
	return sumStr

def makeOneLiner(inFName,outFName,prefStr,sufStr):
# membuat teks yang terdapat di file inFName menjadi satu baris
	inOFile = open(inFName,'r')

	sumStr = ''
	str = inOFile.read(1)
	while (str <> ''):
		if str <> '\n':
			sumStr = sumStr + str
		str = inOFile.read(1)

	inOFile.close()
	
	if outFName <> '':
		outOFile = open(outFName, 'w')
		outOFile.write(sumStr)
		outOFile.close()
	
	return sumStr

def searchString(str,varTuple):
	return 0

def changeStr(stringLine,varTuple,valTuple):
# mengganti string di stringLine yang terdiri dari string2 di varTuple
# menjadi string2 di valTuple sesuai urutannya

	if len(varTuple) <> len(valTuple):
		raise 'Banyaknya nilai tidak sesuai dengan variabel.'
	
	lenStr = len(stringLine)
	count = 0
	while count < lenStr:
		stringLine[count]
		
	return sumStr


##from htmlreader import addPrefAndSufStr
##addPrefAndSufStr('C:\DAFApp//<appfolder>//reports//<template file name.htm>','C:\DAFApp//<appfolder>//reports//<template file name.htm.py>','  oFile.write(\'','\\n\')')
