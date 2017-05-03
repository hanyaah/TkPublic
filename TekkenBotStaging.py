import discord
import asyncio
import aiohttp

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

          if bool (move_attribute_dict): #if true, dictionary not empty
            move_Found = 1
          else:
            move_Found = 0

          if (move_Found == 1):
            misc_details_Dict = tekkenFinder.get_Misc_Chara_Details(user_Chara_Name)
            embedDict = {**move_attribute_dict, **misc_details_Dict}
            embed_MoveFound = embedCreation.embed_Move_Details(**embedDict)

            await client.send_message(message.channel, embed=embed_MoveFound)
            return

          else:
            misc_details_Dict = tekkenFinder.get_Misc_Chara_Details(user_Chara_Name)
            similar_moves_list = tekkenFinder.get_Similar_Moves(user_Chara_Name, user_Chara_Move)
            embed_SimilarMoves = embedCreation.embed_Similar_Moves(similar_moves_list, **misc_details_Dict)

            await client.send_message(message.channel, embed = embed_SimilarMoves)
            return

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
                                    +'**Use double exclamation marks (!!) for case-sensitive search.**\n'
                                    +'Implemented workaround for moves with alternate notations.\n'
                                    +'All frame data is sourced from RBNorway.org.'         
                                )

    elif message.content.startswith('.early2017'):
        #help requested, send message reinforcements!
        await client.send_message(message.channel, 
                                    'X DAYS UNTIL EARLY 2017'         
                                )

#Starts the bot
client.run(token)


