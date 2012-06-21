import explorer

def FormGeneralSetData(uideflist, uiname, pobjconst):
  config = uideflist.config
  dir_dataset = uideflist.list_class.Dataset
  active_dataset = uideflist.active_directory.Dataset

  root_dir = explorer.get_dirconfig(config, pobjconst)[0]

  for rec_dir in explorer.browsedir(root_dir):
    record = dir_dataset.AddRecord()
    record.fd_name = rec_dir[0]
    record.fd_type = rec_dir[3]
    if record.fd_type == 0:
      record.fd_size = explorer.sz_kb(rec_dir[1])
    record.fd_type_char = rec_dir[2]
    record.fd_mdate = rec_dir[4]
  
  record = active_dataset.AddRecord()
  record.actual_server_path = root_dir
  record.display_path = 'SERVER\\'
  record.path_type = 0
  # path type :
  # 0 -> root directory
  # 1 -> regular directory
  # 2 -> virtual directory

  # stop further processing
  return 0
