import urllib.request
import os
import json
from bs4 import BeautifulSoup

#self-created modules below
import lib.moveMatcher as moveMatcher

#======================================================
#=======Should probably put this stuff in a module=====
#======================================================
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
#======================================================
#====END Should probably put this stuff in a module====
#======================================================
def does_char_exist(user_Chara_Name):
  doesCharacterExist = 0

  for characterName in charLocalPageDict:
    if user_Chara_Name.lower() == characterName:
      print("\n======================")
      print("Chara Found: " + user_Chara_Name)
      doesCharacterExist = 1
      break

  return doesCharacterExist


def charJson(chara_Name):
  dirStr = os.getcwd()
  charFilePath = 'file:///' + dirStr + '/webpages/' + chara_Name
  name = chara_Name.replace(".html", "")
  jsonFilePath = dirStr + '/json/' + name + '.json'

    
  try:
        if os.path.isfile(jsonFilePath): #if path exists
            file = open(jsonFilePath, 'r')
            content = file.read()
            jsonconvert = json.loads(content)
            print(type(jsonconvert))
        else:
            charSpecific = urllib.request.urlopen(charFilePath).read()      
            charPageSoup = BeautifulSoup(charSpecific, "html.parser")
            table = charPageSoup.table
            row = table.find_all('tr')
            dic = []
            for index in row:
               col = index.find_all('td')
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
              
               dic.append(addmove)
            
            file = open(jsonFilePath, 'w')
            json.dump(dic, file)
            #Probably have better way of doing
            file = open(jsonFilePath, 'r')
            content = file.read()
            jsonconvert = json.loads(content)
  except IOError as e:
    print(e)
  
  return jsonconvert

def charPage_BS4_Setup(chara_Name):
  
  charPageSoup = charJson(chara_Name)

  return charPageSoup

def get_Move_Details(chara_Name, chara_Move, is_case_sensitive):
  chara_Page_FileName = charLocalPageDict[chara_Name]
  charSpecSoup = charPage_BS4_Setup(chara_Page_FileName)

  move_Attribute_Dict = moveMatcher.move_Compare_Main(chara_Move, charSpecSoup, is_case_sensitive, chara_Name)

  if not move_Attribute_Dict:
    print('MOVE NOT FOUND: ' + chara_Move)
    print("======================")
  return move_Attribute_Dict

def get_Similar_Moves(chara_Name, chara_Move):
  chara_Page_FileName = charLocalPageDict[chara_Name]
  charSpecSoup = charPage_BS4_Setup(chara_Page_FileName)

  similar_Moves_List = moveMatcher.move_Compare_Similar(chara_Move, charSpecSoup)
  return similar_Moves_List

def get_Misc_Chara_Details(chara_Name):
  #misc character details used in embed display
  chara_WebUrl = charFullUrlDict[chara_Name]
  chara_ImgurPortrait = charImgurDict[chara_Name]

  misc_chara_details_dict = {'char_url' : chara_WebUrl,
                             'char_imgur' : chara_ImgurPortrait
                              }

  return misc_chara_details_dict