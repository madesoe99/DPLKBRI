import sys
import dafsys4
import com.ihsan.util.base88enc as b88enc
import random

# initialize user data

def main_function():
  cfg = dafsys4.openConfig("c:\\dafapp\\dplk\\default.cfg")
  cfg.BeginTransaction()
  try:
    createUserGroup(cfg)
    createBranch(cfg)
    pwd = createUser(cfg)
    cfg.Commit()
    print "Init user data success"
    print "root password: %s" % pwd
  except:
    cfg.Rollback()
    print "Error: %s" % str(sys.exc_info()[1])
  #--
#--

def createUserGroup(cfg):
  o = cfg.CreatePObject("UserGroup")
  o.group_id = "ADM"
  o.last_update = cfg.Now()
  o.description = "Administrator group"
  o.groupname = "Administrator"
  o.user_id = "root"
  
  o = cfg.CreatePObject("UserGroup")
  o.group_id = "OPR"
  o.last_update = cfg.Now()
  o.description = "Operator group"
  o.groupname = "Operator"
  o.user_id = "root"
  
  o = cfg.CreatePObject("UserGroup")
  o.group_id = "INV"
  o.last_update = cfg.Now()
  o.description = "Investment group"
  o.groupname = "Investment"
  o.user_id = "root"

  o = cfg.CreatePObject("UserGroup")
  o.group_id = "MAN"
  o.last_update = cfg.Now()
  o.description = "Management group"
  o.groupname = "Management group"
  o.user_id = "root"
#--

def createBranch(cfg):
  o = cfg.CreatePObject("BranchLocation")
  o.branch_code = "000"
  o.branchname = "Kantor pusat"
  o.branchstatus = "B"
  o.last_update = cfg.Now()
  o.user_id = "root"
#--
  
def createUser(cfg):
  o = cfg.CreatePObject("UserApp")
  o.user_id = "root"
  o.username = "root user"
  o.description = "administrator"
  o.mod_user_id = "root"
  o.user_id1 = "root"
  o.branch_code = "000"
  o.nolimitlocation = "T"
  o.last_update = cfg.Now()

  b88 = b88enc.base88()
  pwd = genPassword()
  o.encpassword = b88.convertFromString(pwd)
  
  o = cfg.CreatePObject("UserGroupApp")
  o.user_id = "root"
  o.group_id = "ADM"
  
  o = cfg.CreatePObject("UserGroupApp")
  o.user_id = "root"
  o.group_id = "OPR"
  
  return pwd
#--

def genPassword():
  s = ""
  for i in range(6):
    s = s + chr(random.randint(ord('a'), ord('z')))
  s = s + str(random.randint(101, 999))
  return s
#--

random.seed()
main_function()
  
  