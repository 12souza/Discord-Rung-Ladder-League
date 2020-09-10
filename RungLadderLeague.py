import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
from datetime import date
import random
import os
import sys

client = commands.Bot(command_prefix = "!")
bMsg = ' '

with open('maplist.json') as m:
  mapList = json.load(m)

with open('teamrosters.json') as tR:
  teamRosters = json.load(tR)
'''teamRosters = {'TnS' : {'joe': [('steamid:0:0:1', 'Captain', '05/07/2020')], 'jane': [('STEAMID::0:0:2', 'Player', '05/07/2020')]},
               'auto!': {'bert': [('steamid:0:0:4', 'Captain', '05/07/2020')], 'ernie': [('STEAMID::0:0:3', 'Player', '05/07/2020')]}}'''

with open('upcomingmatches.json') as uM:
  upcomingMatches = json.load(uM)

with open('records.json') as r:
  records = json.load(r)

for i in records:
    if(records[i][2] == 'ðŸŸ¢'):
        records[i][2] = '🟢'
    if(records[i][2] == 'ðŸ”´'):
        records[i][2] = '🔴'
    if(records[i][2] == 'â›”'):
        records[i][2] = '⛔'
    if(records[i][2] == 'ðŸš«'):
        records[i][2] = '🚫'

print(records)

teams = list(records)

@client.event
async def on_ready():
    channel = client.get_channel(752215331476602920)
    await channel.send('Bot is ready to go... place all your commands/transactions here')

@client.command(pass_context=True)
async def updatestandings(ctx):
    if(ctx.message.channel.name == 'commands'):
        #teams = list(records)
        bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
        bEnumList = list(enumerate(teams, start = 1))

        for i in range(len(bEnumList)):
            #print(i)
            bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
            bMsg = ''.join(bMsgList)
        channel = client.get_channel(751542184968323223)
        msg_id = 752065329185685605

        msg = await channel.fetch_message(msg_id)
        await msg.edit(content="```" + bMsg + "```")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

@client.command(pass_context=True)
async def suspend(ctx, Team):
    records[str(Team)][2] = '⛔'

    teams = list(records)
    bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
    bEnumList = list(enumerate(teams, start = 1))

    for i in range(len(bEnumList)):
        #print(i)
        bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
        bMsg = ''.join(bMsgList)

    channel = client.get_channel(751542184968323223)
    msg_id = 752065329185685605

    msg = await channel.fetch_message(msg_id)
    await msg.edit(content="```" + bMsg + "```")

@client.command(pass_context=True)
async def reinstate(ctx, Team):
    if(records[str(Team)][2] == '⛔'):
        if(len(teamRosters[Team]) >= 4):
            records[str(Team)][2] = '🟢'
        else:
            records[str(Team)][2] = '🚫' 

        teams = list(records)
        bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
        bEnumList = list(enumerate(teams, start = 1))

        for i in range(len(bEnumList)):
        #print(i)
            bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
            bMsg = ''.join(bMsgList)

            channel = client.get_channel(751542184968323223)
            msg_id = 752065329185685605

            msg = await channel.fetch_message(msg_id)
            await msg.edit(content="```" + bMsg + "```")
    else:
        await ctx.send("This team was never suspended...")

@client.command(pass_context=True)
async def createteam(ctx, TeamName, TeamCaptain: discord.User, SteamID):
    today = date.today()
    if(ctx.author.name == str(TeamCaptain.name)):
        if(TeamName in teamRosters):
            await ctx.send("Sorry that team already exists..")
        else:
            teamRosters[TeamName] = {}
            teamRosters[TeamName][str(TeamCaptain.name)] = []
            teamRosters[TeamName][str(TeamCaptain.name)] = [SteamID, 'Captain', str(today.strftime("%d/%m/%Y")), TeamCaptain.id]
            records[TeamName] = [0, 0, '🚫']
            print(teamRosters)
            await ctx.guild.create_role(name= TeamName, hoist=True)
            playerAdd = discord.utils.get(ctx.message.guild.roles, name=TeamName)
            await ctx.message.author.add_roles(playerAdd)

        teams = list(records)
        bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
        bEnumList = list(enumerate(teams, start = 1))

        for i in range(len(bEnumList)):
            #print(i)
            bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
            bMsg = ''.join(bMsgList)

        channel = client.get_channel(751542184968323223)
        msg_id = 752065329185685605

        msg = await channel.fetch_message(msg_id)
        await msg.edit(content="```" + bMsg + "```")
    else:
        await ctx.send("You must put name yourself as the Team Captain or have the Team Captain add the team..")

