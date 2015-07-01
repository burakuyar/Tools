# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import winsound as w
import time
from lxml import etree
from io import StringIO, BytesIO
from audiolazy import *

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

#mansur nısfiyesi
#frequency dictionary
freqdict = {'__': 0 ,'A3': 220 ,'B3': 247, 'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349,
		'G4' : 392,	'A4' : 440,	'B4' : 493,	'C5' : 523, 'D5' : 587, 'E5' : 659, 'F5' : 698, 'G5' : 783, 'A5' : 880, 'B5': 988}

def getKeySig():

	#file = 'sertan_senturk\SymbTr_to_musicXML\SymbTr2_TXT_corrected\zirefkend--pesrev--agirdarbifetih----gazi_giray_han.xml'
	file = 'sertan_senturk\SymbTr_to_musicXML\SymbTr2_TXT_corrected\hicaz--sarki--nimsofyan--gonul_penceresinden--muzaffer_ilkar.xml'
	#file = 'sertan_senturk\SymbTr_to_musicXML\SymbTr2_TXT_corrected\segah--turku--nimsofyan--silifkenin_yogurdu--.xml'
	#file = 'sertan_senturk\SymbTr_to_musicXML\SymbTr2_TXT_corrected\segah--turku--aksak--beyaz_giyme--bolu.xml'
	tree = ET.parse(file)
	root = tree.getroot()
	#print(root.tag)
	
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
		
	#print(durs, len(durs))
	#print(pitches, len(pitches))
	#print(accs, len(accs))
	print('BPM:', bpm)
	print('divs:', divs)
	'''
	w.Beep(1000,500)
	w.Beep(2000,500)
	w.Beep(3000,500)
	w.Beep(4000,500)
	'''
	rate = 44100 # Sampling rate, in samples/second
	s, Hz = sHz(rate) # Seconds and hertz
	ms = 1e-3 * s
	notes = []
	totaltime = 0
	
	x = 0
	for i in range(0, len(durs)):
		#new version
		freq = freqdict[pitches[i]]
		if accs[i] != 0:
			freq *= 2**(accs[i]/53.0)

		#print(totaltime, freq)
		###########
		tempnote = zeros(totaltime).append(karplus_strong(freq * Hz))
		totaltime += durs[i] * ms
		if i == 0:
			notes = tempnote * 0.8
		else:
			notes += (tempnote * 0.8)
		###########
		'''
		notes.append(zeros(totaltime * ms).append(karplus_strong(int(freq) * Hz)))
		totaltime += durs[i]
		'''
		x += 1
		#print(durs[i] , pitches[i], freq)
	#print(x, len(notes))
	#print(notes)
	
	sound = notes.take(2 * s)
	with AudioIO(True) as player:
		player.play(sound, rate=rate)
	
	#print(totaltime)
	
getKeySig()