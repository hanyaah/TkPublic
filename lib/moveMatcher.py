from fuzzywuzzy import fuzz
from collections import OrderedDict
from operator import itemgetter

#Self Created Modules Below
import lib.notationToEmoji as notationToEmoji

def FuzMatch(userInput, moves, ratio):
  founds = fuzz.ratio(userInput, moves)
  print(founds)
  return founds > ratio

def move_Compare_Main(chara_Move, characterMoves_json, is_case_sensitive, chara_Name):
  chara_Move = move_Input_Standardizer(chara_Move)
  if is_case_sensitive == 0:
    move = list(filter(lambda x: (move_Input_Standardizer(x['Command'].lower()) == chara_Move.lower()), characterMoves_json))
  else:
    move = list(filter(lambda x: (move_Input_Standardizer(x['Command']) == chara_Move), characterMoves_json))

  if(move == []):
    #if Move not found, look for substring match
    move = list(filter(lambda x: (chara_Move.lower() in move_Input_Standardizer(x['Command'].lower())), characterMoves_json))

  if (move == []):
    #if move still not found, return None
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

def move_Compare_Similar(user_Move, jsonconvert):
  user_Move = move_Input_Standardizer(user_Move.lower())

  moves_Added = 0
  #found = list(filter(lambda x: (FuzMatch(user_Move,move_Input_Standardizer(x['Command']), 0)) , jsonconvert))
  compare = list()
  for mov in jsonconvert:
      move_notation = str(mov['Command'])
      move_notation = move_Input_Standardizer(move_notation)
      rat = fuzz.ratio(user_Move,move_notation)
     
      kV = {
          "Command" : move_notation,
          "Similarity" : rat
          }
      compare.append(kV)

  compare = bubble(compare)
  short_similar_moves_list = []
  for i, item in enumerate(compare):
    if moves_Added < 9:
      short_similar_moves_list.append(compare[i]['Command'])
      moves_Added +=1
    else:
      break

  return short_similar_moves_list

def bubble(lst, asc=False):
    lst = list(lst)  # copy collection to list
    for passesLeft in range(len(lst)-1, 0, -1):
        for i in range(passesLeft):
            if asc:
                if lst[i]['Similarity'] > lst[i + 1]['Similarity']:
                    lst[i]['Similarity'], lst[i + 1]['Similarity'] = lst[i + 1]['Similarity'], lst[i]['Similarity']
                    lst[i]['Command'], lst[i + 1]['Command'] = lst[i + 1]['Command'], lst[i]['Command']
            else:
                if lst[i]['Similarity'] < lst[i + 1]['Similarity']:
                    lst[i]['Similarity'], lst[i + 1]['Similarity'] = lst[i + 1]['Similarity'], lst[i]['Similarity']
                    lst[i]['Command'], lst[i + 1]['Command'] = lst[i + 1]['Command'], lst[i]['Command']
    return lst


def move_Input_Standardizer(move_input):
  #remove spaces and slashes
  move_input = move_input.replace(" ", "")
  move_input = move_input.replace("/", "")

  #translate shorthand into full notation
  if move_input[:2].lower() == 'wr' and move_input[2] != '+':
    move_input = move_input.replace('wr', 'f,f,f+')
    move_input = move_input.replace('WR', 'f,f,f+')
  if move_input[:2].lower() == 'ws' and move_input[2] != '+':
    move_input = move_input.replace('ws', 'ws+')
    move_input = move_input.replace('WS', 'ws+')
  if move_input[:2].lower() == 'fc' and move_input[2] != '+':
    move_input = move_input.replace('fc', 'fc+')
    move_input = move_input.replace('FC', 'FC+')
  if move_input[:2].lower() == 'cd' and move_input[2] != '+':
    move_input = move_input.replace('cd', 'f,n,d,df+')
    move_input = move_input.replace('CD', 'f,n,d,df+')
  if move_input[:3].lower() == 'qcf' and move_input[2] != '+':
    move_input = move_input.replace('qcf', 'qcf+')
    move_input = move_input.replace('QCF', 'qcf+')
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
  move_Attribute_Dict['char_moveIcon'] =  notationToEmoji.icon_move_processor(moveAttribute_Cells['Command'])
  return move_Attribute_Dict