@client.command(pass_context=True)
async def playeradd(ctx, TeamName, player, SteamID):
    if(teamRosters[TeamName][ctx.message.author.name][1] == "Captain"):    
        today = date.today()
        playerRostered = 0
        rTeams = list(teamRosters)
        print(teamRosters)
        if(TeamName not in rTeams):
            await ctx.send("No such team exists..")
        else:
            #trying to get this working with the nested dictionary to where it will exclude any attempt at adding a duplicate SteamID (adminable, not crucial.)  This works with the non-nested dictionary
            for i in teamRosters:
                for j in teamRosters[i]:
                    if((SteamID.lower()) in (teamRosters[i][j][0][0].lower())):
                        playerRostered = 1
                
            if(playerRostered == 0):
                #playerID = [SteamID, role, str(today.strftime("%m/%d/%Y"))]
                teamRosters[TeamName][str(player)] = []
                teamRosters[TeamName][str(player)].append(SteamID)
                teamRosters[TeamName][str(player)].append("Player")
                teamRosters[TeamName][str(player)].append(str(today.strftime("%m/%d/%Y")))
                print(teamRosters)
                playerAdd = discord.utils.get(ctx.message.guild.roles, name=TeamName)
                await ctx.message.author.add_roles(playerAdd)
                await ctx.send(player + " ( " + SteamID + " ) has been successfully added to " + TeamName)
            else:
                await ctx.send("Player is already assigned to a team..")

            print(len(teamRosters[TeamName]))
            if (len(teamRosters[TeamName]) == 4):
                await ctx.send(str(TeamName) + " now have enough players on their team to challenge another team..")
                records[TeamName][2] = '🟢'
    else:
        await ctx.send("You are not the Captain of this team.  Please let your Captain know a player needs to be added to the roster..")

@client.command(pass_context=True)
async def promote(ctx, TeamName, player: discord.User):
    if(teamRosters[TeamName][ctx.message.author.name][1] == "Captain"):
        if(teamRosters[TeamName][str(player.name)][1] == "Player"):
            teamRosters[TeamName][str(player.name)][1] = "Captain"
            teamRosters[TeamName][str(player.name)].append(player.id)
            await ctx.send(str(player.name) + " has been promoted to **Captain** of **auto!**")
            print(teamRosters)
        else:
            ctx.send("Player does not exist or is already a Captain")
    else:
        ctx.send("Only captains can promote players") 

@client.command(pass_context=True)
async def demote(ctx, TeamName, player: discord.User):
    if(teamRosters[TeamName][ctx.message.author.name][1] == "Captain"):
        if(teamRosters[TeamName][str(player.name)][1] == "Captain"):
            teamRosters[TeamName][str(player.name)][1] = "player"
            teamRosters[TeamName][str(player.name)].remove(player.id)
            await ctx.send(str(player.name) + " has been demoted to **Player** of **auto!**")
            print(teamRosters)
        else:
            ctx.send("Player does not exist or is already a Player")
    else:
        ctx.send("Only captains can demote players") 

@client.command(pass_context=True)
async def playerremove(ctx, TeamName, player):
    if(teamRosters[TeamName][ctx.message.author.name][1] == "Captain"):    
        print(teamRosters)
        #player = (player, SteamID, role, dateAdded)
        if(TeamName in teamRosters):
            if(player in teamRosters[TeamName]):
                await ctx.send("Player " + player[0] + " ( " + player[1] + " ) has been successfully removed from " + TeamName)
                del teamRosters[TeamName][player]
                print(teamRosters)
                
            else:
                await ctx.send("Player does not exist on team.. Maybe mistyped player name or SteamID")
        else:
            await ctx.send("No such team exists..")
    else:
        await ctx.send("You are not the Captain of this team.  Please let your Captain know a player needs to be removed from the roster..")

