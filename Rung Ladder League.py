import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
import datetime

client = commands.Bot(command_prefix = "!")
bMsg = ' '


teamRosters = {'TnS' : [('joe', 'steamid:0:0:1'), ('jane', 'STEAMID::0:0:2')],
               'auto!': [('bert', 'steamid:0:0:4'), ('ernie', 'STEAMID::0:0:3')]}
upcomingMatchs = {}
records = {'TnS': [0, 0, '🟢'],
             'auto!': [0, 0, '🟢'],
             'St4ck': [0, 0, '🟢'],
             'cc:': [0, 0, '🟢'],
             'Sn#': [0, 0, '🟢'],} # W, L, Status (0 for open (green light), 1 for pending and scheduled (red light), 2 for suspended (yellow light).), placement on standings
teams = list(records)
standings = []

@client.command(pass_context=True)
async def updatestandings(ctx):
    teams = list(records)
    bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
    bEnumList = list(enumerate(teams, start = 1))

    for i in range(len(bEnumList)):
        #print(i)
        bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
        bMsg = ''.join(bMsgList)

    await ctx.send("```" + bMsg + "```")

@client.command(pass_context=True)
async def suspend(ctx, Team):
    records[str(Team)][2] = '🟡'

    teams = list(records)
    bMsgList =  [' Rank  │     Team Name              W              L         Status  \n', '-------╪---------------------╪-------------╪-------------╪-----------\n']
    bEnumList = list(enumerate(teams, start = 1))

    for i in range(len(bEnumList)):
        #print(i)
        bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "  │        " + bEnumList[i][1] + (" " * (13 - len(bEnumList[i][1]))) + "│      " + str(records[bEnumList[i][1]][0]) + (" " * (7 - len(str(records[bEnumList[i][1]][0]))))  + "│       " + str(records[bEnumList[i][1]][1]) + (" " * (6 - len(str(records[bEnumList[i][1]][1])))) + "│    " + records[bEnumList[i][1]][2] + "\n")
        bMsg = ''.join(bMsgList)
    await ctx.send("```" + bMsg + "```")

@client.command(pass_context=True)
async def reinstate(ctx, Team):
    if(records[str(Team)][2] == '🟡'):
        records[str(Team)][2] = '🟢'

        teams = list(records)
        bMsgList =  [' Rank  │     Team Name              W              L         Status  \n', '-------╪---------------------╪-------------╪-------------╪-----------\n']
        bEnumList = list(enumerate(teams, start = 1))

        for i in range(len(bEnumList)):
            #print(i)
            bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "  │        " + bEnumList[i][1] + (" " * (13 - len(bEnumList[i][1]))) + "│      " + str(records[bEnumList[i][1]][0]) + (" " * (7 - len(str(records[bEnumList[i][1]][0]))))  + "│       " + str(records[bEnumList[i][1]][1]) + (" " * (6 - len(str(records[bEnumList[i][1]][1])))) + "│    " + records[bEnumList[i][1]][2] + "\n")
            bMsg = ''.join(bMsgList)
        await ctx.send("```" + bMsg + "```")
    else:
        await ctx.send("This team was never suspended...")

@client.command(pass_context=True)
async def createteam(ctx, TeamName, TeamCaptain, SteamID):
    if(TeamName in teamRosters):
        await ctx.send("Sorry that team already exists..")
    else:
        teamRosters[TeamName] = [(TeamCaptain, SteamID)]
        records[TeamName] = [0, 0, '❌']
        print(teamRosters)
        await ctx.guild.create_role(name= TeamName, hoist=True)
        playerAdd = discord.utils.get(ctx.message.guild.roles, name=TeamName)
        await ctx.message.author.add_roles(playerAdd)

    teams = list(records)
    bMsgList =  [' Rank  │     Team Name              W              L         Status  \n', '-------╪---------------------╪-------------╪-------------╪-----------\n']
    bEnumList = list(enumerate(teams, start = 1))

    for i in range(len(bEnumList)):
        #print(i)
        bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "  │        " + bEnumList[i][1] + (" " * (13 - len(bEnumList[i][1]))) + "│      " + str(records[bEnumList[i][1]][0]) + (" " * (7 - len(str(records[bEnumList[i][1]][0]))))  + "│       " + str(records[bEnumList[i][1]][1]) + (" " * (6 - len(str(records[bEnumList[i][1]][1])))) + "│    " + records[bEnumList[i][1]][2] + "\n")
        bMsg = ''.join(bMsgList)
    await ctx.send("```" + bMsg + "```")

@client.command(pass_context=True)
async def playeradd(ctx, TeamName, player, SteamID):
    playerRostered = 0
    if(TeamName not in teamRosters):
        await ctx.send("No such team exists..")
    else:
        for i in teamRosters:
            for j in teamRosters[i]:
                if(SteamID in j):
                    playerRostered = 1
        
        if(playerRostered == 0):
            playerID = (player, SteamID)
            teamRosters[TeamName].append(playerID)
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

