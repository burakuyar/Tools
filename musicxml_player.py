import xml.etree.ElementTree as ET
import winsound as w
import time
from lxml import etree
from io import StringIO, BytesIO

#koma definitions
#flats
b_koma = 'quarter-flat' #'flat-down'
b_bakiyye = 'slash-flat'
b_kmucennep = 'flat'
b_bmucennep = 'double-slash-flat'

#sharps
d_koma = 'slash-quarter-sharp'
d_bakiyye = 'sharp'
d_kmucennep = ''
d_bmucennep = 'slash-sharp'

#frequency dictionary
freqdict = {'__': 0 ,'A3': 220 ,'B3': 248, 'C4': 261, 'D4': 294, 'E4': 330, 'F4': 348,
		'G4' : 391,	'A4' : 440,	'B4' : 495,	'C5' : 522, 'D5' : 587, 'E5' : 660, 'F5' : 695, 'G5' : 782, 'A5' : 880, 'B5': 990}

def getKeySig():

	#file = 'sertan_senturk\SymbTr_to_musicXML\SymbTr2_TXT_corrected\zirefkend--pesrev--agirdarbifetih----gazi_giray_han.xml'
	#file = 'sertan_senturk\SymbTr_to_musicXML\SymbTr2_TXT_corrected\hicaz--sarki--nimsofyan--gonul_penceresinden--muzaffer_ilkar.xml'
	#file = 'sertan_senturk\SymbTr_to_musicXML\SymbTr2_TXT_corrected\segah--turku--nimsofyan--silifkenin_yogurdu--.xml'
	#file = 'sertan_senturk\SymbTr_to_musicXML\SymbTr2_TXT_corrected\segah--turku--aksak--beyaz_giyme--bolu.xml'
	file = 'symbtr2/SymbTr2_Latest/txt_for_dotted_and_tuplets/segah--turku--nimsofyan--silifkenin_yogurdu--.xml'
	
	tree = ET.parse(file)
	root = tree.getroot()
	print(root.tag)
	
	bpm = float(root.find('part/measure/direction/sound').attrib['tempo'])
	divs = float(root.find('part/measure/attributes/divisions').text)
	qnotelen = 60000/bpm
	
	durs = []
	pitches = []
	accs = []
	for note in root.findall('part/measure/note'):
		dur = note.find('duration').text
		try:
			step = note.find('pitch/step').text
			oct = note.find('pitch/octave').text
		except:
			step = '_'
			oct = '_'
			print('Cannot get pitch info.')
		try:
			acc = note.find('accidental').text
			if type(acc) == type(None) : acc = 0
			elif acc == b_koma: acc = -1
			elif acc == b_bakiyye: acc = -4
			elif acc == b_kmucennep: acc = -5
			elif acc == b_bmucennep: acc = -8
			
			elif acc == d_koma: acc = +1
			elif acc == d_bakiyye: acc = +4
			elif acc == d_kmucennep: acc = +5
			elif acc == d_bmucennep: acc = +8
		except:
			print('Cannot get accidental info.')
			acc = 0

		#print(dur)
		durs.append(int(qnotelen*float(dur)/divs))
		pitches.append(step + oct)
		accs.append(acc)
		
	print(durs, len(durs))
	print(pitches, len(pitches))
	print(accs, len(accs))
	print('BPM:', bpm)
	print('divs:', divs)
	'''
	w.Beep(1000,500)
	w.Beep(2000,500)
	w.Beep(3000,500)
	w.Beep(4000,500)
	'''
	x = 0
	for i in range(0, len(durs)):
		#tempdur = int(qnotelen*durs[i]/divs)
		
		''' old version
		if pitches[i] == 'A3' : freq = 440
		elif pitches[i] == 'B3' : freq = 493
		elif pitches[i] == 'C4' : freq = 523
		elif pitches[i] == 'D4' : freq = 587
		elif pitches[i] == 'E4' : freq = 659
		elif pitches[i] == 'F4' : freq = 698
		elif pitches[i] == 'G4' : freq = 783
		elif pitches[i] == 'A4' : freq = 880
		elif pitches[i] == 'B4' : freq = 987
		elif pitches[i] == 'C5' : freq = 1046
		elif pitches[i] == 'D5' : freq = 1174
		elif pitches[i] == 'E5' : freq = 1318
		elif pitches[i] == 'F5' : freq = 1396
		elif pitches[i] == 'G5' : freq = 1567
		elif pitches[i] == 'A5' : freq = 1760
		'''
		#new version
		freq = freqdict[pitches[i]]
		if accs[i] != 0:
			freq *= 2**(accs[i]/53)
		if freq == 0:
			time.sleep(durs[i]/1000)
		else:
			w.Beep(int(freq), durs[i])
		x += 1
		#print(durs[i] , pitches[i], freq)
	print(x)
	
		

x = getKeySig()