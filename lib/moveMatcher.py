from fuzzywuzzy import fuzz
from collections import OrderedDict
from operator import itemgetter

#Self Created Modules Below
import lib.notationToEmoji as notationToEmoji

def move_Compare_Main(chara_Move, jsonconvert, is_case_sensitive, chara_Name):
  chara_Move = move_Input_Standardizer(chara_Move)
  found = list(filter(lambda x: (x['Command'] == chara_Move) , jsonconvert))
  #assuming one is found
  newdict = {
              "Command": found[0]['Command'],
              "Hit level": found[0]['Hit level'],
              "Damage": found[0]['Damage'],
              "Start up frame": found[0]['Start up frame'],
              "Block frame": found[0]['Block frame'],
              "Hit frame": found[0]['Hit frame'],
              "Counter hit frame": found[0]['Counter hit frame'],
              "Notes": found[0]['Notes']                        
             }   
  convert = move_Attr_Dict_Creator(newdict, chara_Name)
  #chara_Name = charSpecSoup.find("h2", {"class":"title"})
  #chara_Name = chara_Name.text.replace(' T7 Frames','')

  #MatchAttempts = 0
  #while (MatchAttempts <2):
  #  for table_row in charSpecSoup.select("table tr"):
  #    moveAttribute_Cells = table_row.findAll('td')

  #    cell_move_compare = moveAttribute_Cells[0].text
  #    cell_move_compare = move_Input_Standardizer(cell_move_compare)

  #    if(MatchAttempts == 0):
  #      is_move_found = move_Compare_Strict(chara_Move, cell_move_compare,
  #      is_case_sensitive)
  #    else: #1:1 match failed, attempting substring match
  #      is_move_found = move_Compare_Substring(chara_Move, cell_move_compare,
  #      is_case_sensitive)

  #    if (is_move_found == 1):
  #      print('MOVE FOUND= ' + cell_move_compare)
  #      print("======================")

  #      move_Attribute_Dict =
  #      move_Attr_Dict_Creator(moveAttribute_Cells,chara_Name)
  #      return move_Attribute_Dict

  #  MatchAttempts +=1
  #function returns None if no matches found
  return convert

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
    if moves_Added < 9:
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