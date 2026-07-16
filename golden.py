# ===== GOLDEN SCANNER - FINAL (BATCH DOWNLOAD + WITA) =====
# Strategi: Screening semua saham IDX, cari potensi gap up (buy sore, sell pagi)

import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
from datetime import datetime
import pytz
import time
import warnings
warnings.filterwarnings('ignore')

# ========== KONFIGURASI ==========
TOKEN = "8815512475:AAGdaw8FHq35iBo9XGbtoOH7zkk-UrdmWOE"
CHAT_ID = "8467853860"
# =================================

# ========== DAFTAR SAHAM IDX ==========
LIST_SAHAM = [
"AALI.JK","ABBA.JK","ABDA.JK","ABMM.JK","ACES.JK","ACST.JK","ADES.JK",
"ADHI.JK","AISA.JK","AKKU.JK","AKPI.JK","AKRA.JK","AKSI.JK","ALDO.JK",
"ALKA.JK","ALMI.JK","ALTO.JK","AMAG.JK","AMFG.JK","AMIN.JK","AMRT.JK",
"ANJT.JK","ANTM.JK","APEX.JK","APIC.JK","APII.JK","APLI.JK","APLN.JK",
"ARGO.JK","ARII.JK","ARNA.JK","ARTA.JK","ARTI.JK","ARTO.JK","ASBI.JK",
"ASDM.JK","ASGR.JK","ASII.JK","ASJT.JK","ASMI.JK","ASRI.JK","ASRM.JK",
"ASSA.JK","ATIC.JK","AUTO.JK","BABP.JK","BACA.JK","BAJA.JK","BALI.JK",
"BAPA.JK","BATA.JK","BAYU.JK","BBCA.JK","BBHI.JK","BBKP.JK","BBLD.JK",
"BBMD.JK","BBNI.JK","BBRI.JK","BBRM.JK","BBTN.JK","BBYB.JK","BCAP.JK",
"BCIC.JK","BCIP.JK","BDMN.JK","BEKS.JK","BEST.JK","BFIN.JK","BGTG.JK",
"BHIT.JK","BIKA.JK","BIMA.JK","BINA.JK","BIPI.JK","BIPP.JK","BIRD.JK",
"BISI.JK","BJBR.JK","BJTM.JK","BKDP.JK","BKSL.JK","BKSW.JK","BLTA.JK",
"BLTZ.JK","BMAS.JK","BMRI.JK","BMSR.JK","BMTR.JK","BNBA.JK","BNBR.JK",
"BNGA.JK","BNII.JK","BNLI.JK","BOLT.JK","BPFI.JK","BPII.JK","BRAM.JK",
"BRMS.JK","BRNA.JK","BRPT.JK","BSDE.JK","BSIM.JK","BSSR.JK","BSWD.JK",
"BTEK.JK","BTEL.JK","BTON.JK","BTPN.JK","BUDI.JK","BUKK.JK","BULL.JK",
"BUMI.JK","BUVA.JK","BVIC.JK","BWPT.JK","BYAN.JK","CANI.JK","CASS.JK",
"CEKA.JK","CENT.JK","CFIN.JK","CINT.JK","CITA.JK","CLPI.JK","CMNP.JK",
"CMPP.JK","CNKO.JK","CNTX.JK","COWL.JK","CPIN.JK","CPRO.JK","CSAP.JK",
"CTBN.JK","CTRA.JK","CTTH.JK","DART.JK","DEFI.JK","DEWA.JK","DGIK.JK",
"DILD.JK","DKFT.JK","DLTA.JK","DMAS.JK","DNAR.JK","DNET.JK","DOID.JK",
"DPNS.JK","DSFI.JK","DSNG.JK","DSSA.JK","DUTI.JK","DVLA.JK","DYAN.JK",
"ECII.JK","EKAD.JK","ELSA.JK","ELTY.JK","EMDE.JK","EMTK.JK","ENRG.JK",
"EPMT.JK","ERAA.JK","ERTX.JK","ESSA.JK","ESTI.JK","ETWA.JK","EXCL.JK",
"FAST.JK","FASW.JK","FISH.JK","FMII.JK","FORU.JK","FPNI.JK","GAMA.JK",
"GDST.JK","GDYR.JK","GEMA.JK","GEMS.JK","GGRM.JK","GIAA.JK","GJTL.JK",
"GLOB.JK","GMTD.JK","GOLD.JK","GOLL.JK","GPRA.JK","GSMF.JK","GTBO.JK",
"GWSA.JK","GZCO.JK","HADE.JK","HDFA.JK","HERO.JK","HEXA.JK","HITS.JK",
"HMSP.JK","HOME.JK","HOTL.JK","HRUM.JK","IATA.JK","IBFN.JK","IBST.JK",
"ICBP.JK","ICON.JK","IGAR.JK","IIKP.JK","IKAI.JK","IKBI.JK","IMAS.JK",
"IMJS.JK","IMPC.JK","INAF.JK","INAI.JK","INCI.JK","INCO.JK","INDF.JK",
"INDR.JK","INDS.JK","INDX.JK","INDY.JK","INKP.JK","INPC.JK","INPP.JK",
"INRU.JK","INTA.JK","INTD.JK","INTP.JK","IPOL.JK","ISAT.JK","ISSP.JK",
"ITMA.JK","ITMG.JK","JAWA.JK","JECC.JK","JIHD.JK","JKON.JK","JPFA.JK",
"JRPT.JK","JSMR.JK","JSPT.JK","JTPE.JK","KAEF.JK","KARW.JK","KBLI.JK",
"KBLM.JK","KBLV.JK","KBRI.JK","KDSI.JK","KIAS.JK","KICI.JK","KIJA.JK",
"KKGI.JK","KLBF.JK","KOBX.JK","KOIN.JK","KONI.JK","KOPI.JK","KPIG.JK",
"KRAS.JK","KREN.JK","LAPD.JK","LCGP.JK","LEAD.JK","LINK.JK","LION.JK",
"LMAS.JK","LMPI.JK","LMSH.JK","LPCK.JK","LPGI.JK","LPIN.JK","LPKR.JK",
"LPLI.JK","LPPF.JK","LPPS.JK","LRNA.JK","LSIP.JK","LTLS.JK","MAGP.JK",
"MAIN.JK","MAPI.JK","MAYA.JK","MBAP.JK","MBSS.JK","MBTO.JK","MCOR.JK",
"MDIA.JK","MDKA.JK","MDLN.JK","MDRN.JK","MEDC.JK","MEGA.JK","MERK.JK",
"META.JK","MFMI.JK","MGNA.JK","MICE.JK","MIDI.JK","MIKA.JK","MIRA.JK",
"MITI.JK","MKPI.JK","MLBI.JK","MLIA.JK","MLPL.JK","MLPT.JK","MMLP.JK",
"MNCN.JK","MPMX.JK","MPPA.JK","MRAT.JK","MREI.JK","MSKY.JK","MTDL.JK",
"MTFN.JK","MTLA.JK","MTSM.JK","MYOH.JK","MYOR.JK","MYTX.JK","NELY.JK",
"NIKL.JK","NIRO.JK","NISP.JK","NOBU.JK","NRCA.JK","OCAP.JK","OKAS.JK",
"OMRE.JK","PADI.JK","PALM.JK","PANR.JK","PANS.JK","PBRX.JK","PDES.JK",
"PEGE.JK","PGAS.JK","PGLI.JK","PICO.JK","PJAA.JK","PKPK.JK","PLAS.JK",
"PLIN.JK","PNBN.JK","PNBS.JK","PNIN.JK","PNLF.JK","PSAB.JK","PSDN.JK",
"PSKT.JK","PTBA.JK","PTIS.JK","PTPP.JK","PTRO.JK","PTSN.JK","PTSP.JK",
"PUDP.JK","PWON.JK","PYFA.JK","RAJA.JK","RALS.JK","RANC.JK","RBMS.JK",
"RDTX.JK","RELI.JK","RICY.JK","RIGS.JK","RIMO.JK","RODA.JK","ROTI.JK",
"RUIS.JK","SAFE.JK","SAME.JK","SCCO.JK","SCMA.JK","SCPI.JK","SDMU.JK",
"SDPC.JK","SDRA.JK","SGRO.JK","SHID.JK","SIDO.JK","SILO.JK","SIMA.JK",
"SIMP.JK","SIPD.JK","SKBM.JK","SKLT.JK","SKYB.JK","SMAR.JK","SMBR.JK",
"SMCB.JK","SMDM.JK","SMDR.JK","SMGR.JK","SMMA.JK","SMMT.JK","SMRA.JK",
"SMRU.JK","SMSM.JK","SOCI.JK","SONA.JK","SPMA.JK","SQMI.JK","SRAJ.JK",
"SRIL.JK","SRSN.JK","SRTG.JK","SSIA.JK","SSMS.JK","SSTM.JK","STAR.JK",
"STTP.JK","SUGI.JK","SULI.JK","SUPR.JK","TALF.JK","TARA.JK","TAXI.JK",
"TBIG.JK","TBLA.JK","TBMS.JK","TCID.JK","TELE.JK","TFCO.JK","TGKA.JK",
"TIFA.JK","TINS.JK","TIRA.JK","TIRT.JK","TKIM.JK","TLKM.JK","TMAS.JK",
"TMPO.JK","TOBA.JK","TOTL.JK","TOTO.JK","TOWR.JK","TPIA.JK","TPMA.JK",
"TRAM.JK","TRIL.JK","TRIM.JK","TRIO.JK","TRIS.JK","TRST.JK","TRUS.JK",
"TSPC.JK","ULTJ.JK","UNIC.JK","UNIT.JK","UNSP.JK","UNTR.JK","UNVR.JK",
"VICO.JK","VINS.JK","VIVA.JK","VOKS.JK","VRNA.JK","WAPO.JK","WEHA.JK",
"WICO.JK","WIIM.JK","WIKA.JK","WINS.JK","WOMF.JK","WSKT.JK","WTON.JK",
"YPAS.JK","YULE.JK","ZBRA.JK","SHIP.JK","CASA.JK","DAYA.JK","DPUM.JK",
"IDPR.JK","JGLE.JK","KINO.JK","MARI.JK","MKNT.JK","MTRA.JK","OASA.JK",
"POWR.JK","INCF.JK","WSBP.JK","PBSA.JK","PRDA.JK","BOGA.JK","BRIS.JK",
"PORT.JK","CARS.JK","MINA.JK","CLEO.JK","TAMU.JK","CSIS.JK","TGRA.JK",
"FIRE.JK","TOPS.JK","KMTR.JK","ARMY.JK","MAPB.JK","WOOD.JK","HRTA.JK",
"MABA.JK","HOKI.JK","MPOW.JK","MARK.JK","NASA.JK","MDKI.JK","BELL.JK",
"KIOS.JK","GMFI.JK","MTWI.JK","ZINC.JK","MCAS.JK","PPRE.JK","WEGE.JK",
"PSSI.JK","MORA.JK","DWGL.JK","PBID.JK","JMAS.JK","CAMP.JK","IPCM.JK",
"PCAR.JK","LCKM.JK","BOSS.JK","HELI.JK","JSKY.JK","INPS.JK","GHON.JK",
"TDPM.JK","DFAM.JK","NICK.JK","BTPS.JK","SPTO.JK","PRIM.JK","HEAL.JK",
"TRUK.JK","PZZA.JK","TUGU.JK","MSIN.JK","SWAT.JK","TNCA.JK","MAPA.JK",
"TCPI.JK","IPCC.JK","RISE.JK","BPTR.JK","POLL.JK","NFCX.JK","MGRO.JK",
"NUSA.JK","FILM.JK","ANDI.JK","LAND.JK","MOLI.JK","PANI.JK","DIGI.JK",
"CITY.JK","SAPX.JK","SURE.JK","HKMU.JK","MPRO.JK","DUCK.JK","GOOD.JK",
"SKRN.JK","YELO.JK","CAKK.JK","SATU.JK","SOSS.JK","DEAL.JK","POLA.JK",
"DIVA.JK","LUCK.JK","URBN.JK","SOTS.JK","ZONE.JK","PEHA.JK","FOOD.JK",
"BEEF.JK","POLI.JK","CLAY.JK","NATO.JK","JAYA.JK","COCO.JK","MTPS.JK",
"CPRI.JK","HRME.JK","POSA.JK","JAST.JK","FITT.JK","BOLA.JK","CCSI.JK",
"SFAN.JK","POLU.JK","KJEN.JK","KAYU.JK","ITIC.JK","PAMG.JK","IPTV.JK",
"BLUE.JK","ENVY.JK","EAST.JK","LIFE.JK","FUJI.JK","KOTA.JK","INOV.JK",
"ARKA.JK","SMKL.JK","HDIT.JK","KEEN.JK","BAPI.JK","TFAS.JK","GGRP.JK",
"OPMS.JK","NZIA.JK","SLIS.JK","PURE.JK","IRRA.JK","DMMX.JK","SINI.JK",
"WOWS.JK","ESIP.JK","TEBE.JK","KEJU.JK","PSGO.JK","AGAR.JK","IFSH.JK",
"REAL.JK","IFII.JK","PMJS.JK","UCID.JK","GLVA.JK","PGJO.JK","AMAR.JK",
"CSRA.JK","INDO.JK","AMOR.JK","TRIN.JK","DMND.JK","PURA.JK","PTPW.JK",
"TAMA.JK","IKAN.JK","SAMF.JK","SBAT.JK","KBAG.JK","CBMF.JK","RONY.JK",
"CSMI.JK","BBSS.JK","BHAT.JK","CASH.JK","TECH.JK","EPAC.JK","UANG.JK",
"PGUN.JK","SOFA.JK","PPGL.JK","TOYS.JK","SGER.JK","TRJA.JK","PNGO.JK",
"SCNP.JK","BBSI.JK","KMDS.JK","PURI.JK","SOHO.JK","HOMI.JK","ROCK.JK",
"ENZO.JK","PLAN.JK","PTDU.JK","ATAP.JK","VICI.JK","PMMP.JK","BANK.JK",
"WMUU.JK","EDGE.JK","UNIQ.JK","BEBS.JK","SNLK.JK","ZYRX.JK","LFLO.JK",
"FIMP.JK","TAPG.JK","NPGF.JK","LUCY.JK","ADCP.JK","HOPE.JK","MGLV.JK",
"TRUE.JK","LABA.JK","ARCI.JK","IPAC.JK","MASB.JK","BMHS.JK","FLMC.JK",
"NICL.JK","UVCR.JK","BUKA.JK","HAIS.JK","OILS.JK","GPSO.JK","MCOL.JK",
"RSGK.JK","RUNS.JK","SBMA.JK","CMNT.JK","GTSI.JK","IDEA.JK","KUAS.JK",
"BOBA.JK","MTEL.JK","DEPO.JK","BINO.JK","CMRY.JK","WGSH.JK","TAYS.JK",
"WMPP.JK","RMKE.JK","OBMD.JK","AVIA.JK","IPPE.JK","NASI.JK","BSML.JK",
"DRMA.JK","ADMR.JK","SEMA.JK","ASLC.JK","NETV.JK","BAUT.JK","ENAK.JK",
"NTBK.JK","SMKM.JK","STAA.JK","NANO.JK","BIKE.JK","WIRG.JK","SICO.JK",
"GOTO.JK","TLDN.JK","MTMH.JK","WINR.JK","IBOS.JK","OLIV.JK","ASHA.JK",
"SWID.JK","TRGU.JK","ARKO.JK","CHEM.JK","DEWI.JK","AXIO.JK","KRYA.JK",
"HATM.JK","RCCC.JK","GULA.JK","JARR.JK","AMMS.JK","RAFI.JK","KKES.JK",
"ELPI.JK","EURO.JK","KLIN.JK","TOOL.JK","BUAH.JK","CRAB.JK","MEDS.JK",
"COAL.JK","PRAY.JK","CBUT.JK","BELI.JK","MKTR.JK","OMED.JK","BSBK.JK",
"PDPP.JK","KDTN.JK","ZATA.JK","NINE.JK","MMIX.JK","PADA.JK","ISAP.JK",
"VTNY.JK","SOUL.JK","ELIT.JK","BEER.JK","CBPE.JK","SUNI.JK","CBRE.JK",
"WINE.JK","BMBL.JK","PEVE.JK","LAJU.JK","FWCT.JK","NAYZ.JK","IRSX.JK",
"PACK.JK","VAST.JK","CHIP.JK","HALO.JK","KING.JK","PGEO.JK","FUTR.JK",
"HILL.JK","BDKR.JK","PTMP.JK","SAGE.JK","TRON.JK","CUAN.JK","NSSS.JK",
"GTRA.JK","HAJJ.JK","JATI.JK","TYRE.JK","MPXL.JK","SMIL.JK","KLAS.JK",
"MAXI.JK","VKTR.JK","RELF.JK","AMMN.JK","CRSN.JK","GRPM.JK","WIDI.JK",
"TGUK.JK","INET.JK","MAHA.JK","RMKO.JK","CNMA.JK","FOLK.JK","HBAT.JK",
"GRIA.JK","PPRI.JK","ERAL.JK","CYBR.JK","MUTU.JK","LMAX.JK","HUMI.JK",
"MSIE.JK","RSCH.JK","BABY.JK","AEGS.JK","IOTF.JK","KOCI.JK","PTPS.JK",
"BREN.JK","STRK.JK","KOKA.JK","LOPI.JK","UDNG.JK","RGAS.JK","MSTI.JK",
"IKPM.JK","AYAM.JK","SURI.JK","ASLI.JK","GRPH.JK","SMGA.JK","UNTD.JK",
"TOSK.JK","MPIX.JK","ALII.JK","MKAP.JK","MEJA.JK","LIVE.JK","HYGN.JK",
"BAIK.JK","VISI.JK","AREA.JK","MHKI.JK","ATLA.JK","DATA.JK","SOLA.JK",
"BATR.JK","SPRE.JK","PART.JK","GOLF.JK","ISEA.JK","BLES.JK","GUNA.JK",
"LABS.JK","DOSS.JK","NEST.JK","PTMR.JK","VERN.JK","DAAZ.JK","BOAT.JK",
"NAIK.JK","AADI.JK","MDIY.JK","KSIX.JK","RATU.JK","YOII.JK","HGII.JK",
"BRRC.JK","DGWG.JK","CBDK.JK","OBAT.JK","MINE.JK","ASPR.JK","PSAT.JK",
"COIN.JK","CDIA.JK","BLOG.JK","MERI.JK","KAQI.JK","YUPI.JK","FORE.JK",
"MDLA.JK","DKHH.JK","AYLS.JK","DADA.JK","ASPI.JK","ESTA.JK","BESS.JK",
"AMAN.JK","CARE.JK","PIPA.JK","NCKL.JK","MENN.JK","AWAN.JK","MBMA.JK",
"RAAM.JK","DOOH.JK","CGAS.JK","NICE.JK","MSJA.JK","SMLE.JK","ACRO.JK",
"MANG.JK","WIFI.JK","FAPA.JK","DCII.JK","KETR.JK","DGNS.JK","UFOE.JK",
"CHEK.JK","PMUI.JK","EMAS.JK","PJHB.JK","RLCO.JK","SUPA.JK","WBSA.JK",
"JECX.JK","JELI.JK","EMMI.JK","BACH.JK","PRDL.JK","RANS.JK","ADMF.JK",
"ADMG.JK","ADRO.JK","AGII.JK","AGRO.JK","AGRS.JK","AHAP.JK","AIMS.JK",
"PNSE.JK","POLY.JK","POOL.JK","PPRO.JK"
]