@client.command(pass_context=True)
async def challenge(ctx, Team1: discord.Role, Team2: discord.Role, map1):
    teams = list(records)
    challenger = Team1
    defender = Team2

    defenderIndex = teams.index(str(defender))
    challengerIndex = teams.index(str(challenger))

    for i in teams:
        if (i in str(ctx.message.author.roles)):
            teamCheck = i
    if(teamCheck == str(challenger)):
        if(teamRosters[str(Team1)][ctx.message.author.name][1] == "Captain"):
            if(defenderIndex < challengerIndex):
                if(records[str(Team2)][2] == '🔴'):
                    await ctx.message.channel.send(str(Team2) + " has a challenge or scheduled match in progress..")
                elif(records[str(Team2)][2] == '🚫'):
                    await ctx.message.channel.send(str(Team2) + " does not have 4 players on the roster yet")
                elif(records[str(Team2)][2] == '⛔'):
                    await ctx.message.channel.send(str(Team2) + " is suspended and can not challenge or be challenged")
                else:
                    
                    records[str(challenger)][2] = '🔴'
                    records[str(defender)][2] = '🔴'

                    #teams = list(records)
                    bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
                    bEnumList = list(enumerate(teams, start = 1))
                    tiebreaker = random.choice(mapList)
                    for i in range(len(bEnumList)):
                        #print(i)
                        bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
                        bMsg = ''.join(bMsgList)

                    channel = client.get_channel(751542184968323223)
                    msg_id = 752065329185685605

                    msg = await channel.fetch_message(msg_id)
                    await msg.edit(content="```" + bMsg + "```")

                    match = str(Team1) + " vs " + str(Team2)
                    upcomingMatches[match] = [1, map1, 'TBA', tiebreaker, str(Team1), str(Team2), 'TBA', 'TBA']
                    
                    #uMsgList =  ['Defender │ Challenger │    Round 1 Map     │    Round 2 Map     │   Tiebreaker Map   │     Date    │     Time    │     Status   │\n---------╪------------╪--------------------╪--------------------╪--------------------╪-------------╪-------------╪--------------╪\n ']
                    '''uMsgList = [str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4]
                                +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                +"\n Round 2 Map: " + upcomingMatches[i][2]
                                +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][6])'''
                    uMsgList = []
                    for i in upcomingMatches:
                        #print(upcomingMatches[i])
                        if(upcomingMatches[i][0] == 0):
                            uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "       **PENDING**"
                                            +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                            +"\n Round 2 Map: " + upcomingMatches[i][2]
                                            +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][6]))

                        else:
                            uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + "vs" + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                                            +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                            +"\n Round 2 Map: " + upcomingMatches[i][2]
                                            +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][6]))

                        uMsg = ''.join(uMsgList)
                    
                    channel2 = client.get_channel(752215154430574742)
                    msg_id2 = 752246430906712104
                    
                    msg = await channel2.fetch_message(msg_id2)
                    await msg.edit(content= "```" + uMsg + "```")

                await ctx.message.channel.send(str(challenger) + " has challenged " + str(defender) + " to a match!  The maps will be " + map1 + ", a map of " + str(Team2) + "'s choosing if they accept, and " + tiebreaker + " for the tiebreaker")
            else:
                await ctx.message.channel.send("You can only challenge teams at a higher rank than you..")
        else:
            await ctx.message.channel.send("You are not the captain of " + str(Team1) + ".  Please advise your captain to challenge this team!")
    else:
        await ctx.message.channel.send("You are not on that Team or you did the format wrong..")
        
@client.command(pass_context=True)
async def accept(ctx, Team1: discord.Role, map2):
    if(teamRosters[str(Team1)][ctx.message.author.name][1] == "Captain"):
        for i in upcomingMatches:
            if (str(Team1) in i):
                print(upcomingMatches[i][0])
                upcomingMatches[i][0] = 2
                upcomingMatches[i][2] = map2
                await ctx.send("```" + upcomingMatches[i][5] + " has accepted the challenge from " + upcomingMatches[i][4] + "\nRound 1: " + upcomingMatches[i][1] + "\nRound 2: " + upcomingMatches[i][2] + "\nTiebreaker: " + upcomingMatches[i][3] + "```" )      
            else:
                await ctx.send(str(Team1) + " has no challengers..")
    else:
        await ctx.send("Only Captains can accept matches on behalf of their team..  Please advise your team captain of a pending match")

    uMsgList = []
    for i in upcomingMatches:
        #print(upcomingMatches[i])
        if(upcomingMatches[i][0] == 0):
            uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "       **PENDING**"
                            +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                            +"\n Round 2 Map: " + upcomingMatches[i][2]
                            +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][6]))

        else:
            uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + "vs" + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                            +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                            +"\n Round 2 Map: " + upcomingMatches[i][2]
                            +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][6]))

        uMsg = ''.join(uMsgList)
                    
        channel2 = client.get_channel(752215154430574742)
        msg_id2 = 752246430906712104
                    
        msg = await channel2.fetch_message(msg_id2)
        await msg.edit(content= "```" + uMsg + "```")

@client.command(pass_context=True)
async def decline(ctx, Team1):
    pass

