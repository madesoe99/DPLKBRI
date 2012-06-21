def FormShow(form, parameter):
    pass

def AfterLookup_NoPeserta(sender, linkui) :
    form = sender.OwnerForm
    app = form.ClientApplication
    uipNas = form.GetUIPartByName('uipNasabah')
    uipData = form.GetUIPartByName('uipDataPeserta')
    res = app.ExecuteScript('transaksi/AmbilInfo_SRR',\
          app.CreateValues(['no_peserta',uipNas.GetFieldValue('LRekeningDPLK.no_peserta')])\
        )
    rec = res.FirstRecord
    uipNas.nama_lengkap = rec.nama_lengkap
    uipNas.tempat_lahir = rec.tempat_lahir
    uipNas.tanggal_lahir = rec.tanggal_lahir
    uipNas.no_identitas_diri = rec.no_identitas_diri
    uipNas.jenis_kelamin = rec.jenis_kelamin
    uipNas.SetFieldValue('LDaerahAsal.kode_propinsi',rec.kode_propinsi)
    uipNas.SetFieldValue('LDaerahAsal.nama_propinsi',rec.nama_propinsi)

    qTransDPLK = form.GetPanelByName('qTransaksiDPLK')
    qTransDPLK.SetParameter('no_peserta',rec.no_peserta)
    qTransDPLK.SetParameter('tgl_transaksi_awal',rec.tgl_transaksi_awal)
    qTransDPLK.DisplayData()

    uipData.kode_paket = rec.kode_paket
    uipData.nama_paket = rec.nama_paket
    uipData.SRR_paket = rec.SRR_paket
    uipData.distribusi_inv = rec.distribusi_inv
    uipData.SRR_before = rec.SRR_bln_lalu
    uipData.tgl_akhir_SRR = rec.tgl_transaksi_awal
    uipData.SRR_peserta = rec.SRR_peserta
    

    return 0

