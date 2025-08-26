import genanki
import random
import requests

#Looping through content in individual techniques; looking for attack patterns covering main techniques (subtechniques excluded via 'not in' check, since subtechnique ids are formatted to be TX.X where X are numerical values)
def main_technique_parsing(technique_obj, techniques):
    tactics = []
    for reference in technique_obj['external_references']:
        if 'external_id' in reference:
            if ((reference['external_id'].startswith("T")) and '.' not in reference['external_id']):
                if 'kill_chain_phases' in technique_obj:
                    for tactic in technique_obj['kill_chain_phases']:
                        tactics.append(tactic['phase_name'])
                technique = reference['external_id']
                name = object['name']
                url = reference['url']

                if ((object['x_mitre_deprecated'] == False) or ('x_mitre_deprecated' not in object)):
                    filtered_object = {'tactics': str(tactics), 'technique': technique, 'name': name, 'url': url}
                    techniques[technique] = filtered_object

#Function to loop through content in individual techniques; looking for attack patterns covering subtechniques (since subtechnique ids are formatted to be TX.X where X are numerical values)
def sub_technique_parsing(technique_obj, subtechniques):
    tactics = []
    for reference in technique_obj['external_references']:
        if 'external_id' in reference:
            if ((reference['external_id'].startswith("T")) and '.' in reference['external_id']):
                if 'kill_chain_phases' in technique_obj:
                    for tactic in technique_obj['kill_chain_phases']:
                        tactics.append(tactic['phase_name'])
                subtechnique = reference['external_id']
                name = object['name']
                url = reference['url']

                if ((object['x_mitre_deprecated'] == False) or ('x_mitre_deprecated' not in object)):
                    filtered_object = {'tactics': str(tactics), 'subtechnique': subtechnique, 'name': name, 'url': url}
                    subtechniques.append(filtered_object)

#Generating random Anki note model ID and deck ID per genanki's documentation recommendations
model_id = random.randrange(1 << 30, 1 << 31)
deck_id = random.randrange(1 << 30, 1 << 31)

#Making an Anki Note Model based on genanki documentation 
#(Also, custom css gathered from basic (genanki) model example from builtin_models.py  at https://github.com/kerrickstaley/genanki ; in the genanki directory)
basic_model = genanki.Model(
    model_id,
    'Basic - Front and Bank',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        }
    ],
    css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n}\n')


#Making the Anki deck
technique_deck = genanki.Deck(deck_id, 'MITRE ATT&CK® Matrix for Enterprise - Sub-techniques')

url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

headers = {
    'accept': 'application/json'
}

mitre_data = requests.get(url, headers=headers).json()

#This will be a dictionary of technique objects (each dictionary entry is going to be a main technique with a technique id key used to make it accessible)
techniques = {}

#This will be a list of dictionary objects (each list entry is going to be a 'subtechnique' dictionary)
subtechniques = []

#Looping through attack-pattern json objects in returned json document with a focus on techniques that are not listed as revoked; parsing and addition of technique dictionary items to techniques dictionary handled by main_technique_parsing function
for object in mitre_data['objects']:
    if object['type'] == 'attack-pattern':
        if 'external_references' in object:
            if 'revoked' in object:
                if object['revoked'] == False: 
                    main_technique_parsing(object, techniques)
            else:
                main_technique_parsing(object, techniques)

#Looping through attack-pattern json objects again in returned json document with a focus on subtechniques that are not listed as revoked; parsing and addition of subtechnique dictionary objects to subtechniques list handled by sub_technique_parsing function
for object in mitre_data['objects']:
    if object['type'] == 'attack-pattern':
        if 'external_references' in object:
            if 'revoked' in object:
                if object['revoked'] == False: 
                    sub_technique_parsing(object, subtechniques)
            else:
                sub_technique_parsing(object, subtechniques)

for x in range(0, len(subtechniques)):
    splitstr=subtechniques[x]['subtechnique'].split('.')
    main_technique=splitstr[0]
    frontstr = subtechniques[x]['subtechnique'] + " - Sub-technique name? (Optional: Main technique and tactic(s) it is mapped to?)"
    backstr = subtechniques[x]['name'] + "<br><br>Main Technique it is a part of - " + techniques[main_technique]["name"] + "<br>Tactics - " + subtechniques[x]['tactics'] + "<br>Link: " + subtechniques[x]['url']
    curr_note = genanki.Note(model=basic_model, fields=[frontstr,backstr])
    technique_deck.add_note(curr_note)

genanki.Package(technique_deck).write_to_file('mitre_enterprise_subtechniques.apkg')
