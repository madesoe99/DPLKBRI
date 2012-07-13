# text utilities
def Pad(kode, text, length):
  from string import ljust, rjust, center

  if kode==0:
    retval = ljust(text, length)
  elif kode==1:
    retval = center(text, length)
  elif kode==2:
    retval = rjust(text, length)
  return retval

def space(f, digit):
  i = 0
  while i<digit:
    f.WriteText(' ')
    i = i+1

def symbol(f, karakter, digit):
  i = 0
  while i<digit:
    f.WriteText(karakter)
    i = i+1

def formatfloat(fl):
  from fpformat import fix
  strfl = fix(fl,2)
  length = len(strfl)
  retval = ''
  j = 0
  for i in range(length-1, -1, -1):
    j = j+1
    if ((j%3)==0) and (j != 3) and (j != 0) and (j != length):
      retval = ','+strfl[i]+retval
    else:
      retval = strfl[i]+retval
  return retval
  
def floattocur(X):
  from fpformat import fix
  PB = 1000.0
  str = fix(X % PB, 2)
  if X / PB >= 1:
    while 1:
      PB = PB * 1000.0
      IX = int((X % PB) / (PB / 1000))
      str = fix(IX, 0) + ',' + str
      if X / PB < 1:
        break

  return str



# Class to access TextFile
class TextFileClass:
  #property
  FTextFile = None
  FActive = 0
  FUNIXStyle = 0
  FPageMode = 1
  FPageHeight = 0
  FTopMargin = 0
  FBottomMargin = 0
  FCurrentLine = 0
  
  # Actual functions
  def BeginWrite(self, AFileName):
    if self.FActive == 1:
      raise Exception, ValueError +  'Textutils: file already opened'
    self.FTextFile = open(AFileName, 'w')
    self.FUNIXStyle = 0
    self.FPageMode = 0
    self.FActive = 1

  def StopWrite(self):
    if self.FActive==1:
      self.FTextFile.close()
      self.FActive = 0

  def SetDOSMode(self):
    self.FUNIXStyle = 0

  def SetUNIXMode(self):
    self.FUNIXStyle = 1
    
  def SetPageMode(self, PageHeight, TopMargin, BottomMargin):
    self.FPageMode = 1
    self.FPageHeight = PageHeight
    self.FTopMargin = TopMargin
    self.FBottomMargin = BottomMargin
    self.FCurrentLine = self.FTopMargin + 1
    for i in range(1, self.FTopMargin+1):
      self.WriteEOL()

  def ClearPageMode(self):
    self.FPageMode = 0

  def WriteText(self, AText):
    self.FTextFile.write(AText)

  def Writeline(self):
    self.WriteEOL()
    if self.FPageMode==1:
      self.FCurrentLine = self.FCurrentLine + 1
      if self.FCurrentLine > (self.FPageHeight - self.FBottomMargin):
        for i in range(1, self.FBottomMargin+1):
          self.WriteEOL()
        for i in range(1, self.FTopMargin+1):
          self.WriteEOL()
        self.FCurrentLine = self.FTopMargin + 1


  def FillUntilEndOfPage(self):
    if self.FPageMode==0:
      raise Exception, ValueError +  'TextUtils : Not in page mode'
    for i in range(1, (self.FPageHeight - self.FCurrentLine + 2)):
      self.WriteEOL()
    for i in range(1, self.FTopMargin+1):
      self.WriteEOL()
    self.FCurrentLine = self.FTopMargin + 1

  def WriteEOL(self):
    if self.FUNIXStyle==1:
      self.FTextFile.write('#10')
    else:
      self.FTextFile.write('\n')