def kirim_pesan(pesan):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.get(url, params={
            'chat_id': CHAT_ID,
            'text': pesan,
            'parse_mode': 'HTML'
        }, timeout=30)
        if resp.status_code == 200:
            print("✅ Pesan terkirim!")
        else:
            print(f"❌ Gagal: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error kirim: {e}")

def detect_support_resistance(df):
    high = df['High']
    low = df['Low']
    close = df['Close']
    resistance = high.rolling(20).max().iloc[-1]
    support = low.rolling(20).min().iloc[-1]
    current_close = close.iloc[-1]
    is_breakout = current_close > resistance * 1.005
    is_support_bounce = current_close > support * 1.005
    breakout_strength = (current_close / resistance - 1) * 100 if is_breakout else 0
    return {
        'resistance': resistance,
        'support': support,
        'is_breakout': is_breakout,
        'is_support_bounce': is_support_bounce,
        'breakout_strength': breakout_strength
    }

def detect_chart_pattern(df):
    close = df['Close']
    high = df['High']
    low = df['Low']
    recent_high = high.iloc[-10:].max()
    recent_low = low.iloc[-10:].min()
    range_width = (recent_high - recent_low) / recent_high * 100
    lows_rising = low.iloc[-10:].is_monotonic_increasing
    highs_flat = (high.iloc[-10:].max() - high.iloc[-10:].min()) / high.iloc[-10:].mean() * 100 < 3
    if range_width < 10 and close.iloc[-1] > close.iloc[-5]:
        return "🚩 Bullish Flag"
    elif lows_rising and highs_flat and close.iloc[-1] > high.iloc[-2]:
        return "📐 Ascending Triangle"
    elif close.iloc[-1] > close.iloc[-5] * 1.05 and high.iloc[-1] > high.iloc[-2]:
        return "📈 Momentum Breakout"
    else:
        return "⚪ Tidak terdeteksi"

