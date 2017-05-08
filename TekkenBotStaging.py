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

description = 'Evil Bot World Domination!'

prefix = '.'

bot = commands.Bot(command_prefix=prefix, description=description)

@bot.event
async def on_ready():
    #Display Login Status in Console
    print('<---------------------------->')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('<---------------------------->')
    await bot.change_presence(game=discord.Game(name='you like a damn fiddle'))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

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

            await bot.send_message(message.channel, embed=embed_MoveFound)
            return

          else: #dictionary is empty, move not found  
            misc_details_Dict = tekkenFinder.get_Misc_Chara_Details(user_Chara_Name)
            similar_moves_list = tekkenFinder.get_Similar_Moves(user_Chara_Name, user_Chara_Move)
            embed_SimilarMoves = embedCreation.embed_Similar_Moves(similar_moves_list, **misc_details_Dict)

            await bot.send_message(message.channel, embed=embed_SimilarMoves)
            return

        elif characterExists == 0:
          await bot.say('Character not found: ' + '**' + user_Chara_Name + '**')

    await bot.process_commands(message)

@bot.command()
async def early2017():
    await client.send_message(message.channel, 'X DAYS UNTIL EARLY 2017')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True) 
async def gagcombot(ctx):
	channel = ctx.message.channel.id
	await bot.say('mmmph! Gagging Combot. Channel ID is: ' + channel)
	#TODO: Implement actual gagging later	

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True) 
async def ungagcombot(ctx):
    channel = ctx.message.channel
    await bot.say('Ungagged Combot. Channel ID is: ' + channel)
    #TODO: Implement actual ungagging later

@bot.command()
async def printServers(ctx):
    if ctx.author.id != ('99090187560173568')
    # ctx.author.id
    serverListStr = ''
    for server in bot.servers:
        serverListStr = serverListStr + server + '\n'
    await bot.say('Server List ' + channel)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await bot.send_message(ctx.message.channel, "You don't have permissions to run this!")

#Starts the bot
bot.run(token)