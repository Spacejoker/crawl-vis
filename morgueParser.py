from flask import jsonify
import re

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

weapon_skills = ['Fighting', 'Short Blades', 'Long Blades', u'Maces & Flails', 'Axes', 'Polearms', 'Unarmed Combat', 'Staves', 'Bows','Throwing', 'Crossbows', 'Slings']
magic_schools = [ 'Spellcasting', 'Conjurations', 'Hexes', 'Charms', 'Summonings', 'Necromancy', 'Translocations', 'Transmutations', 'Fire Magic', 'Ice Magic', 'Air Magic', 'Earth Magic', 'Poison Magic']
defensive_schools = [ 'Armour', 'Dodging', 'Stealth', 'Shields', u'Traps', 'Stabbing', 'Invocations', 'Evocations']


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

	def parse(self, morgueText):
		
		all_skills = weapon_skills + magic_schools + defensive_schools
		level_map = {}
		species = ""
		background = ""
		species_short = ""
		background_short = ""
		current_level = 1
		level_skills = [[0 for y in xrange(len(all_skills))] for x in xrange(28)]
		victorious = False
		xl = 1
		total_turns = 0
		title = ""
		shopping_list = []

		#extract data from text file
		for line, text in enumerate(morgueText.split("\n")):

			text = text.strip()


			if "Escaped with the Orb" in text:
				victorious = True

			if( "Reached XP level" in text):
				match = re.search("\\d+", text)

				if(match != None):

					turns = match.group()

					second_half = text.split("Reached XP level")[1]
					level = re.search("\\d+", second_half).group()
					level_map[level] = turns
					current_level = int(level)
					xl = max(xl, int(level))

			#Extract which species and background that is used
			if "Began as a " in text :
				species, species_short = self.get_from_cands(text, all_species)
				background, background_short = self.get_from_cands(text, all_backgrounds)

				print species, "(" + species_short + ")"
				print background, "(" + background_short + ")"
	
			if "reached skill level" in text.lower():

				match = re.search("\\d+", text)
				t = match.group()
				second_half = text.split("Reached skill level")[1]
				skill_level = re.search("\\d+", second_half).group()
				skill_type = ""
				skill_id = -1

				for _id, skill in enumerate(all_skills):
					if skill in second_half:
						skill_type = skill
						skill_id = _id

				if skill_type != "":
					level_skills[current_level][skill_id] = int(skill_level)

				print skill_type, "to", skill_level, "id is", skill_id, "at turn", t, "(currently level", current_level, ")"
			if "Turns: " in text:
				title = text.split("Turns")[0]
				total_turns = int(re.search("\\d+", text.split("Turns")[1]).group())
			if "Bought" in text:
				shopping_list.append(text)

		if victorious:
			result = "Win"
		else:
			result = "Death"

		for level in range(1, 28):
			for skill_id in xrange(len(all_skills)):
				level_skills[level][skill_id] = max(level_skills[level-1][skill_id], level_skills[level][skill_id])
			
		return { 'species' : species,
				'species_short' : species_short,
				'background' : background,
				'background_short' : background_short,
				'level_map' : level_map,
				'weapon_data' : level_skills,
				'weapon_names' : all_skills,
				'XL' : xl,
				'total_turns' : total_turns,
				'title' : title,
				'result' : result,
				'nr_of_skills' : len(level_skills),
				'shopping_list' : shopping_list}

if __name__ == '__main__':
	pass

