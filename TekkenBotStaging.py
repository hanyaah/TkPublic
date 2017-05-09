import discord
import asyncio
import aiohttp
import logging
from discord.ext import commands

#self-created modules below
import lib.embedCreation as embedCreation #contains functions for creating an embed
import lib.tekkenFinder as tekkenFinder   #contains functions for finding character and move details

#Nothing to see here, move along
tokenFile = open("token.txt", 'r')
token = tokenFile.read()

description = 'Tekken 7 Frame Data Bot!'

prefix = '.'

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='combot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

bot = commands.Bot(command_prefix=prefix, description=description)

combot_gagged_channels_File = open("lib/gagged_channels.txt", 'r')
combot_gagged_channels = combot_gagged_channels_File.read().splitlines()

@bot.event
async def on_ready():
    #Display Login Status in Console
    print('<---------------------------->')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('<---------------------------->')
    await bot.change_presence(game=discord.Game(name='you like a damn fiddle || .help'))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content != '.ungagcombot':
        print('not ungagging combot')
        for channelID in combot_gagged_channels:
            if message.channel.id == channelID:
                print('This channel is gagged')
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
          return

    await bot.process_commands(message)
    print('Processed Commands.')

@bot.command(pass_context=True)
async def early2017():
    print('Early 2017 function')
    await bot.say('X DAYS UNTIL EARLY 2017')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True) 
async def gagcombot(ctx):
    channel = ctx.message.channel.id
    f = open("lib/gagged_channels.txt","a")
    f.write(channel + '\n')
    f.close()

    combot_gagged_channels.append(channel)

    await bot.say('mmmph! Gagging Combot. Channel ID is: ' + channel)
    #TODO: Implement actual gagging later   

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True) 
async def ungagcombot(ctx):
    channel = ctx.message.channel
    combot_gagged_channels.remove(channel)
    #clear file contents
    open("lib/gagged_channels.txt","w").close()

    f = open("lib/gagged_channels.txt","a")
    for channel in combot_gagged_channels:
        f.write(channel+'\n')
    f.close()

    await bot.say('Ungagged Combot. Channel ID is: ' + channel)

@bot.command(pass_context=True)
async def printServers(ctx):
    appinfo = await bot.application_info()
    owner = appinfo.owner.id

    if ctx.message.author.id != owner:
        print('Non-bot owner called print server.')
        await bot.say('Command restricted to bot owner only.')
        return
    else:
        print('Bot Owner called print server.')

    serverConctStr = ''
    for server in bot.servers:
        serverConctStr = serverConctStr + server.name + '\n' 
    await bot.say('Server List: \n' + serverConctStr)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await bot.send_message(ctx.message.channel, "You don't have permissions to run this!")

#Starts the bot
bot.run(token)
handlers = log.handlers[:]
for hdlr in handlers:
    hdlr.close()
    log.removeHandler(hdlr)