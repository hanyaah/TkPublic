import discord
import asyncio
import aiohttp
import logging
from discord.ext import commands
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

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
    while 1 ==1 :
        await bot.change_presence(game=discord.Game(name='YouLikeADamnFiddle'))
        await asyncio.sleep(200)
        await bot.change_presence(game=discord.Game(name='.help for assistance'))
        await asyncio.sleep(1000)
        await bot.change_presence(game=discord.Game(name='Riri Toppu Tieru'))
        await asyncio.sleep(200)

@bot.event
async def on_message(message):
    #check if message author is a bot
    if message.author.bot:
        return
    if await is_Gagged(message) == True:
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

        if user_Chara_Name == 'dvj' or user_Chara_Name == 'deviljin':
            user_Chara_Name = 'devil_jin'
        if user_Chara_Name == 'jack':
            user_Chara_Name = 'jack7'
        if user_Chara_Name == 'raven':
            user_Chara_Name = 'master_raven'
        if user_Chara_Name == 'yoshi':
            user_Chara_Name = 'yoshimitsu'
        if user_Chara_Name == 'chloe':
            user_Chara_Name = 'lucky_chloe'

        #TODO: IMPLEMENT CHARACTER SHORTHAND NAME CONVERTER, OR CHARACTER NAMELIST DISPLAY
        characterExists = tekkenFinder.does_char_exist(user_Chara_Name)

        if characterExists == 1:
          user_Chara_Name = user_Chara_Name.lower()
          move_attribute_dict = tekkenFinder.get_Move_Details(user_Chara_Name,
                                                              user_Chara_Move,
                                                              case_sensitive_toggle)

          if bool (move_attribute_dict): #if dictionary not empty, move found
            embed_MoveFound = await get_MoveFound_Embed(**move_attribute_dict)
            await bot.send_message(message.channel, embed=embed_MoveFound)
            return

          else: #dictionary is empty, move not found
            embed_SimilarMoves = await get_SimilarMoves_Embed(user_Chara_Name,user_Chara_Move)
            await bot.send_message(message.channel, embed=embed_SimilarMoves)
            return

        elif characterExists == 0:
          await bot.send_message(message.channel, 'Character not found: ' + '**' + user_Chara_Name + '**')
          return

    await bot.process_commands(message)

@bot.command(pass_context=True)
async def early2017():
    """Don't let your memes be dreams."""
    print('MEME MODE ACTIVATED')

    releaseDate = datetime(2017, 6, 2, 0, 0, 0)
    timeNow = datetime.now()
    timeLeft = relativedelta(releaseDate, timeNow)
    early2017Str = str(timeLeft.days) + ' days, ' + str(timeLeft.hours) + ' hours,' +str(timeLeft.minutes) + ' minutes UNTIL TEKKEN 7 RELEASES'

    embed_early2017 = embedCreation.embed_early2017(early2017Str,timeLeft)
    await bot.say(embed = embed_early2017)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def gagcombot(ctx):
    """Gags Combot in this channel. Usable only by admin roles."""
    channel = ctx.message.channel.id
    combot_gagged_channels.append(channel)

    f = open("lib/gagged_channels.txt","a")
    f.write(channel + '\n')
    f.close()

    await bot.say('Mmmph! Gagging Combot.')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ungagcombot(ctx):
    """Ungags Combot in this channel. Usable only by server admins."""
    channel = ctx.message.channel.id
    if channel in combot_gagged_channels:
        combot_gagged_channels.remove(channel)
    else:
        return
    #clear file contents and rewrite
    open("lib/gagged_channels.txt","w").close()
    f = open("lib/gagged_channels.txt","a")
    for channel in combot_gagged_channels:
        f.write(channel+'\n')
    f.close()

    await bot.say('Ungagged Combot. Beep Boop.')

@bot.command(pass_context=True)
async def printServers(ctx):
    """List servers with Combot. Cmd restricted to Bot Owner."""
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

@bot.command(pass_context=True)
async def Frame_Data():
    """Use ![character] [move], !! for case-sensitive search"""
    return

#TODO: This block of code to be used when character html pages are updated, do not edit
# @bot.command(pass_context=True)
# async def convertAll(ctx):
#     """Converts all """
#     appinfo = await bot.application_info()
#     owner = appinfo.owner.id
#
#     if ctx.message.author.id != owner:
#         await bot.say('Hann forgot to hide this function from help listing, lul')
#         return
#     else:
#         await bot.say('Converting all character htmls to json.')
#     tekkenFinder.charJsonMassConverter()
#     return

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await bot.send_message(ctx.message.channel, "You don't have permissions to run this.")

#==============================================
#==========NON COMMAND FUNCTIONS===============
#==============================================
async def is_Gagged(user_message):
    message = user_message
    #check if channel is gagged
    if message.content != '.ungagcombot':
        for channelID in combot_gagged_channels:
            if message.channel.id == channelID:
                return True
    else:
        return False

async def get_MoveFound_Embed(**move_attribute_dict):
    misc_details_Dict = tekkenFinder.get_Misc_Chara_Details(move_attribute_dict['char_name'])
    embedDict = {**move_attribute_dict, **misc_details_Dict}
    embed_MoveFound = embedCreation.embed_Move_Details(**embedDict)

    return embed_MoveFound

async def get_SimilarMoves_Embed(user_Chara_Name, user_Chara_Move):
    misc_details_Dict = tekkenFinder.get_Misc_Chara_Details(user_Chara_Name)
    similar_moves_list = tekkenFinder.get_Similar_Moves(user_Chara_Name, user_Chara_Move)
    embed_SimilarMoves = embedCreation.embed_Similar_Moves(similar_moves_list, user_Chara_Name, **misc_details_Dict)

    return embed_SimilarMoves

#Starts the bot
bot.run(token)

handlers = log.handlers[:]
for hdlr in handlers:
    hdlr.close()
    log.removeHandler(hdlr)