def scrape_sentimen(kode):
    try:
        saham = yf.Ticker(kode)
        nama = saham.info.get('shortName', kode.replace('.JK', ''))
        search_url = f"https://news.google.com/search?q={nama.replace(' ', '+')}+saham"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(search_url, headers=headers, timeout=5)
        if resp.status_code == 200:
            text = resp.text.lower()
            pos = ['naik', 'melesat', 'rekor', 'laba', 'dividen', 'ekspansi', 'akuisisi']
            neg = ['turun', 'anjlok', 'rugi', 'utang', 'krisis', 'skandal']
            pos_count = sum(1 for kw in pos if kw in text)
            neg_count = sum(1 for kw in neg if kw in text)
            if pos_count > neg_count:
                return "📰 Positif (Buy on Rumor)", pos_count - neg_count
            elif neg_count > pos_count:
                return "📰 Negatif (Sell on News)", neg_count - pos_count
            else:
                return "📰 Netral", 0
        return "📰 Tidak ada berita", 0
    except:
        return "📰 Gagal", 0

def analisis_golden(kode, df):
    try:
        if df.empty or len(df) < 30:
            return None
        info = yf.Ticker(kode).info
        last = df.iloc[-1]
        prev = df.iloc[-2]
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['MA20'] = ta.sma(df['Close'], length=20)
        df['MA50'] = ta.sma(df['Close'], length=50)
        df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
        harga = last['Close']
        atr = df['ATR'].iloc[-1]
        rsi = df['RSI'].iloc[-1]
        perubahan = ((harga - prev['Close']) / prev['Close']) * 100
        avg_vol_5 = df['Volume'].rolling(5).mean().iloc[-1]
        avg_vol_20 = df['Volume'].rolling(20).mean().iloc[-1]
        vol_hari = last['Volume']
        volume_spike = vol_hari / avg_vol_5 if avg_vol_5 > 0 else 0
        volume_bandar = vol_hari > avg_vol_20 * 2.0
        snr = detect_support_resistance(df)
        pattern = detect_chart_pattern(df)
        sentimen_label, sentimen_score = scrape_sentimen(kode)
        skor = 0
        if 50 <= rsi <= 70:
            skor += 20
        elif 40 <= rsi < 50 or 70 < rsi <= 80:
            skor += 10
        if snr['is_breakout']:
            skor += 25
        elif snr['is_support_bounce']:
            skor += 15
        if volume_bandar:
            skor += 25
        elif volume_spike > 1.5:
            skor += 15
        if sentimen_score > 0:
            skor += 15
        elif sentimen_score < 0:
            skor += 0
        else:
            skor += 7
        if 'Bullish' in pattern or 'Breakout' in pattern:
            skor += 15
        elif 'Konsolidasi' in pattern:
            skor += 10
        if skor >= 70:
            entry = harga
            sl = round(harga - (1.5 * atr), 2)
            tp1 = round(harga + (2.0 * atr), 2)
            tp2 = round(harga + (3.5 * atr), 2)
            signal = "🔥 ENTRY SORE (GAP UP)"
            rekom = f"Beli Rp{entry:.0f}, target gap up besok"
        else:
            sl = tp1 = tp2 = None
            signal = "⏳ Tahan Diri"
            rekom = "Belum memenuhi kriteria"
        return {
            'kode': kode.replace('.JK', ''),
            'nama': info.get('shortName', kode)[:25],
            'harga': harga,
            'perubahan': perubahan,
            'rsi': round(rsi, 2),
            'ma20': round(df['MA20'].iloc[-1], 2),
            'ma50': round(df['MA50'].iloc[-1], 2),
            'volume': int(vol_hari),
            'volume_spike': round(volume_spike, 1),
            'volume_bandar': volume_bandar,
            'support': round(snr['support'], 2),
            'resistance': round(snr['resistance'], 2),
            'is_breakout': snr['is_breakout'],
            'breakout_strength': round(snr['breakout_strength'], 2),
            'pattern': pattern,
            'sentimen': sentimen_label,
            'skor': skor,
            'signal': signal,
            'rekom': rekom,
            'entry': harga,
            'sl': sl,
            'tp1': tp1,
            'tp2': tp2,
        }
    except Exception as e:
        return None

