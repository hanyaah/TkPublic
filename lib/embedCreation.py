import discord
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from random import randint

def embed_Move_Details(char_name, char_url, char_moveIcon, char_imgur, char_move, char_hitLevel, char_dmg, char_startup, char_block, char_hit, char_counterhit, char_notes):
    #I can live with this for now.
    #If values are null, use placeholder value to prevent Bad Request errors when sending message
    if not char_dmg:
      char_dmg = '-'
    if not char_startup:
      char_startup = '-'
    if not char_block:
      char_block = '-'
    if not char_hit:
      char_hit = '-'
    if not char_counterhit:
      char_counterhit = '-'
    if not char_notes:
      char_notes = '-'

    #convert shorthand to full character names for display
    if(char_name == 'raven'):
        char_name = 'Master Raven'
    if(char_name == 'chloe'):
        char_name = 'Lucky Chloe'
    if(char_name == 'dvj'):
        char_name = 'Devil Jin'

    embed = discord.Embed(title= char_name.title() + " Frame Data (RBNorway)", 
                          colour=discord.Colour(0x6342FC), 
                          url=char_url, 
                          description="**Move: " + char_move + "**\n" + char_moveIcon)

    embed.set_thumbnail(url=char_imgur)                                         
    embed.set_author(name= char_name.title(), url=char_url, icon_url="https://i.imgur.com/9YWQdwE.jpg")
    embed.add_field(name="Property", value= char_hitLevel)
    embed.add_field(name="Damage", value= char_dmg)
    embed.add_field(name="Startup", value= 'i' + char_startup)
    embed.add_field(name="Block", value= char_block)
    embed.add_field(name="Hit", value= char_hit)
    embed.add_field(name="Counter Hit", value= char_counterhit)
    embed.add_field(name="Notes", value= char_notes)

    return embed

def embed_Similar_Moves(similar_Moves_List, char_name, char_url, char_imgur):
  embed = discord.Embed(title= char_name.title() + " Frame Data (RBNorway)", 
                        colour=discord.Colour(0xFF5733), 
                        url=char_url, 
                        description="**Move Not Found.**")
  embed.set_thumbnail(url=char_imgur)
  embed.set_author(name= char_name.title(), url=char_url, icon_url="https://i.imgur.com/9YWQdwE.jpg")

  moveList = ''
  if (len(similar_Moves_List) == 0):
    moveList = 'No similar moves found.'
  for moveNum, move in enumerate(similar_Moves_List):
    if moveNum <9:
      moveList = moveList + move + '\n'

  embed.add_field(name='Similar moves', value=moveList)
  
  return embed

def embed_early2017(early2017Str, timeLeft):
    opkick_Emote = '<:OPKICK:306556200626159616>'
    lul_Emote = '<:LUL:306533696826245120>'
    xdcr_Emote = '<:XDCR:306542128010625035>'
    gudTimes_Emote = '<:GoodTime4Fans:308593805362462721>'
    leeGasm_Emote = '<:Leegasm:306554217533800448>'
    murray_Emote = '<:tgMurray:309301734205816833>'
    portrait_num = randint(0,4)
    if portrait_num == 1:
        thumbnailEmote = 'https://i.imgur.com/FMqJijI.png?1'
    elif portrait_num == 2:
        thumbnailEmote = 'http://i.imgur.com/8pLMgGv.png'
    elif portrait_num == 3:
        thumbnailEmote = 'https://i.imgur.com/iMtrObh.png'
    elif portrait_num == 4:
        thumbnailEmote = 'https://i.imgur.com/YNjuCFA.png'

    pre_days_left = str(timeLeft.days)
    pre_hours_left = str(timeLeft.hours)
    pre_minutes_left = str(timeLeft.minutes)

    digitNumList = ["0","1", "2", "3","4","5","6","7","8","9"]
    wordNumList = [":zero:", ":one:", ":two:", ":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"]

    numConversionDict = {}
    for i in range(len(digitNumList)):
        numConversionDict[digitNumList[i]] = wordNumList[i]

    days_left = ''
    for digit in pre_days_left:
        for digitNum in numConversionDict:
            if digit == digitNum:
                days_left = days_left + numConversionDict[digitNum]

    hours_left = ''
    for digit in pre_hours_left:
        for digitNum in numConversionDict:
            if digit == digitNum:
                hours_left = hours_left + numConversionDict[digitNum]

    minutes_left = ''
    for digit in pre_minutes_left:
        for digitNum in numConversionDict:
            if digit == digitNum:
                minutes_left = minutes_left + numConversionDict[digitNum]

    embed = discord.Embed(title= "Time Until" + gudTimes_Emote + " :regional_indicator_e::regional_indicator_a::regional_indicator_r::regional_indicator_l::regional_indicator_y:" + gudTimes_Emote+
                                 ":two::zero::one::seven:" + gudTimes_Emote,
                          colour=discord.Colour(0xf4427a),
                          url='http://early2017.com',
                          description= '**' + early2017Str + '**')
    embed.add_field(name= xdcr_Emote + murray_Emote + days_left + "➖" + " 🇩🇦🇾🇸" + murray_Emote + xdcr_Emote, value= '-')
    embed.add_field(name= gudTimes_Emote + opkick_Emote + hours_left + "➖" + "  🇭🇴🇺:regional_indicator_r:🇸" + opkick_Emote + gudTimes_Emote, value='-')
    embed.add_field(name= leeGasm_Emote + lul_Emote+ minutes_left + "➖"+ "  🇲:regional_indicator_i:🇳:regional_indicator_u:🇹🇪:regional_indicator_s:" + lul_Emote + leeGasm_Emote, value='-')
    embed.set_thumbnail(url=thumbnailEmote)
    return embed