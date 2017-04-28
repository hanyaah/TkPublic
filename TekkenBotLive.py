import discord
import asyncio
import aiohttp

#self-created modules below
import lib.embedCreation as embedCreation #contains functions for creating an embed
import lib.tekkenFinder as tekkenFinder   #contains functions for finding character and move details

#Nothing to see here, move along
tokenFile = open("tokenLive.txt", 'r')
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

          if not move_attribute_dict:
            print('MOVE NOT FOUND: ' + user_Chara_Move)
            print("======================")
            await client.send_message(message.channel, 'Move not found for '+ '**' + user_Chara_Name.title() + '**')
            return

          misc_details_Dict = tekkenFinder.get_Misc_Chara_Details(user_Chara_Name)

          embedDict = {**move_attribute_dict, **misc_details_Dict}

          processedEmbed = embedCreation.embed_creator(**embedDict)

          await client.send_message(message.channel, embed=processedEmbed)

        elif characterExists == 0:
          await client.send_message(message.channel, 'Character not found: ' + '**' + user_Chara_Name + '**')

    elif message.content.startswith('.help'):
        #help requested, send message reinforcements!
        await client.send_message(message.channel, 
                                    'Ping <@99090187560173568> for any questions/suggestions/bug reports.\n'
                                    +'Commands: '
                                    +'```'
                                    +'![charname] [notation] or !![charname] [notation] \n'
                                    +'Eg: !kazuya f,n,d,df+2 or !!kazuya f,n,d,DF+2'
                                    +'```'
                                    +'Notable Character Names: Use dvj for deviljin, jack for Jack7, raven for Master Raven, and chloe for Lucky Chloe.'                                    
                                    +'\n'
                                    +'Use double exclamation marks (!!) for case-sensitive search.\n'
                                    +'Moves with alternate notations are not currently supported due to how the moves are formatted.\n'
                                    +'All frame data is sourced from RBNorway.org.'         
                                )

#Starts the bot
client.run(token)