# ========== MAIN ==========
wita = pytz.timezone('Asia/Makassar')
waktu_str = datetime.now(wita).strftime('%d-%m-%Y %H:%M')
print(f"🚀 GOLDEN SCANNER (WITA) - {waktu_str}")

# === BATCH DOWNLOAD ===
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

batch_size = 90
batches = list(chunk_list(LIST_SAHAM, batch_size))
print(f"📥 Total {len(LIST_SAHAM)} saham, dipecah menjadi {len(batches)} batch.")

all_data = {}
batch_count = 0

for batch in batches:
    batch_count += 1
    print(f"🔄 Memproses batch {batch_count}/{len(batches)} ({len(batch)} saham)...")
    try:
        data = yf.download(
            tickers=batch,
            period="60d",
            group_by='ticker',
            threads=False,
            progress=False,
            auto_adjust=False
        )
        for ticker in batch:
            if ticker in data and not data[ticker].empty:
                all_data[ticker] = data[ticker]
        print(f"✅ Batch {batch_count} selesai.")
    except Exception as e:
        print(f"❌ Batch {batch_count} gagal: {e}")
    time.sleep(2)

print(f"✅ Total berhasil di-download: {len(all_data)} saham")

# === PROSES ===
semua_hasil = []
for kode in LIST_SAHAM:
    if kode not in all_data or all_data[kode].empty:
        continue
    df = all_data[kode].copy()
    res = analisis_golden(kode, df)
    if res:
        semua_hasil.append(res)

