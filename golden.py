# ===== SUPER SCREENER (TEKNIKAL + MONEY FLOW) - GOLDEN.PY FINAL =====
# Perbaikan: SyntaxError fixed, MA50 fallback, Breakout logic, RSI overbought penalty

import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
from datetime import datetime
import pytz
import time
import random
import warnings
warnings.filterwarnings('ignore')

# ========== KONFIGURASI ==========
TOKEN = "8815512475:AAGa6k3GHqoWisqiPWaD1MUR0dD75h4_hdU"   # Ganti dengan token baru dari @BotFather
CHAT_ID = "8467853860"      # ID Telegram kamu
# =================================

# ========== LIST SAHAM LENGKAP (900+ IDX) ==========
LIST_SAHAM = [
"AALI.JK","ABBA.JK","ABDA.JK","ABMM.JK","ACES.JK","ACST.JK","ADES.JK","ADHI.JK","AISA.JK","AKKU.JK","AKPI.JK","AKRA.JK","AKSI.JK","ALDO.JK","ALKA.JK","ALMI.JK","ALTO.JK","AMAG.JK","AMFG.JK","AMIN.JK","AMRT.JK","ANJT.JK","ANTM.JK","APEX.JK","APIC.JK","APII.JK","APLI.JK","APLN.JK","ARGO.JK","ARII.JK","ARNA.JK","ARTA.JK","ARTI.JK","ARTO.JK","ASBI.JK","ASDM.JK","ASGR.JK","ASII.JK","ASJT.JK","ASMI.JK","ASRI.JK","ASRM.JK","ASSA.JK","ATIC.JK","AUTO.JK","BABP.JK","BACA.JK","BAJA.JK","BALI.JK","BAPA.JK","BATA.JK","BAYU.JK","BBCA.JK","BBHI.JK","BBKP.JK","BBLD.JK","BBMD.JK","BBNI.JK","BBRI.JK","BBRM.JK","BBTN.JK","BBYB.JK","BCAP.JK","BCIC.JK","BCIP.JK","BDMN.JK","BEKS.JK","BEST.JK","BFIN.JK","BGTG.JK","BHIT.JK","BIKA.JK","BIMA.JK","BINA.JK","BIPI.JK","BIPP.JK","BIRD.JK","BISI.JK","BJBR.JK","BJTM.JK","BKDP.JK","BKSL.JK","BKSW.JK","BLTA.JK","BLTZ.JK","BMAS.JK","BMRI.JK","BMSR.JK","BMTR.JK","BNBA.JK","BNBR.JK","BNGA.JK","BNII.JK","BNLI.JK","BOLT.JK","BPFI.JK","BPII.JK","BRAM.JK","BRMS.JK","BRNA.JK","BRPT.JK","BSDE.JK","BSIM.JK","BSSR.JK","BSWD.JK","BTEK.JK","BTEL.JK","BTON.JK","BTPN.JK","BUDI.JK","BUKK.JK","BULL.JK","BUMI.JK","BUVA.JK","BVIC.JK","BWPT.JK","BYAN.JK","CANI.JK","CASS.JK","CEKA.JK","CENT.JK","CFIN.JK","CINT.JK","CITA.JK","CLPI.JK","CMNP.JK","CMPP.JK","CNKO.JK","CNTX.JK","COWL.JK","CPIN.JK","CPRO.JK","CSAP.JK","CTBN.JK","CTRA.JK","CTTH.JK","DART.JK","DEFI.JK","DEWA.JK","DGIK.JK","DILD.JK","DKFT.JK","DLTA.JK","DMAS.JK","DNAR.JK","DNET.JK","DOID.JK","DPNS.JK","DSFI.JK","DSNG.JK","DSSA.JK","DUTI.JK","DVLA.JK","DYAN.JK","ECII.JK","EKAD.JK","ELSA.JK","ELTY.JK","EMDE.JK","EMTK.JK","ENRG.JK","EPMT.JK","ERAA.JK","ERTX.JK","ESSA.JK","ESTI.JK","ETWA.JK","EXCL.JK","FAST.JK","FASW.JK","FISH.JK","FMII.JK","FORU.JK","FPNI.JK","GAMA.JK","GDST.JK","GDYR.JK","GEMA.JK","GEMS.JK","GGRM.JK","GIAA.JK","GJTL.JK","GLOB.JK","GMTD.JK","GOLD.JK","GOLL.JK","GPRA.JK","GSMF.JK","GTBO.JK","GWSA.JK","GZCO.JK","HADE.JK","HDFA.JK","HERO.JK","HEXA.JK","HITS.JK","HMSP.JK","HOME.JK","HOTL.JK","HRUM.JK","IATA.JK","IBFN.JK","IBST.JK","ICBP.JK","ICON.JK","IGAR.JK","IIKP.JK","IKAI.JK","IKBI.JK","IMAS.JK","IMJS.JK","IMPC.JK","INAF.JK","INAI.JK","INCI.JK","INCO.JK","INDF.JK","INDR.JK","INDS.JK","INDX.JK","INDY.JK","INKP.JK","INPC.JK","INPP.JK","INRU.JK","INTA.JK","INTD.JK","INTP.JK","IPOL.JK","ISAT.JK","ISSP.JK","ITMA.JK","ITMG.JK","JAWA.JK","JECC.JK","JIHD.JK","JKON.JK","JPFA.JK","JRPT.JK","JSMR.JK","JSPT.JK","JTPE.JK","KAEF.JK","KARW.JK","KBLI.JK","KBLM.JK","KBLV.JK","KBRI.JK","KDSI.JK","KIAS.JK","KICI.JK","KIJA.JK","KKGI.JK","KLBF.JK","KOBX.JK","KOIN.JK","KONI.JK","KOPI.JK","KPIG.JK","KRAS.JK","KREN.JK","LAPD.JK","LCGP.JK","LEAD.JK","LINK.JK","LION.JK","LMAS.JK","LMPI.JK","LMSH.JK","LPCK.JK","LPGI.JK","LPIN.JK","LPKR.JK","LPLI.JK","LPPF.JK","LPPS.JK","LRNA.JK","LSIP.JK","LTLS.JK","MAGP.JK","MAIN.JK","MAPI.JK","MAYA.JK","MBAP.JK","MBSS.JK","MBTO.JK","MCOR.JK","MDIA.JK","MDKA.JK","MDLN.JK","MDRN.JK","MEDC.JK","MEGA.JK","MERK.JK","META.JK","MFMI.JK","MGNA.JK","MICE.JK","MIDI.JK","MIKA.JK","MIRA.JK","MITI.JK","MKPI.JK","MLBI.JK","MLIA.JK","MLPL.JK","MLPT.JK","MMLP.JK","MNCN.JK","MPMX.JK","MPPA.JK","MRAT.JK","MREI.JK","MSKY.JK","MTDL.JK","MTFN.JK","MTLA.JK","MTSM.JK","MYOH.JK","MYOR.JK","MYTX.JK","NELY.JK","NIKL.JK","NIRO.JK","NISP.JK","NOBU.JK","NRCA.JK","OCAP.JK","OKAS.JK","OMRE.JK","PADI.JK","PALM.JK","PANR.JK","PANS.JK","PBRX.JK","PDES.JK","PEGE.JK","PGAS.JK","PGLI.JK","PICO.JK","PJAA.JK","PKPK.JK","PLAS.JK","PLIN.JK","PNBN.JK","PNBS.JK","PNIN.JK","PNLF.JK","PSAB.JK","PSDN.JK","PSKT.JK","PTBA.JK","PTIS.JK","PTPP.JK","PTRO.JK","PTSN.JK","PTSP.JK","PUDP.JK","PWON.JK","PYFA.JK","RAJA.JK","RALS.JK","RANC.JK","RBMS.JK","RDTX.JK","RELI.JK","RICY.JK","RIGS.JK","RIMO.JK","RODA.JK","ROTI.JK","RUIS.JK","SAFE.JK","SAME.JK","SCCO.JK","SCMA.JK","SCPI.JK","SDMU.JK","SDPC.JK","SDRA.JK","SGRO.JK","SHID.JK","SIDO.JK","SILO.JK","SIMA.JK","SIMP.JK","SIPD.JK","SKBM.JK","SKLT.JK","SKYB.JK","SMAR.JK","SMBR.JK","SMCB.JK","SMDM.JK","SMDR.JK","SMGR.JK","SMMA.JK","SMMT.JK","SMRA.JK","SMRU.JK","SMSM.JK","SOCI.JK","SONA.JK","SPMA.JK","SQMI.JK","SRAJ.JK","SRIL.JK","SRSN.JK","SRTG.JK","SSIA.JK","SSMS.JK","SSTM.JK","STAR.JK","STTP.JK","SUGI.JK","SULI.JK","SUPR.JK","TALF.JK","TARA.JK","TAXI.JK","TBIG.JK","TBLA.JK","TBMS.JK","TCID.JK","TELE.JK","TFCO.JK","TGKA.JK","TIFA.JK","TINS.JK","TIRA.JK","TIRT.JK","TKIM.JK","TLKM.JK","TMAS.JK","TMPO.JK","TOBA.JK","TOTL.JK","TOTO.JK","TOWR.JK","TPIA.JK","TPMA.JK","TRAM.JK","TRIL.JK","TRIM.JK","TRIO.JK","TRIS.JK","TRST.JK","TRUS.JK","TSPC.JK","ULTJ.JK","UNIC.JK","UNIT.JK","UNSP.JK","UNTR.JK","UNVR.JK","VICO.JK","VINS.JK","VIVA.JK","VOKS.JK","VRNA.JK","WAPO.JK","WEHA.JK","WICO.JK","WIIM.JK","WIKA.JK","WINS.JK","WOMF.JK","WSKT.JK","WTON.JK","YPAS.JK","YULE.JK","ZBRA.JK","SHIP.JK","CASA.JK","DAYA.JK","DPUM.JK","IDPR.JK","JGLE.JK","KINO.JK","MARI.JK","MKNT.JK","MTRA.JK","OASA.JK","POWR.JK","INCF.JK","WSBP.JK","PBSA.JK","PRDA.JK","BOGA.JK","BRIS.JK","PORT.JK","CARS.JK","MINA.JK","CLEO.JK","TAMU.JK","CSIS.JK","TGRA.JK","FIRE.JK","TOPS.JK","KMTR.JK","ARMY.JK","MAPB.JK","WOOD.JK","HRTA.JK","MABA.JK","HOKI.JK","MPOW.JK","MARK.JK","NASA.JK","MDKI.JK","BELL.JK","KIOS.JK","GMFI.JK","MTWI.JK","ZINC.JK","MCAS.JK","PPRE.JK","WEGE.JK","PSSI.JK","MORA.JK","DWGL.JK","PBID.JK","JMAS.JK","CAMP.JK","IPCM.JK","PCAR.JK","LCKM.JK","BOSS.JK","HELI.JK","JSKY.JK","INPS.JK","GHON.JK","TDPM.JK","DFAM.JK","NICK.JK","BTPS.JK","SPTO.JK","PRIM.JK","HEAL.JK","TRUK.JK","PZZA.JK","TUGU.JK","MSIN.JK","SWAT.JK","TNCA.JK","MAPA.JK","TCPI.JK","IPCC.JK","RISE.JK","BPTR.JK","POLL.JK","NFCX.JK","MGRO.JK","NUSA.JK","FILM.JK","ANDI.JK","LAND.JK","MOLI.JK","PANI.JK","DIGI.JK","CITY.JK","SAPX.JK","SURE.JK","HKMU.JK","MPRO.JK","DUCK.JK","GOOD.JK","SKRN.JK","YELO.JK","CAKK.JK","SATU.JK","SOSS.JK","DEAL.JK","POLA.JK","DIVA.JK","LUCK.JK","URBN.JK","SOTS.JK","ZONE.JK","PEHA.JK","FOOD.JK","BEEF.JK","POLI.JK","CLAY.JK","NATO.JK","JAYA.JK","COCO.JK","MTPS.JK","CPRI.JK","HRME.JK","POSA.JK","JAST.JK","FITT.JK","BOLA.JK","CCSI.JK","SFAN.JK","POLU.JK","KJEN.JK","KAYU.JK","ITIC.JK","PAMG.JK","IPTV.JK","BLUE.JK","ENVY.JK","EAST.JK","LIFE.JK","FUJI.JK","KOTA.JK","INOV.JK","ARKA.JK","SMKL.JK","HDIT.JK","KEEN.JK","BAPI.JK","TFAS.JK","GGRP.JK","OPMS.JK","NZIA.JK","SLIS.JK","PURE.JK","IRRA.JK","DMMX.JK","SINI.JK","WOWS.JK","ESIP.JK","TEBE.JK","KEJU.JK","PSGO.JK","AGAR.JK","IFSH.JK","REAL.JK","IFII.JK","PMJS.JK","UCID.JK","GLVA.JK","PGJO.JK","AMAR.JK","CSRA.JK","INDO.JK","AMOR.JK","TRIN.JK","DMND.JK","PURA.JK","PTPW.JK","TAMA.JK","IKAN.JK","SAMF.JK","SBAT.JK","KBAG.JK","CBMF.JK","RONY.JK","CSMI.JK","BBSS.JK","BHAT.JK","CASH.JK","TECH.JK","EPAC.JK","UANG.JK","PGUN.JK","SOFA.JK","PPGL.JK","TOYS.JK","SGER.JK","TRJA.JK","PNGO.JK","SCNP.JK","BBSI.JK","KMDS.JK","PURI.JK","SOHO.JK","HOMI.JK","ROCK.JK","ENZO.JK","PLAN.JK","PTDU.JK","ATAP.JK","VICI.JK","PMMP.JK","BANK.JK","WMUU.JK","EDGE.JK","UNIQ.JK","BEBS.JK","SNLK.JK","ZYRX.JK","LFLO.JK","FIMP.JK","TAPG.JK","NPGF.JK","LUCY.JK","ADCP.JK","HOPE.JK","MGLV.JK","TRUE.JK","LABA.JK","ARCI.JK","IPAC.JK","MASB.JK","BMHS.JK","FLMC.JK","NICL.JK","UVCR.JK","BUKA.JK","HAIS.JK","OILS.JK","GPSO.JK","MCOL.JK","RSGK.JK","RUNS.JK","SBMA.JK","CMNT.JK","GTSI.JK","IDEA.JK","KUAS.JK","BOBA.JK","MTEL.JK","DEPO.JK","BINO.JK","CMRY.JK","WGSH.JK","TAYS.JK","WMPP.JK","RMKE.JK","OBMD.JK","AVIA.JK","IPPE.JK","NASI.JK","BSML.JK","DRMA.JK","ADMR.JK","SEMA.JK","ASLC.JK","NETV.JK","BAUT.JK","ENAK.JK","NTBK.JK","SMKM.JK","STAA.JK","NANO.JK","BIKE.JK","WIRG.JK","SICO.JK","GOTO.JK","TLDN.JK","MTMH.JK","WINR.JK","IBOS.JK","OLIV.JK","ASHA.JK","SWID.JK","TRGU.JK","ARKO.JK","CHEM.JK","DEWI.JK","AXIO.JK","KRYA.JK","HATM.JK","RCCC.JK","GULA.JK","JARR.JK","AMMS.JK","RAFI.JK","KKES.JK","ELPI.JK","EURO.JK","KLIN.JK","TOOL.JK","BUAH.JK","CRAB.JK","MEDS.JK","COAL.JK","PRAY.JK","CBUT.JK","BELI.JK","MKTR.JK","OMED.JK","BSBK.JK","PDPP.JK","KDTN.JK","ZATA.JK","NINE.JK","MMIX.JK","PADA.JK","ISAP.JK","VTNY.JK","SOUL.JK","ELIT.JK","BEER.JK","CBPE.JK","SUNI.JK","CBRE.JK","WINE.JK","BMBL.JK","PEVE.JK","LAJU.JK","FWCT.JK","NAYZ.JK","IRSX.JK","PACK.JK","VAST.JK","CHIP.JK","HALO.JK","KING.JK","PGEO.JK","FUTR.JK","HILL.JK","BDKR.JK","PTMP.JK","SAGE.JK","TRON.JK","CUAN.JK","NSSS.JK","GTRA.JK","HAJJ.JK","JATI.JK","TYRE.JK","MPXL.JK","SMIL.JK","KLAS.JK","MAXI.JK","VKTR.JK","RELF.JK","AMMN.JK","CRSN.JK","GRPM.JK","WIDI.JK","TGUK.JK","INET.JK","MAHA.JK","RMKO.JK","CNMA.JK","FOLK.JK","HBAT.JK","GRIA.JK","PPRI.JK","ERAL.JK","CYBR.JK","MUTU.JK","LMAX.JK","HUMI.JK","MSIE.JK","RSCH.JK","BABY.JK","AEGS.JK","IOTF.JK","KOCI.JK","PTPS.JK","BREN.JK","STRK.JK","KOKA.JK","LOPI.JK","UDNG.JK","RGAS.JK","MSTI.JK","IKPM.JK","AYAM.JK","SURI.JK","ASLI.JK","GRPH.JK","SMGA.JK","UNTD.JK","TOSK.JK","MPIX.JK","ALII.JK","MKAP.JK","MEJA.JK","LIVE.JK","HYGN.JK","BAIK.JK","VISI.JK","AREA.JK","MHKI.JK","ATLA.JK","DATA.JK","SOLA.JK","BATR.JK","SPRE.JK","PART.JK","GOLF.JK","ISEA.JK","BLES.JK","GUNA.JK","LABS.JK","DOSS.JK","NEST.JK","PTMR.JK","VERN.JK","DAAZ.JK","BOAT.JK","NAIK.JK","AADI.JK","MDIY.JK","KSIX.JK","RATU.JK","YOII.JK","HGII.JK","BRRC.JK","DGWG.JK","CBDK.JK","OBAT.JK","MINE.JK","ASPR.JK","PSAT.JK","COIN.JK","CDIA.JK","BLOG.JK","MERI.JK","KAQI.JK","YUPI.JK","FORE.JK","MDLA.JK","DKHH.JK","AYLS.JK","DADA.JK","ASPI.JK","ESTA.JK","BESS.JK","AMAN.JK","CARE.JK","PIPA.JK","NCKL.JK","MENN.JK","AWAN.JK","MBMA.JK","RAAM.JK","DOOH.JK","CGAS.JK","NICE.JK","MSJA.JK","SMLE.JK","ACRO.JK","MANG.JK","WIFI.JK","FAPA.JK","DCII.JK","KETR.JK","DGNS.JK","UFOE.JK","CHEK.JK","PMUI.JK","EMAS.JK","PJHB.JK","RLCO.JK","SUPA.JK","WBSA.JK","JECX.JK","JELI.JK","EMMI.JK","BACH.JK","PRDL.JK","RANS.JK","ADMF.JK","ADMG.JK","ADRO.JK","AGII.JK","AGRO.JK","AGRS.JK","AHAP.JK","AIMS.JK","PNSE.JK","POLY.JK","POOL.JK","PPRO.JK"
]

