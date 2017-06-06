from fuzzywuzzy import fuzz

# Self Created Modules Below
import lib.notationToEmoji as notationToEmoji


def move_Compare_Main(chara_Move, characterMoves_json, is_case_sensitive, chara_Name):
    chara_Move = move_Input_Standardizer(chara_Move)
    if is_case_sensitive:
        move = list(filter(lambda x: (move_Input_Standardizer(x['Command']) == chara_Move), characterMoves_json))
    else:
        move = list(filter(lambda x: (move_Input_Standardizer(x['Command'].lower()) == chara_Move.lower()),
                           characterMoves_json))

    if not move:
        # if Move not found, look for substring match
        move = list(filter(lambda x: (chara_Move.lower() in move_Input_Standardizer(x['Command'].lower())),
                           characterMoves_json))

    if not move:
        # if move still not found, return None
        return None
    else:
        moveDict = {
            "Command": move[0]['Command'],
            "Hit level": move[0]['Hit level'],
            "Damage": move[0]['Damage'],
            "Start up frame": move[0]['Start up frame'],
            "Block frame": move[0]['Block frame'],
            "Hit frame": move[0]['Hit frame'],
            "Counter hit frame": move[0]['Counter hit frame'],
            "Notes": move[0]['Notes']
        }

        convert = move_Attr_Dict_Creator(moveDict, chara_Name)
        return convert


def move_Compare_Similar(user_Move, chara_json):
    user_Move = move_Input_Standardizer(user_Move.lower())
    moves_Added = 0
    similar_moves_dict = dict()

    for mov in chara_json:
        move_notation = str(mov['Command'])
        standardized_move_notation = move_Input_Standardizer(move_notation)
        similarity = fuzz.ratio(user_Move, standardized_move_notation.lower())

        similar_moves_dict[move_notation] = similarity

    similar_moves_list = sorted(similar_moves_dict, key=similar_moves_dict.__getitem__, reverse=True)

    short_similar_moves_list = []
    for move in similar_moves_list:
        if moves_Added < 9:
            short_similar_moves_list.append(move)
            moves_Added += 1
        else:
            break

    return short_similar_moves_list


def move_Input_Standardizer(move_input):
    # remove spaces and slashes
    move_input = move_input.replace(" ", "")
    move_input = move_input.replace("/", "")

    # translate shorthand into full notation
    if move_input[:2].lower() == 'wr' and move_input[2] != '+':
        move_input = move_input.lower().replace('wr', 'f,f,f+')
    if move_input[:2].lower() == 'ss' and move_input[2] != '+':
        move_input = move_input.lower().replace('ss', 'ss+')
    if move_input[:2].lower() == 'ws' and move_input[2] != '+':
        move_input = move_input.lower().replace('ws', 'ws+')
    if move_input[:2].lower() == 'fc' and move_input[2] != '+':
        move_input = move_input.lower().replace('fc', 'fc+')
    if move_input[:2].lower() == 'cd' and move_input[2] != '+':
        move_input = move_input.lower().replace('cd', 'f,n,d,df+')
    if move_input[:3].lower() == 'qcf' and move_input[2] != '+':
        move_input = move_input.lower().replace('qcf', 'qcf+')
    return move_input


def move_Attr_Dict_Creator(moveAttribute_Cells, chara_Name):
    move_Attribute_Dict = dict()
    move_Attribute_Dict['char_name'] = chara_Name.lower().replace(' ', '_')
    move_Attribute_Dict['char_move'] = moveAttribute_Cells['Command']
    move_Attribute_Dict['char_hitLevel'] = moveAttribute_Cells['Hit level']
    move_Attribute_Dict['char_dmg'] = moveAttribute_Cells['Damage']
    move_Attribute_Dict['char_startup'] = moveAttribute_Cells['Start up frame']
    move_Attribute_Dict['char_block'] = moveAttribute_Cells['Block frame']
    move_Attribute_Dict['char_hit'] = moveAttribute_Cells['Hit frame']
    move_Attribute_Dict['char_counterhit'] = moveAttribute_Cells['Counter hit frame']
    move_Attribute_Dict['char_notes'] = moveAttribute_Cells['Notes']
    move_Attribute_Dict['char_moveIcon'] = notationToEmoji.icon_move_processor(moveAttribute_Cells['Command'])
    return move_Attribute_Dict