semua_hasil.sort(key=lambda x: x['skor'], reverse=True)
potensial = [h for h in semua_hasil if h['skor'] >= 70]
pantauan = [h for h in semua_hasil if 50 <= h['skor'] < 70]

print(f"✅ Berhasil menganalisis {len(semua_hasil)} saham.")

# === PESAN TELEGRAM ===
pesan = f"<b>🌟 GOLDEN SCANNER (WITA) - {waktu_str}</b>\n"
pesan += f"📌 Total: {len(semua_hasil)} saham | 🔥 Potensial: {len(potensial)}\n"
pesan += "=" * 30 + "\n\n"

if potensial:
    pesan += "<b>🔥 SAHAM POTENSIAL GAP UP (SKOR ≥ 70)</b>\n\n"
    for h in potensial[:10]:
        pesan += f"🏢 <b>{h['kode']}</b> - {h['nama']}\n"
        pesan += f"💰 Rp{h['harga']:.0f} | 📈 {h['perubahan']:+.2f}% | ⭐ Skor: {h['skor']}\n"
        pesan += f"📊 RSI: {h['rsi']} | MA20: Rp{h['ma20']:.0f} | MA50: Rp{h['ma50']:.0f}\n"
        pesan += f"📦 Vol: {h['volume']:,} | Spike: {h['volume_spike']}x | Bandar: {'✅' if h['volume_bandar'] else '❌'}\n"
        pesan += f"📐 S: Rp{h['support']:.0f} | R: Rp{h['resistance']:.0f} | Breakout: {'✅' if h['is_breakout'] else '❌'} ({h['breakout_strength']:.1f}%)\n"
        pesan += f"📈 Pattern: {h['pattern']}\n"
        pesan += f"{h['sentimen']}\n"
        pesan += f"💡 <b>Strategi:</b> {h['rekom']}\n"
        pesan += f"🔴 <b>SL:</b> Rp{h['sl']:.0f} | 🟢 <b>TP1:</b> Rp{h['tp1']:.0f} | 🟢 <b>TP2:</b> Rp{h['tp2']:.0f}\n"
        pesan += "-" * 25 + "\n"
else:
    pesan += "⏳ Belum ada saham dengan skor ≥ 70 hari ini.\n\n"

if pantauan:
    pesan += "<b>📊 PANTAUAN (Skor 50-69)</b>\n"
    for h in pantauan[:5]:
        pesan += f"🔹 {h['kode']} | Skor: {h['skor']} | RSI: {h['rsi']} | Rp{h['harga']:.0f}\n"

kirim_pesan(pesan)
print("✅ Selesai! Cek Telegram.")
