import discord


def embed_Move_Details(char_name, char_url, char_moveIcon, char_imgur, char_move, char_hitLevel, char_dmg,
                       char_startup,char_block, char_hit, char_counterhit, char_notes):
    # I can live with this for now.

    embed = discord.Embed(title=char_name.title() + " Frame Data (RBNorway)",
                          colour=discord.Colour(0x6342FC),
                          url=char_url,
                          description="**Move: " + char_move + "**\n" + char_moveIcon)

    print(char_startup)

    embed.set_thumbnail(url=char_imgur)
    embed.set_author(name=char_name.title(), url=char_url, icon_url="https://i.imgur.com/9YWQdwE.jpg")
    embed.add_field(name="Property", value=char_hitLevel)
    embed.add_field(name="Damage", value=char_dmg)
    embed.add_field(name="Startup", value='i' + str(char_startup))
    embed.add_field(name="Block", value=char_block)
    embed.add_field(name="Hit", value=char_hit)
    embed.add_field(name="Counter Hit", value=char_counterhit)
    embed.add_field(name="Notes", value=char_notes)

    return embed


def embed_Similar_Moves(similar_Moves_List, char_name, char_url, char_imgur):
    embed = discord.Embed(title=char_name.title() + " Frame Data (RBNorway)",
                          colour=discord.Colour(0xFF5733),
                          url=char_url,
                          description="**Move Not Found.**")
    embed.set_thumbnail(url=char_imgur)
    embed.set_author(name=char_name.title(), url=char_url, icon_url="https://i.imgur.com/9YWQdwE.jpg")

    moveList = ''
    if len(similar_Moves_List) == 0:
        moveList = 'No similar moves found.'
    for moveNum, move in enumerate(similar_Moves_List):
        if moveNum < 9:
            moveList = moveList + move + '\n'

    embed.add_field(name='Similar moves', value=moveList)

    return embed


def embed_legend():
    forwardStr = '**f** = forward \t\t<:FORWARD:303930958049181719>'
    backwardStr = '**b** = backward\t<:BACK:304165586756304896>'
    upwardStr = '**u** = up  \t\t\t\t<:UP:304165643282808833>'
    downwardStr = '**d** = down\t\t\t<:DOWN:304165435233009664>'
    neutralStr = '**n** = neutral\t\t <:NEUTRAL:304178841327239168>'
    directionStr = forwardStr + '\n' + backwardStr + '\n' + upwardStr + '\n' + downwardStr + '\n' + neutralStr

    lpStr = '**1** = Left Punch\t <:1_:304166000369336321>'
    rpStr = '**2** = Right Punch  <:2_:304166127985098763>'
    lkStr = '**3** = Left Kick\t    <:3_:304166145299054592>'
    rkStr = '**4** = Right Kick\t <:4_:304166174541742082>'
    attackStr = lpStr + '\n' + rpStr + '\n' + lkStr + '\n' + rkStr

    fcStr = '**FC** = Full Crouch'
    wrStr = '**WR** = While Running'
    wsStr = '**WS** = While Standing(Up)'
    ssStr = '**SS** = Sidestep'
    btStr = '**BT** = Backturned'
    stateStr = fcStr + '\n' + wrStr + '\n' + wsStr + '\n' + ssStr + '\n' + btStr

    tz_glossary_url = 'http://www.tekkenzaibatsu.com/wiki/Glossary'
    thumbnail = 'http://i.imgur.com/bLLr0sj.png'
    embed = discord.Embed(title="Tekken Notations",
                          colour=discord.Colour(0x7fffd4),
                          url=tz_glossary_url,
                          description="A list of tekken notations")
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name='Directions', value=directionStr)
    embed.add_field(name='Attack', value=attackStr)
    embed.add_field(name='State', value=stateStr)

    return embed
