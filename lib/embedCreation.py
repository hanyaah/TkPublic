import discord

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

  print('MoveList: ' + moveList)
  embed.add_field(name='Similar moves', value=moveList)
  
  return embed