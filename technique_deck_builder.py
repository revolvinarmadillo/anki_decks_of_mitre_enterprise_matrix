import genanki
import random
import requests

#Function to loop through content in individual techniques; looking for attack patterns covering main techniques (subtechniques excluded via 'not in' check, since subtechnique ids are formatted to be TX.X where X are numerical values)
def main_technique_parsing(technique, techniques):
    tactics = []
    for reference in technique['external_references']:
        if 'external_id' in reference:
            if ((reference['external_id'].startswith("T")) and '.' not in reference['external_id']):
                if 'kill_chain_phases' in technique:
                    for tactic in technique['kill_chain_phases']:
                        tactics.append(tactic['phase_name'])
                technique = reference['external_id']
                name = object['name']
                url = reference['url']

                if ((object['x_mitre_deprecated'] == False) or ('x_mitre_deprecated' not in object)):
                    filtered_object = {'tactics': str(tactics), 'technique': technique, 'name': name, 'url': url}
                    techniques.append(filtered_object)

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
technique_deck = genanki.Deck(deck_id, 'MITRE ATT&CK Enterprise - Techniques')

url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

headers = {
    'accept': 'application/json'
}

mitre_data = requests.get(url, headers=headers).json()

#This will be a list of dictionary objects (each list entry is going to be a 'technique' dictionary)
techniques = []

#Looping through attack-pattern json objects in returned json document with a focus on techniques that are not listed as revoked; parsing and addition of technique dictionary objects to techniques python list handled by main_technique_parsing function
for object in mitre_data['objects']:
    if object['type'] == 'attack-pattern':
        if 'external_references' in object:
            if 'revoked' in object:
                if object['revoked'] == False: 
                    main_technique_parsing(object, techniques)
            else:
                main_technique_parsing(object, techniques)


for x in range(0,len(techniques)):
    frontstr = techniques[x]['technique'] + " - technique name? (Optional: Tactic(s) it is mapped to?)"
    backstr = techniques[x]['name'] + "<br>Tactics - " + techniques[x]['tactics'] + "<br>Link: " + techniques[x]['url']
    curr_note = genanki.Note(model=basic_model, fields=[frontstr,backstr])
    technique_deck.add_note(curr_note)

genanki.Package(technique_deck).write_to_file('mitre_enterprise_techniques.apkg')