@client.command(pass_context=True)
async def playerremove(ctx, TeamName, player, SteamID):
    print(teamRosters)
    player = (player, SteamID)
    if(TeamName in teamRosters):
        if(player in teamRosters[TeamName]):
            await ctx.send("Player " + player[0] + " ( " + player[1] + " ) has been successfully removed from " + TeamName)
            teamRosters[TeamName].remove(player)
            print(teamRosters)
            
        else:
            await ctx.send("Player does not exist on team.. Maybe mistyped player name or SteamID")
    else:
        await ctx.send("No such team exists..")

@client.command(pass_context=True)
async def challenge(ctx, Team1: discord.Role, Team2: discord.Role):
    challenger = Team1
    defender = Team2
    if(records[Team2][2] == '🔴'):
        await ctx.message.channel.send(str(Team2) + " has a challenge or scheduled match in progress..")
    elif(records[Team2][2] == '❌'):
        await ctx.message.channel.send(str(Team2) + " does not have 4 players on the roster yet")
    else:
        for i in teams:
            if (i in str(ctx.message.author.roles)):
                teamCheck = i
        if(teamCheck == str(challenger)):
            if(defender.position > challenger.position):
                await ctx.message.channel.send(str(challenger) + " has challenged " + str(defender) + " to a match!")
            else:
                await ctx.message.channel.send("You can only challenge teams at a higher rank than you..")
        else:
            await ctx.message.channel.send("You are not on that Team or you did the format wrong..")
        
        records[str(challenger)][2] = '🔴'
        records[str(defender)][2] = '🔴'

        #teams = list(records)
        bMsgList =  [' Rank  │     Team Name              W              L         Status  \n', '-------╪---------------------╪-------------╪-------------╪-----------\n']
        bEnumList = list(enumerate(teams, start = 1))

        for i in range(len(bEnumList)):
            #print(i)
            bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "  │        " + bEnumList[i][1] + (" " * (13 - len(bEnumList[i][1]))) + "│      " + str(records[bEnumList[i][1]][0]) + (" " * (7 - len(str(records[bEnumList[i][1]][0]))))  + "│       " + str(records[bEnumList[i][1]][1]) + (" " * (6 - len(str(records[bEnumList[i][1]][1])))) + "│    " + records[bEnumList[i][1]][2] + "\n")
            bMsg = ''.join(bMsgList)
        await ctx.send("```" + bMsg + "```")

@client.command(pass_context=True)
async def results(ctx, Team1: discord.Role, score1: int, Team2: discord.Role, score2: int):
    global bMsg
    champion = len(ctx.guild.roles) - 3
    '''winnerIndex = teams.index(winner)
    loserIndex = teams.index(loser)

    if (winnerIndex > loserIndex):
        newRank = teams.pop(winnerIndex)
        teams.insert(loserIndex, newRank)'''
        
    if (score1 > score2):
        winner = Team1
        loser = Team2
    else:
        winner = Team2
        loser = Team1

    await ctx.send(str(winner) + " has won their match against " + str(loser) + " by a score of " + str(score1) + " to " + str(score2) + ".")

    if(int(winner.position) < int(loser.position)):
        await winner.edit(position=int(loser.position))
    winnerIndex = teams.index(str(winner))
    loserIndex = teams.index(str(loser))

    if (winnerIndex > loserIndex):
        newRank = teams.pop(winnerIndex)
        teams.insert(loserIndex, newRank)

    if(winner.position == champion):
        await ctx.message.channel.send(str(winner) + " are the current **CHAMPIONS**")

    records[str(winner)][0] += 1 #add one to the wins column
    records[str(loser)][1] += 1 #add one to the loss column

    records[str(loser)][2] = '🟢'
    records[str(winner)][2] = '🟢'

    #updatingStandings()
    #teams = list(records)
    bMsgList =  [' Rank  │     Team Name              W              L         Status  \n', '-------╪---------------------╪-------------╪-------------╪-----------\n']
    bEnumList = list(enumerate(teams, start = 1))

    for i in range(len(bEnumList)):
        #print(i)
        bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "  │        " + bEnumList[i][1] + (" " * (13 - len(bEnumList[i][1]))) + "│      " + str(records[bEnumList[i][1]][0]) + (" " * (7 - len(str(records[bEnumList[i][1]][0]))))  + "│       " + str(records[bEnumList[i][1]][1]) + (" " * (6 - len(str(records[bEnumList[i][1]][1])))) + "│    " + records[bEnumList[i][1]][2] + "\n")
        bMsg = ''.join(bMsgList)
    await ctx.send("```" + bMsg + "```")

@client.command(pass_context=True)
async def removeteam(ctx, TeamName: discord.Role):
    if(ctx.message.author == teamRosters[str(TeamName.name)][0][0]):
        del teamRosters[str(TeamName.name)]
        print(teamRosters)
        await TeamName.delete()
    else:
        await ctx.send("You are not the captain of this team..")


client.run('NzMyMzcyMTcwMzY5NTMxOTc4.XwzovA.ngNtyusstc8Oz_xV2pM1BH_JZ70') #input your discord token here.  Keep the quotations