# ===========================================================

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
    high = df['High']; low = df['Low']; close = df['Close']
    resistance = high.rolling(20).max().iloc[-1]
    support = low.rolling(20).min().iloc[-1]
    current_close = close.iloc[-1]
    is_breakout = current_close > resistance * 1.005
    if not is_breakout and current_close >= resistance:
        is_breakout = True
        breakout_strength = (current_close / support - 1) * 100
    else:
        breakout_strength = (current_close / resistance - 1) * 100 if is_breakout else 0
    return {
        'resistance': resistance,
        'support': support,
        'is_breakout': is_breakout,
        'breakout_strength': breakout_strength
    }

def detect_chart_pattern(df):
    close = df['Close']; high = df['High']; low = df['Low']
    recent_high = high.iloc[-10:].max()
    recent_low = low.iloc[-10:].min()
    range_width = (recent_high - recent_low) / recent_high * 100 if recent_high > 0 else 100
    lows_rising = low.iloc[-10:].is_monotonic_increasing
    highs_flat = (high.iloc[-10:].max() - high.iloc[-10:].min()) / high.iloc[-10:].mean() * 100 < 3 if high.iloc[-10:].mean() > 0 else False
    if range_width < 10 and close.iloc[-1] > close.iloc[-5]:
        return "🚩 Bullish Flag"
    elif lows_rising and highs_flat and close.iloc[-1] > high.iloc[-2]:
        return "📐 Ascending Triangle"
    elif close.iloc[-1] > close.iloc[-5] * 1.05 and high.iloc[-1] > high.iloc[-2]:
        return "📈 Momentum Breakout"
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
            pos = ['naik','melesat','rekor','laba','dividen','ekspansi','akuisisi']
            neg = ['turun','anjlok','rugi','utang','krisis','skandal']
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

