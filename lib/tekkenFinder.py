import urllib.request
import os
from bs4 import BeautifulSoup

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
  move_Attribute_Dict = dict()
  
  is_move_found = 0

  chara_Move = chara_Move.replace(" ", "")
  chara_Move = chara_Move.replace("/", "")

  charSpecSoup = charPage_BS4_Setup(chara_Page_FileName)

  for table_row in charSpecSoup.select("table tr"):
    moveAttribute_Cells = table_row.findAll('td')

    cell_move_compare = moveAttribute_Cells[0].text
    cell_move_compare = cell_move_compare.replace(" ", "")
    cell_move_compare = cell_move_compare.replace("/", "")

    if (is_case_sensitive == 0):
      if chara_Move.lower() == cell_move_compare.lower():
        is_move_found = 1

    elif (is_case_sensitive == 1):
      if chara_Move == cell_move_compare:
        is_move_found = 1

    if (is_move_found == 1):     

      print('MOVE FOUND= ' + cell_move_compare)
      print("======================")

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

      break
  return move_Attribute_Dict

def get_Misc_Chara_Details(chara_Name):
  chara_WebUrl = charFullUrlDict[chara_Name]
  chara_ImgurPortrait = charImgurDict[chara_Name]

  misc_chara_details_dict = {'char_name': chara_Name,
                             'char_url' : chara_WebUrl,
                             'char_imgur' : chara_ImgurPortrait
                              }

  return misc_chara_details_dict
