import time
import json
import httplib
import logging
import database

logging.basicConfig(filename='logs/cron.log', level=logging.DEBUG)

collections = [
    [ 
      {
        'name': 'EDSA1',       
        'nodes': [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
      }
    ],
    [ 
      {'name': 'EDSA2',       'nodes': [32,34,35,37]},
      {'name': 'Mrcs Hwy',    'nodes': [110,112,114]},
      {'name': 'Espana',      'nodes': [65,67,69,71]},
    ],
    [
      {'name': 'QAve',        'nodes': [39,41,43,45,47,49,51,55,57,59,61,63]},
      {'name': 'SLEX',        'nodes': [93,141,96]},
    ],
    [
      {'name': 'C5',          'nodes': [73,75,77,79,131,133,135,137,139]},
      {'name': 'Cmnwlth',     'nodes': [99,101,103,105,107]},
    ],
    [
      {'name': 'Ortgs',       'nodes': [117,119,121,123,125,127,129]},
      {'name': 'Cstal Rd',    'nodes': [82,84,86,88,89,91]},
    ],
]

names = {
      1: u"Bltwk",
      2: u"Kaingn",
      3: u"Munoz",
      4: u"Bnslngn",
      5: u"NrthAve",
      6: u"Trnoma",
      7: u"QAve",
      8: u"NIA",
      9: u"Timg",
     10: u"Kmning",
     11: u"NwYrk",
     12: u"MntDPied",
     13: u"Aurora",
     14: u"Frmrs",
     15: u"P.Tuazn",
     16: u"MainAve",
     17: u"Sntoln",
     18: u"WytPlains",
     19: u"Ortgs",
     20: u"Mgamll",
     21: u"Shaw",
     22: u"Rliance",
     23: u"Pioneer",
     24: u"Guadlupe",
     25: u"Ornse",
     26: u"Klyaan",
     27: u"Buendia",
     28: u"Ayla",
     29: u"Arnaiz",
     30: u"Mgllans",
     31: u"Mlibay",
     32: u"Tramo",
     33: u"Taft",
     34: u"FBHrrson",
     35: u"Roxas",
     36: u"Mcpgl",
     37: u"MOA",
     38: u"Phlcoa",
     39: u"QCrcle",
     40: u"Agham",
     41: u"Bntyog",
     42: u"Edsa",
     43: u"Esgera",
     44: u"Albno",
     45: u"Brrmeo",
     46: u"Sntiago",
     47: u"Tmog",
     48: u"Reyes",
     49: u"Mgbnua",
     50: u"Roces",
     51: u"Roosvlt",
     52: u"Grcia",
     53: u"Chuatoco",
     54: u"G Arnta",
     55: u"StDmngo",
     56: u"BiaknBto",
     57: u"Bnawe",
     58: u"Crdllera",
     59: u"DTuazn",
     60: u"Spkr Perez",
     61: u"Apo",
     62: u"Knlaon",
     63: u"Mayon",
     64: u"Lerma",
     65: u"PNoval",
     66: u"Lcson",
     67: u"VcntCruz",
     68: u"Antipolo",
     69: u"AMceda",
     70: u"Blmntrit",
     71: u"WRtnda",
     72: u"Lbis",
     73: u"Eastwd",    
     74: u"GrnMdws",
     75: u"Ortgas",
     76: u"JVrgs",
     77: u"Lnuza",
     78: u"BgongIlg",
     79: u"Klayaan",
     80: u"MktMkt",
     81: u"CstlRd",
     82: u"AirptRd",
     83: u"Bclrn",
     84: u"EdsaExt",
     85: u"Buendia",
     86: u"POcmpo",
     87: u"Quirno",
     88: u"RjSlyman",
     89: u"UNAve",
     90: u"FnanceRd",
     91: u"AndaCircl",
     92: u"AlabngExt",
     93: u"SucatExt",
     94: u"BcutnExt",
     95: u"MervlExt",
     96: u"Nicols",
     97: u"Mgllnes",
     98: u"Batasn",
     99: u"StPeter",
    100: u"Ever",
    101: u"DlimanPrep",
    102: u"Zzuaregi",
    103: u"GenMalvar",
    104: u"T.Sora E",
    105: u"T.Sora W",
    106: u"Central",
    107: u"Mgsysy",
    108: u"UnivAve",
    109: u"SnBenildo",
    110: u"Rbnson Metro",
    111: u"FMriano",
    112: u"AmangRdrgez",
    113: u"DonaJuana",
    114: u"LRT2 Stn",
    115: u"SM Mrkina",
    116: u"Sntolan",
    117: u"Mdison",
    118: u"Roosvlt",
    119: u"ClbnFilpno",
    120: u"Wilsn",
    121: u"Cnnctcut",
    122: u"LaSalle",
    123: u"POEA",
    124: u"EDSAShrine",
    125: u"SnMig Ave",
    126: u"Mralco Ave",
    127: u"MedCty",
    128: u"Lnuza",
    129: u"GrnMdws",
    130: u"C5Flyvr",
    131: u"TSora",
    132: u"Cpitol Hlls",
    133: u"UP",
    134: u"CPGarcia",
    135: u"Mriam",
    136: u"Atneo",
    137: u"Xavervill",
    138: u"Aurora",
    139: u"PTuazon",
    140: u"BSerrano",
    141: u"C5Ramp",
    142: u"PdroGil",
}

def nice(x):
	# Conjecture: 4 is better than 5.
    x = int(x)
    if x == 0:
    	return '?'
    if x == 1:
        return 'L'
    elif x == 2 or x == 3:
        return 'M'
    elif x == 4 or x == 5:
        return 'H'
    else:
        return '?'

def load(domain='mmdatraffic.interaksyon.com', path='/data.traffic.status.php'):
    data = None
    for x in xrange(0, 10):
        logging.debug('Loading page... %s%s'%(domain, path))
        conn = httplib.HTTPConnection(domain)
        conn.request('GET', path)
        resp = conn.getresponse()

        if resp.status == 200:
            data = resp.read()
            conn.close()
            break
        else:
            logging.warning('Error loading page: (%d) %s' % (resp.status, resp.reason))
            time.sleep(3)
    else:
        logging.error('Gave up loading page.')
        return None

    logging.debug('Finished loading!')
    parsed = json.loads(data)
    sane = [{'street': int(arr[0][0]), 'id': int(arr[0][1]), 'fore': nice(arr[1][0]), 'back': nice(arr[2][0])} for arr in parsed]
    nodes = {}
    for n in sane:
        nodes[n['id']] = n

    return nodes

def generate_messages():
    nodes = load()
    if nodes is None:
        return None
    logging.debug('Got traffic data')

    messages = []
    for pk, collection in enumerate(collections):
        strings = []
        for street in collection:
            strings.append(street['name'])
            for n in street['nodes']:
                name = names[n]
                node = nodes[n]
                temp = "%s-%s%s"%(name, node['fore'], node['back'])
                strings.append(temp.strip())
            strings.append('\n')
        message = '\n'.join(strings).strip()
        messages.append({'pk': pk, 'data': message})
        print message, '\n'
    logging.debug('Generated messages!')
    return messages

if __name__ == '__main__':
    messages = generate_messages()
    if messages is None:
        logging.error('Could not write messages.')

    connection = database.Connection()
    connection.initialize(messages)
    connection.update_messages(messages)
    logging.debug('Finished updating messages')
