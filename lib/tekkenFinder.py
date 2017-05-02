import urllib.request
import os
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#self-created modules below
import lib.notationToEmoji as notationToEmoji

charaImageLinks = open("lib/characterImageList.txt", 'r')
charaImageLines = charaImageLinks.read().splitlines()

charaDataFile = open("lib/characterList.txt", 'r')
charaLines = charaDataFile.read().splitlines()

#declare dictionaries
charLocalPageDict = dict()
charFullUrlDict = dict()
charImgurDict = dict()

#Create Dictionaries for referring to locally stored webpages  
for lines in charaLines:
    charVar = lines.split(",")
    charLocalPageDict[charVar[0]] = charVar[0] + '.html'
    charFullUrlDict[charVar[0]] = charVar[1]

#Create dictionary for imgur urls of character images, used in embed thumbnails
for lines in charaImageLines:
    charImg = lines.split(",")
    charImgurDict[charImg[0]] = charImg[1]


def does_char_exist(user_Chara_Name):
  doesCharacterExist = 0
  for characterName in charLocalPageDict:
    
    if user_Chara_Name.lower() == characterName:
      print("\n======================")
      print("Chara Found: " + user_Chara_Name)
      doesCharacterExist = 1

      break

  return doesCharacterExist

def charPage_BS4_Setup(chara_Name):
  #Setup webpages for parsing by Beautiful Soup
  #Get current working directory
  dirStr = os.getcwd()

  charFilePath = 'file:///'+ dirStr + '/webpages/' + chara_Name

  #Create the soup...thing? What kinda data type is created anyway?
  charSpecific = urllib.request.urlopen(charFilePath).read()
  charPageSoup = BeautifulSoup(charSpecific, "html.parser")

  return charPageSoup

def get_Move_Details(chara_Name, chara_Move, is_case_sensitive):
  chara_Page_FileName = charLocalPageDict[chara_Name]
  chara_Move = move_Input_Standardizer(chara_Move) 
  charSpecSoup = charPage_BS4_Setup(chara_Page_FileName)
  soup_NumOfRows = len(charSpecSoup.find_all("tr"))
  move_Attribute_Dict = dict()

  table_row_iteration = 0
  for table_row in charSpecSoup.select("table tr"):
    moveAttribute_Cells = table_row.findAll('td')

    cell_move_compare = moveAttribute_Cells[0].text
    cell_move_compare = move_Input_Standardizer(cell_move_compare)

    is_move_found = move_Comparer(chara_Move, cell_move_compare, is_case_sensitive)

    if (is_move_found == 1):     
      print('MOVE FOUND= ' + cell_move_compare)
      print("======================")

      move_Attribute_Dict = move_Attr_Dict_Creator(moveAttribute_Cells)
      break

    table_row_iteration +=1

  if (table_row_iteration == soup_NumOfRows and is_move_found == 0):
    print('Move not found, commencing fuzzy matching')
    for table_row in charSpecSoup.select("table tr"):
      moveAttribute_Cells = table_row.findAll('td')

      cell_move_compare = moveAttribute_Cells[0].text
      cell_move_compare = move_Input_Standardizer(cell_move_compare)

      is_move_found = compare_Move_Substring(chara_Move, cell_move_compare)

      if (is_move_found == 1):
        move_Attribute_Dict = move_Attr_Dict_Creator(moveAttribute_Cells)
        break
      # matchRatio = get_Fuzzy_Match_Ratio(chara_Move, cell_move_compare)
      # if matchRatio == 100:
      #   is_move_found = 1
      #   print('POSSIBLE MATCH FOUND= ' + cell_move_compare)
      #   print("======================")
      #   move_Attribute_Dict = move_Attr_Dict_Creator(moveAttribute_Cells)
      #   break

  return move_Attribute_Dict

def get_Misc_Chara_Details(chara_Name):
  #misc character details used in embed display
  chara_WebUrl = charFullUrlDict[chara_Name]
  chara_ImgurPortrait = charImgurDict[chara_Name]

  misc_chara_details_dict = {'char_name': chara_Name,
                             'char_url' : chara_WebUrl,
                             'char_imgur' : chara_ImgurPortrait
                              }

  return misc_chara_details_dict

def compare_Move_Substring(user_move, cell_move):
  if user_move in cell_move:
    is_move_found = 1
    return is_move_found

#moves are too short and too similar to fuzz, remove later
def get_Fuzzy_Match_Ratio(user_move, cell_move):
  tokenRatio = fuzz.token_set_ratio(user_move, cell_move)
  print('Token Ratio: ', tokenRatio)
  return tokenRatio

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

  standardized_move = move_input

  return standardized_move

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

def move_Comparer(chara_Move, cell_move_compare, is_case_sensitive):
  is_move_found = 0

  if (is_case_sensitive == 0):
      if chara_Move.lower() == cell_move_compare.lower():
        is_move_found = 1

  elif (is_case_sensitive == 1):
      if chara_Move == cell_move_compare:
        is_move_found = 1

  return is_move_found