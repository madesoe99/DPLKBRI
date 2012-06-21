def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterNasabahRekening = config.CreatePObjImplProxy('RegisterNasabahRekening')
  oRegisterNasabahRekening.Key = id

  config.BeginTransaction()
  try:
    #cek bila ada data ahli waris
    if oRegisterNasabahRekening.Ls_RegNRAhliWaris.MemberCount != 0:
      oRegisterNasabahRekening.Ls_RegNRAhliWaris.DeleteAllPObjs()
    
    #cek bila ada data rekening paket
    if oRegisterNasabahRekening.Ls_RegisterNasabahRekPaket.MemberCount != 0:
      oRegisterNasabahRekening.Ls_RegisterNasabahRekPaket.DeleteAllPObjs()

    #cek jika sudah membayar iuran pendaftaran
    if not oRegisterNasabahRekening.IsFieldNull('ID_Transaksi_IuranPendaftaran'):
      oRegisterNasabahRekening.LRegisterIuranPendaftaran.Delete()

    #cek jika sudah membayar iuran pendaftaran dan iuran peserta
    if not oRegisterNasabahRekening.IsFieldNull('ID_Transaksi_IuranPeserta'):
      oRegisterNasabahRekening.LRegisterIuranPeserta.Delete()

    #hapus objek Register Nasabah Rekening
    oRegisterNasabahRekening.Delete()
    
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1