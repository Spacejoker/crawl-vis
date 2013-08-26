import urllib2
import re
from flask import Flask, render_template

app = Flask(__name__)

class MorgueData():
	def __init__(self, path):
		self.path = path
	
	def set_level_turns(self, turns):
		self.level_turns = turns

all_species = """Human - Hu
High elf - HE
Deep elf - DE
Sludge elf - SE
Deep Dwarf - DD
Hill Orc - HO
Merfolk - Mf
Halfling - Ha
Kobold - Ko
Spriggan - Sp
Naga - Na
Centaur - Ce
Ogre - Og
Troll - Tr
Minotaur - Mi
Tengu - Te
Draconian - Dr
Demonspawn - Ds
Demigod - Dg
Mummy - Mu
Ghoul - Gh
Vampire - Vp
Felid - Fe
Octopode - Op"""

all_backgrounds = """
Fighter - Fi
Gladiator - Gl
Monk - Mo
Hunter - Hu
Assassin - As
Artificer - Ar
Wanderer - Wn
Berserker - Be
Abyssal Knight - AK
Chaos Knight - CK
Death Knight - DK
Priest - Pr
Healer - He
Skald - Sk
Transmuter - Tm
Warper - Wr
Arcane Marksman - AM
Enchanter - En
Stalker - St
Wizard - Wz
Conjurer - Cj
Summoner - Su
Necromancer - Ne
Fire Elementalist - FE
Ice Elementalist - IE
Air Elementalist - AE
Earth Elementalist - EE
Venom Mage - VM
"""

class MorgueParser():
	def __init__(self, version=12):
		self.version = version

	def get_from_cands(self, text, candidates):
		a = ""
		b = ""
		for cand in candidates.split("\n"):
			spec = cand.split('-')
			if len(spec) < 2: continue
				
			if spec[0].strip() in text:
				a = spec[0].strip()
				b = spec[1].strip()
		return a, b

	def parse(self, morgueText, morgueData):
		
		level_map = {}
		species = ""
		background = ""
		species_short = ""
		background_short = ""

		#extract data from text file
		for line, text in enumerate(morgueText.split("\n")):

			text = text.strip()

			if( "Reached XP level" in text):
				match = re.search("\\d+", text)

				if(match != None):

					turns = match.group()

					second_half = text.split("Reached XP level")[1]
					level = re.search("\\d+", second_half).group()
					level_map[level] = turns

			#Extract which species and background that is used
			if "Began as a " in text :
				species, species_short = self.get_from_cands(text, all_species)
				background, background_short = self.get_from_cands(text, all_backgrounds)

				print species, "(" + species_short + ")"
				print background, "(" + background_short + ")"
			
		morgueData.level_map = level_map

@app.route('/')
def hello_world(morgue=None):
	url = 'http://rl.heh.fi/morgue//nago/morgue-nago-20130825-110603.txt'
	response = urllib2.urlopen(url)
	html = unicode(response.read(), 'utf-8')

	data = {u'name' : u'jens', u'c' : u'' }
	morgueData = MorgueData(url)
	MorgueParser().parse(html, morgueData)

	return render_template('morgue.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