@client.command(pass_context=True)
async def results(ctx, Team1: discord.Role, score1: int, Team2: discord.Role, score2: int):
    if(teamRosters[Team1][ctx.message.author.name][1] == "Captain"):
        global bMsg
            
        if (score1 > score2):
            winner = Team1
            loser = Team2
        else:
            winner = Team2
            loser = Team1

        winnerIndex = teams.index(str(winner))
        loserIndex = teams.index(str(loser))

        channel = client.get_channel(752274967973986326)
        await channel.send("```" + str(winner) + " has won their match against " + str(loser) + " by a score of " + str(score1) + " to " + str(score2) + ".```")

        if (winnerIndex > loserIndex):
            newRank = teams.pop(winnerIndex)
            teams.insert(loserIndex, newRank)
        print(teams)

        if(winnerIndex == 0):
            await channel.send(str(winner) + " are the current **CHAMPIONS**")

        records[str(winner)][0] += 1 #add one to the wins column
        records[str(loser)][1] += 1 #add one to the loss column

        records[str(loser)][2] = '🟢'
        records[str(winner)][2] = '🟢'

        #updatingStandings()
        #teams = list(records)
        bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
        bEnumList = list(enumerate(teams, start = 1))

        for i in range(len(bEnumList)):
            #print(i)
            bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
            bMsg = ''.join(bMsgList)

        channel = client.get_channel(751542184968323223)
        msg_id = 752065329185685605

        msg = await channel.fetch_message(msg_id)
        await msg.edit(content="```" + bMsg + "```")

        for i in list(upcomingMatches):
            if(str(winner) in upcomingMatches[i]):
                del upcomingMatches[i]
                print(upcomingMatches)
        
        uMsgList = []
        for i in upcomingMatches:
            #print(upcomingMatches[i])
            if(upcomingMatches[i][0] == 0):
                uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "       **PENDING**"
                                +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                +"\n Round 2 Map: " + upcomingMatches[i][2]
                                +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][6]))

            else:
                uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + "vs" + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                                +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                +"\n Round 2 Map: " + upcomingMatches[i][2]
                                +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][6]))
            uMsg = ''.join(uMsgList)
                    
        channel2 = client.get_channel(752215154430574742)
        msg_id2 = 752246430906712104
                    
        msg = await channel2.fetch_message(msg_id2)
        await msg.edit(content= "```" + uMsg + "```")
    else:
        await ctx.send("Only Captains can report results")

@client.command(pass_context=True)
async def removeteam(ctx, TeamName: discord.Role):
    if(teamRosters[str(TeamName)][ctx.message.author.name][1] == "Captain"):
        del teamRosters[str(TeamName)]
        del records[str(TeamName)]
        print(teamRosters)
        await TeamName.delete()
    else:
        await ctx.send("You are not the captain of this team..")

    teams = list(records)
    bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
    bEnumList = list(enumerate(teams, start = 1))

    for i in range(len(bEnumList)):
        #print(i)
        bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
        bMsg = ''.join(bMsgList)

    channel = client.get_channel(751542184968323223)
    msg_id = 752065329185685605

    msg = await channel.fetch_message(msg_id)
    await msg.edit(content="```" + bMsg + "```")

@client.command(pass_context=True)
async def roster(ctx, TeamName):
    #rosters = list(teamRosters)
    bMsgList =  ['***Roster for ' + TeamName + '***\n\nPlayerName     |           STEAMID          |     ROLE   | DATE ADDED |\n', '---------------╪----------------------------╪------------╪------------╪\n']

    channel = client.get_channel(752215115679662151)

    for i in teamRosters[TeamName]:
        print(i)
        print(teamRosters[TeamName][i][0])
        bMsgList.append(i + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
        bMsg = ''.join(bMsgList)
        #print(teamRosters[TeamName])

    await channel.send(content="```" + bMsg + "```")

@client.command(pass_context=True)
async def restart(ctx):
    await ctx.send("Restarting the bot..")
    print(sys.executable)
    print(['python'] + sys.argv)
    os.execv(sys.executable, ['python'] + sys.argv) 

@client.command(pass_context=True)
async def test(ctx, user: discord.User):
    user = client.get_user(user.id)
    await user.send('👀')
    print(ctx.author.name)
    guild = client.get_guild(732364607821316136) # find ID by right clicking on server icon and choosing "copy id" at the bottom
    if guild.get_member(user.id) is not None: # find ID by right clicking on a user and choosing "copy id" at the bottom
        print("Is in server")
    else:
        pass

client.run('NzMyMzcyMTcwMzY5NTMxOTc4.XwzovA.ngNtyusstc8Oz_xV2pM1BH_JZ70') #input your discord token here.  Keep the quotations