def analisis_super(kode, df):
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
        macd_df = ta.macd(df['Close'], fast=12, slow=26, signal=9)
        df['MACD'] = macd_df['MACD_12_26_9']
        df['MACD_signal'] = macd_df['MACDs_12_26_9']
        
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
        
        mf = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
        mf = mf.fillna(0)
        cmf = mf.rolling(21).mean().iloc[-1]
        adl = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low']) * df['Volume']
        adl = adl.cumsum()
        adl_trend = adl.iloc[-1] - adl.iloc[-21] if len(adl) >= 21 else 0
        
        ma50_val = df['MA50'].iloc[-1]
        if pd.isna(ma50_val):
            ma50_display = "N/A (data < 50 hari)"
        else:
            ma50_display = f"Rp{ma50_val:.0f}"
        
        skor_teknikal = 0
        if harga > df['MA20'].iloc[-1]:
            skor_teknikal += 10
        if not pd.isna(df['MA50'].iloc[-1]) and df['MA20'].iloc[-1] > df['MA50'].iloc[-1]:
            skor_teknikal += 5
        if volume_spike > 2.0:
            skor_teknikal += 15
        elif volume_spike > 1.5:
            skor_teknikal += 8
        if 50 <= rsi <= 70:
            skor_teknikal += 10
        elif 70 < rsi <= 75:
            skor_teknikal += 7
        elif 40 <= rsi < 50:
            skor_teknikal += 5
        if df['MACD'].iloc[-1] > df['MACD_signal'].iloc[-1]:
            skor_teknikal += 5
        if perubahan > 0:
            skor_teknikal += 5
        
        skor_money = 0
        if cmf > 0.1:
            skor_money += 25
        elif cmf > 0:
            skor_money += 15
        elif cmf < -0.1:
            skor_money -= 10
        if adl_trend > 0:
            skor_money += 15
        else:
            skor_money -= 5
        if volume_spike > 2.0 and cmf > 0:
            skor_money += 10
        elif volume_spike > 1.5 and cmf > 0:
            skor_money += 5
        
        skor_total = skor_teknikal + skor_money
        if skor_total < 0:
            skor_total = 0
        
        if cmf > 0.1 and adl_trend > 0:
            money_status = "🔥 Smart Money + (Akumulasi Kuat)"
        elif cmf > 0 and adl_trend > 0:
            money_status = "🟢 Smart Money + (Akumulasi)"
        elif cmf < -0.1 and adl_trend < 0:
            money_status = "🔴 Smart Money - (Distribusi)"
        else:
            money_status = "⚪ Netral"
        
        if skor_total >= 70:
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
            'ma50_display': ma50_display,
            'volume': int(vol_hari),
            'volume_spike': round(volume_spike, 1),
            'volume_bandar': volume_bandar,
            'support': round(snr['support'], 2),
            'resistance': round(snr['resistance'], 2),
            'is_breakout': snr['is_breakout'],
            'breakout_strength': round(snr['breakout_strength'], 2),
            'pattern': pattern,
            'sentimen': sentimen_label,
            'cmf': round(cmf, 3),
            'adl_trend': round(adl_trend, 2),
            'money_status': money_status,
            'skor_teknikal': skor_teknikal,
            'skor_money': skor_money,
            'skor_total': skor_total,
            'signal': signal,
            'rekom': rekom,
            'entry': entry,
            'sl': sl,
            'tp1': tp1,
            'tp2': tp2,
        }
    except Exception as e:
        print(f"❌ Error {kode}: {e}")
        return None

