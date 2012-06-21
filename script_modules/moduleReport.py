import string

def penggal(kalimat, max):
    s = string.splitfields(kalimat,'\n')
    #t = ""
    r = []
    for k in s:
      t = ""
      s1 = string.splitfields(k)
      for i in s1:
        if len(string.strip(t + " " + i)) > max:
          r.append(t)
          t = ""
        t = string.strip(t+" "+i)
      r.append(t)
    return r


def terbilang(b):
  def ParsingTiga(b):    
    if b == 0:
      return "nol"
    bs = str(b)
    pjg = len(bs)
    kalimat = []
    for i in range(pjg):
      c = int(bs[pjg-i-1])
      if c == 0:
        s = ""
      else:
        s = angka[c]
        if i == 1:
          if c == 1:
            sebelum = bs[pjg-1]
            if sebelum == "0":
              s = "sepuluh"
            else:
              j = len(kalimat)
              if sebelum == "1":
                s = "sebelas"
              else:
                s = kalimat[j-2] + "belas"
              kalimat[j-2] = ""
          else:
            s = s + "puluh"
        elif i == 2:
          if c == 1:
            s = "seratus"
          else:
            s = s + "ratus"

      kalimat.append(s)
    kalimat.reverse()
    s = ""
    for i in kalimat:
      s = string.strip(s + " " + i)
    return s
  
  blok = ['','ribu','juta','milyar','trilyun','bilyun']
  angka = ['','satu','dua','tiga','empat','lima','enam','tujuh','delapan','sembilan']
  bs = str(b)
  pjg = len(bs)
  JmlBlok = pjg / 3
  if pjg % 3 > 0:
    JmlBlok = JmlBlok + 1
  k = []
  for i in range(JmlBlok):
    c = int(bs[-3:])
    if i == 1 and c == 1:
      s = "seribu"
    elif c == 0 and JmlBlok > 1:
      s = ""
    else:
      s = ParsingTiga(c) + " " + blok[i]
    k.append(string.strip(s))
    bs = bs[:-3]
  k.reverse()
  s = ""
  for i in k:
    s = string.strip(s + " " + i)
  return s
