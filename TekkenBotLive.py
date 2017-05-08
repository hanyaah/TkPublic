import discord
import asyncio
import aiohttp
from discord.ext import commands

#self-created modules below
import lib.embedCreation as embedCreation #contains functions for creating an embed
import lib.tekkenFinder as tekkenFinder   #contains functions for finding character and move details

#Nothing to see here, move along
tokenFile = open("token.txt", 'r')
token = tokenFile.read()

client = discord.Client()

@client.event
async def on_ready():
    #Display Login Status in Console
    print('<---------------------------->')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('<---------------------------->')
    await client.change_presence(game=discord.Game(name='you like a damn fiddle'))

@client.event
async def on_message(message):
    if message.content.startswith('!'):
        if message.content.startswith('!!'):
          case_sensitive_toggle = 1
        else:
          case_sensitive_toggle = 0

        #message content should look like this
        #![character] [move]

        userMessage = message.content
        userMessage = userMessage.replace("!", "")
        user_message_list = userMessage.split(" ", 1)

        if len(user_message_list) <= 1:
          print('! command used, but character not found/move not given\n')
          return

        user_Chara_Name = user_message_list[0]
        user_Chara_Move = user_message_list[1]

        characterExists = tekkenFinder.does_char_exist(user_Chara_Name)

        if characterExists == 1:
          move_attribute_dict = tekkenFinder.get_Move_Details(user_Chara_Name, 
                                                              user_Chara_Move, 
                                                              case_sensitive_toggle)

          if bool (move_attribute_dict): #if dictionary not empty, move found
            misc_details_Dict = tekkenFinder.get_Misc_Chara_Details(user_Chara_Name)
            embedDict = {**move_attribute_dict, **misc_details_Dict}
            embed_MoveFound = embedCreation.embed_Move_Details(**embedDict)

            await client.send_message(message.channel, embed=embed_MoveFound)
            return

          else: #dictionary is empty, move not found  
            misc_details_Dict = tekkenFinder.get_Misc_Chara_Details(user_Chara_Name)
            similar_moves_list = tekkenFinder.get_Similar_Moves(user_Chara_Name, user_Chara_Move)
            embed_SimilarMoves = embedCreation.embed_Similar_Moves(similar_moves_list, **misc_details_Dict)

            await client.send_message(message.channel, embed = embed_SimilarMoves)
            return

        elif characterExists == 0:
          await client.send_message(message.channel, 'Character not found: ' + '**' + user_Chara_Name + '**')

    elif message.content.startswith('.help'):
        await help_Message(message) 

    elif message.content.startswith('.early2017'):
        await client.send_message(message.channel,
                                     'X DAYS UNTIL EARLY 2017')

    elif message.content.startswith('.stfuCombot'):
    	await gag_Combot(message)

async def help_Message(message):
	await client.send_message(message.channel,'Ping <@Hann> for any questions/suggestions/bug reports.\n'
                            +'Commands: '
                            +'```'
                            +'![charname] [notation] or !![charname] [notation] \n'
                            +'Eg: !kazuya f,n,d,df+2 or !!kazuya f,n,d,DF+2'
                            +'```'
                            +'Notable Character Names: Use dvj for deviljin, jack for Jack7, raven for Master Raven, and chloe for Lucky Chloe.'                                    
                            +'\n'
                            +'**Use double exclamation marks (!!) for case-sensitive search.**\n'
                            +'All frame data is sourced from RBNorway.org.')

# Permissions is borked, checking out bot 
@commands.has_permissions(administrator=True) 
async def gag_Combot(message):
	channel = message.channel.id
	await client.send_message(message.channel, 'mmmph! Gagging combot. Channel ID is: ' + channel)
	#TODO: Implement actual gagging later
	

#Starts the bot
client.run(token)