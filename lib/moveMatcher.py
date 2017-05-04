from fuzzywuzzy import fuzz
from collections import OrderedDict
from operator import itemgetter

#Self Created Modules Below
import lib.notationToEmoji as notationToEmoji

def move_Compare_Main(chara_Move, charSpecSoup, is_case_sensitive):
  chara_Move = move_Input_Standardizer(chara_Move)

  MatchAttempts = 0
  while (MatchAttempts <2):
    for table_row in charSpecSoup.select("table tr"):
      moveAttribute_Cells = table_row.findAll('td')

      cell_move_compare = moveAttribute_Cells[0].text
      cell_move_compare = move_Input_Standardizer(cell_move_compare)

      if(MatchAttempts == 0):
        is_move_found = move_Compare_Strict(chara_Move, cell_move_compare, is_case_sensitive)
      else: #1:1 match failed, attempting substring match
        is_move_found = move_Compare_Substring(chara_Move, cell_move_compare, is_case_sensitive)

      if (is_move_found == 1):     
        print('MOVE FOUND= ' + cell_move_compare)
        print("======================")

        move_Attribute_Dict = move_Attr_Dict_Creator(moveAttribute_Cells)
        return move_Attribute_Dict

    MatchAttempts +=1

  return None

def move_Compare_Strict(chara_Move, cell_move_compare, is_case_sensitive):
  is_move_found = 0

  if (is_case_sensitive == 0):
      if chara_Move.lower() == cell_move_compare.lower():
        is_move_found = 1

  elif (is_case_sensitive == 1):
      if chara_Move == cell_move_compare:
        is_move_found = 1

  return is_move_found

def move_Compare_Substring(user_move, cell_move, is_case_sensitive):
  is_move_found = 0

  if(is_case_sensitive == 0):
    if user_move.lower() in cell_move.lower():
      is_move_found = 1
      return is_move_found
  else:
    if user_move in cell_move:
      is_move_found = 1
      return is_move_found

def move_Compare_Similar(user_Move, charSpecSoup):
  similar_moves_dict = dict()
  user_Move = move_Input_Standardizer(user_Move)

  for table_row in charSpecSoup.select("table tr"):
      moveAttribute_Cells = table_row.findAll('td')

      cell_move_compare = moveAttribute_Cells[0].text
      cell_move_compare = move_Input_Standardizer(cell_move_compare)

      similarity = fuzz.ratio(user_Move, cell_move_compare)
      
      similar_moves_dict[moveAttribute_Cells[0].text] = similarity

  similar_moves_list = sorted(similar_moves_dict, key=similar_moves_dict.__getitem__, reverse=True)
  moves_Added = 0

  short_similar_moves_list = []
  for move in similar_moves_list:
    if moves_Added <9:
      short_similar_moves_list.append(move)
      moves_Added +=1
    else:
      break

  return short_similar_moves_list

def move_Input_Standardizer(move_input):
  #remove spaces and slashes
  move_input = move_input.replace(" ", "")
  move_input = move_input.replace("/", "")

  #translate WR moves into f,f,f
  if move_input[:2].lower() == 'wr':
    move_input = move_input.replace('wr', 'f,f,f+')
    move_input = move_input.replace('WR', 'f,f,f+')
  if move_input[:2].lower() == 'ws' and move_input[2] != '+':
    move_input = move_input.replace('ws', 'ws+')
    move_input = move_input.replace('WS', 'ws+')
  if move_input[:2].lower() == 'fc' and move_input[2] != '+':
    move_input = move_input.replace('fc', 'fc+')
    move_input = move_input.replace('FC', 'FC+')
  if move_input[:2].lower() == 'cd':
    move_input = move_input.replace('cd', 'f,n,d,df+')
    move_input = move_input.replace('CD', 'f,n,d,df+')

  return move_input

def move_Attr_Dict_Creator(moveAttribute_Cells):
  move_Attribute_Dict = dict()
  move_Attribute_Dict['char_move'] = moveAttribute_Cells[0].text
  move_Attribute_Dict['char_hitLevel'] = moveAttribute_Cells[1].text
  move_Attribute_Dict['char_dmg'] = moveAttribute_Cells[2].text
  move_Attribute_Dict['char_startup'] = moveAttribute_Cells[3].text
  move_Attribute_Dict['char_block'] = moveAttribute_Cells[4].text
  move_Attribute_Dict['char_hit'] = moveAttribute_Cells[5].text
  move_Attribute_Dict['char_counterhit'] = moveAttribute_Cells[6].text
  move_Attribute_Dict['char_notes'] = moveAttribute_Cells[7].text
  move_Attribute_Dict['char_moveIcon'] = notationToEmoji.icon_move_processor(moveAttribute_Cells[0].text)

  return move_Attribute_Dict