import genanki
import json
import random
import requests

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
            'afmt': '{{Answer}}',
        }
    ],
    css='.card {\n font-family: arial;\n font-size: 20px;\n}\n')

#Making the Anki deck
tactic_deck = genanki.Deck(deck_id, 'MITRE ATT&CK Enterprise - Tactics')

# Place url and headers back here from original mitre.py when ready
url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

headers = {
    'accept': 'application/json'
}

#Place request.get part after = from original mitre.py when ready
mitre_data = requests.get(url, headers=headers).json()

url_list = []
tactic_names = []
tactic_names_bp = []
tactic_IDs = []

for object in mitre_data['objects']:
    if object['type'] == 'x-mitre-matrix':
        if 'tactic_refs' in object:
            for tactic_ref in object['tactic_refs']:
                url = "https://raw.githubusercontent.com/mitre/cti/refs/heads/master/enterprise-attack/x-mitre-tactic/" + tactic_ref + ".json"
                url_list.append(url)

for url in url_list:
    headers = {'accept': 'application/json'}
    tactic_obj = requests.get(url, headers=headers).json()
    for object in tactic_obj['objects']:
        tactic_names.append(object['name'])
        for items in object['external_references']:
            tactic_IDs.append(items['external_id'])

for tactic in tactic_names:
    tactic_name_bp = "<li>" + tactic + "<br></li>"
    tactic_names_bp.append(tactic_name_bp)

#Making first Anki note be all tactics listed in bullet point order
combined_ans = "<ul>" + "".join(tactic_names_bp) + "</ul>"
first_note = genanki.Note(model=basic_model, fields=['List out the current ATT&CK enterprise tactics in sequential order:',combined_ans])
tactic_deck.add_note(first_note)

#Making remaining Anki notes be the individual TA numbers in order; requires user to answer with tactic name
tactic_len=len(tactic_names)
for x in range(0,tactic_len):
    frontstr = tactic_IDs[x] + " - ???"
    curr_note = genanki.Note(model=basic_model, fields=[frontstr,tactic_names[x]])
    tactic_deck.add_note(curr_note)

genanki.Package(tactic_deck).write_to_file('mitre_enterprise_tactics.apkg')
