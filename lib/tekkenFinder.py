import urllib.request
import os
import json
import pprint
from bs4 import BeautifulSoup

# self-created modules below
import lib.moveMatcher as moveMatcher

# character misc details
chara_misc_file = open('json/character_misc.json', 'r')
content = chara_misc_file.read()
chara_misc_details_json = json.loads(content)


def does_char_exist(user_Chara_Name):
    chara_details_dict = list(filter(lambda x: (x['name'] == user_Chara_Name), chara_misc_details_json))

    if chara_details_dict:
        print("\n======================")
        print("Chara Found: " + user_Chara_Name)
        return True
    else:
        return False

def charJsonMassConverter():
    # json folder must be empty of character jsons to work properly
    for game_character in chara_misc_details_json:
        charUrl = game_character['name'] + '.html'
        get_charJson(charUrl)


def get_charJson(chara_Name):
    dirStr = os.getcwd()
    charFilePath = 'file:///' + dirStr + '/webpages/' + chara_Name
    name = chara_Name.replace(".html", "")
    jsonFilePath = dirStr + '/json/' + name + '.json'

    try:
        if os.path.isfile(jsonFilePath):  # if path exists
            file = open(jsonFilePath, 'r')
            content = file.read()
            jsonconvert = json.loads(content)
        else:
            charSpecific = urllib.request.urlopen(charFilePath).read()
            charPageSoup = BeautifulSoup(charSpecific, "html.parser")
            moveAttribute_List_of_Dicts = []

            for table_row in charPageSoup.select("table tr"):
                col = table_row.find_all('td')

                addmove = {
                    "Command": col[0].text,
                    "Hit level": col[1].text,
                    "Damage": col[2].text,
                    "Start up frame": col[3].text,
                    "Block frame": col[4].text,
                    "Hit frame": col[5].text,
                    "Counter hit frame": col[6].text,
                    "Notes": col[7].text
                }

                if addmove["Command"] == "Command":
                    continue

                for key in addmove:
                    if addmove[key] == "":
                        addmove[key] = "-"

                moveAttribute_List_of_Dicts.append(addmove)

            file = open(jsonFilePath, 'w')
            json.dump(moveAttribute_List_of_Dicts, file, indent=4)

            # Probably have better way of doing
            file = open(jsonFilePath, 'r')
            content = file.read()
            jsonconvert = json.loads(content)
    except IOError as e:
        print(e)

    return jsonconvert


def get_Move_Details(chara_Name, chara_Move, is_case_sensitive):
    chara_details_dict = list(filter(lambda x: (x['name'] == chara_Name), chara_misc_details_json))
    charMoves_json = get_charJson(chara_details_dict[0]['local_webpage'])

    move_Attribute_Dict = moveMatcher.move_Compare_Main(chara_Move, charMoves_json, is_case_sensitive, chara_Name)

    if not move_Attribute_Dict:
        print('MOVE NOT FOUND: ' + chara_Move)
        print("======================")
        return False
    else:
        print('MOVE  FOUND: ' + chara_Move)
        print("======================")
        return move_Attribute_Dict


def get_Similar_Moves(chara_Name, chara_Move):
    chara_details_dict = list(filter(lambda x: (x['name'] == chara_Name), chara_misc_details_json))
    charMoves_json = get_charJson(chara_details_dict[0]['local_webpage'])

    similar_Moves_List = moveMatcher.move_Compare_Similar(chara_Move, charMoves_json)
    return similar_Moves_List


def get_Misc_Chara_Details(chara_Name):
    # misc character details used in embed display
    chara_details_dict = list(filter(lambda x: (x['name'] == chara_Name), chara_misc_details_json))

    misc_chara_details_dict = {'char_url': chara_details_dict[0]['online_webpage'],
                               'char_imgur': chara_details_dict[0]['portrait']
                               }

    return misc_chara_details_dict