# ========== MAIN ==========
wita = pytz.timezone('Asia/Makassar')
waktu_str = datetime.now(wita).strftime('%d-%m-%Y %H:%M')
print(f"🚀 SUPER SCREENER (TEKNIKAL + MONEY FLOW) - {waktu_str}")

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

batch_size = 30
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
            period="120d",
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
    
    delay = random.uniform(3, 6)
    print(f"⏳ Jeda {delay:.1f} detik sebelum batch berikutnya...")
    time.sleep(delay)

print(f"✅ Total berhasil di-download: {len(all_data)} saham")

semua_hasil = []
for kode in LIST_SAHAM:
    if kode not in all_data or all_data[kode].empty:
        continue
    df = all_data[kode].copy()
    res = analisis_super(kode, df)
    if res:
        semua_hasil.append(res)

semua_hasil.sort(key=lambda x: x['skor_total'], reverse=True)
potensial = [h for h in semua_hasil if h['skor_total'] >= 70]
pantauan = [h for h in semua_hasil if 50 <= h['skor_total'] < 70]

print(f"✅ Berhasil menganalisis {len(semua_hasil)} saham.")

pesan = f"🌟 SUPER SCREENER (TEKNIKAL + MONEY FLOW)\n"
pesan += f"📅 {waktu_str} WITA\n"
pesan += f"📌 Total: {len(semua_hasil)} saham | 🔥 Potensial: {len(potensial)}\n"
pesan += "=" * 30 + "\n\n"

