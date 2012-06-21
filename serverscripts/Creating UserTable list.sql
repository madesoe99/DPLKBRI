select s.name
from sysobjects s
where s.type = 'U' AND
      s.name <> 'dtproperties'
order by s.name;