if potensial:
    pesan += "🔥 SAHAM POTENSIAL (SKOR ≥ 70)\n\n"
    for h in potensial[:10]:
        pesan += f"🏢 {h['kode']} - {h['nama']}\n"
        pesan += f"💰 Rp{h['harga']:.0f} | 📈 {h['perubahan']:+.2f}% | ⭐ Skor: {h['skor_total']}\n"
        pesan += f"   Teknikal: {h['skor_teknikal']}/50 | Money: {h['skor_money']}/50\n"
        pesan += f"📊 RSI: {h['rsi']} | MA20: Rp{h['ma20']:.0f} | MA50: {h['ma50_display']}\n"
        pesan += f"📦 Vol: {h['volume']:,} | Spike: {h['volume_spike']}x | Bandar: {'✅' if h['volume_bandar'] else '❌'}\n"
        pesan += f"📐 S: Rp{h['support']:.0f} | R: Rp{h['resistance']:.0f} | Breakout: {'✅' if h['is_breakout'] else '❌'} ({h['breakout_strength']:.1f}%)\n"
        pesan += f"📈 Pattern: {h['pattern']}\n"
        pesan += f"{h['sentimen']}\n"
        pesan += f"💰 CMF: {h['cmf']} | ADL: {h['adl_trend']:.0f}\n"
        pesan += f"🕵️ {h['money_status']}\n"
        pesan += f"💡 Strategi: {h['rekom']}\n"
        if h['sl'] is not None:
            pesan += f"🔴 SL: Rp{h['sl']:.0f} | 🟢 TP1: Rp{h['tp1']:.0f} | 🟢 TP2: Rp{h['tp2']:.0f}\n"
        pesan += "-" * 25 + "\n"
else:
    pesan += "⏳ Belum ada saham dengan skor ≥ 70 hari ini.\n\n"

if pantauan:
    pesan += "📊 PANTAUAN (Skor 50-69)\n"
    for h in pantauan[:5]:
        pesan += f"🔹 {h['kode']} | Skor: {h['skor_total']} | Tek: {h['skor_teknikal']} | Money: {h['skor_money']} | RSI: {h['rsi']} | Rp{h['harga']:.0f}\n"

kirim_pesan(pesan)
print("✅ Selesai! Cek Telegram.")
