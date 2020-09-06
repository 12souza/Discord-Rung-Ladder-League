import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
from datetime import date
import random

client = commands.Bot(command_prefix = "!")
bMsg = ' '

mapList = ['2fort', 'blutopia', 'schtop', 'siege', 'openfire_lowgrens', 'raiden5', 'alchimy_l2', 'warpath_l']
teamRosters = {'TnS' : {'joe': [('steamid:0:0:1', 'Captain', '05/07/2020')], 'jane': [('STEAMID::0:0:2', 'Player', '05/07/2020')]},
               'auto!': {'bert': [('steamid:0:0:4', 'Captain', '05/07/2020')], 'ernie': [('STEAMID::0:0:3', 'Player', '05/07/2020')]}}
upcomingMatches = {}
records = {'TnS': [0, 0, '🟢'],
             'auto!': [0, 0, '🟢'],
             'St4ck': [0, 0, '🟢'],
             'cc:': [0, 0, '🟢'],
             'Sn#': [0, 0, '🟢'],} # W, L, Status (0 for open (green light), 1 for pending and scheduled (red light), 2 for suspended (yellow light).), placement on standings
teams = list(records)

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
    records[str(Team)][2] = ' ❗'

    teams = list(records)
    bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
    bEnumList = list(enumerate(teams, start = 1))

    for i in range(len(bEnumList)):
        #print(i)
        bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
        bMsg = ''.join(bMsgList)

    await ctx.send("```" + bMsg + "```")

@client.command(pass_context=True)
async def reinstate(ctx, Team):
    if(records[str(Team)][2] == ' ❗'):
        records[str(Team)][2] = '🟢'

        teams = list(records)
        bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
        bEnumList = list(enumerate(teams, start = 1))

        for i in range(len(bEnumList)):
        #print(i)
            bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
            bMsg = ''.join(bMsgList)

        await ctx.send("```" + bMsg + "```")
    else:
        await ctx.send("This team was never suspended...")

@client.command(pass_context=True)
async def createteam(ctx, TeamName, TeamCaptain, SteamID):
    today = date.today()
    if(TeamName in teamRosters):
        await ctx.send("Sorry that team already exists..")
    else:
        teamRosters[TeamName] = {}
        teamRosters[TeamName][TeamCaptain] = []
        teamRosters[TeamName][TeamCaptain] = [(SteamID, 'Captain', str(today.strftime("%d/%m/%Y")))]
        records[TeamName] = [0, 0, '❌']
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

    await ctx.send("```" + bMsg + "```")

@client.command(pass_context=True)
async def playeradd(ctx, TeamName, player, SteamID, role):
    today = date.today()
    playerRostered = 0
    rTeams = list(teamRosters)
    print(teamRosters)
    if(TeamName not in rTeams):
        await ctx.send("No such team exists..")
    else:
        if (role == 'Captain' or role == 'Player'):
            #trying to get this working with the nested dictionary to where it will exclude any attempt at adding a duplicate SteamID (adminable, not crucial.)  This works with the non-nested dictionary
            for i in teamRosters:
                for j in teamRosters[i]:
                    if((SteamID.lower()) in (teamRosters[i][j][0][0].lower())):
                        playerRostered = 1
            
            if(playerRostered == 0):
                playerID = (SteamID, role, str(today.strftime("%d/%m/%Y")))
                teamRosters[TeamName][player] = []
                teamRosters[TeamName][player].append(playerID)
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
            await ctx.send("You have given this player an invalid Role")

@client.command(pass_context=True)
async def playerremove(ctx, TeamName, player):
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

@client.command(pass_context=True)
async def challenge(ctx, Team1: discord.Role, Team2: discord.Role, map1):
    challenger = Team1
    defender = Team2
    for i in teams:
        if (i in str(ctx.message.author.roles)):
            teamCheck = i
    if(teamCheck == str(challenger)):
        #print(defender.position, challenger.position)
        if(defender.position > challenger.position):
            if(records[str(Team2)][2] == '🔴'):
                await ctx.message.channel.send(str(Team2) + " has a challenge or scheduled match in progress..")
            elif(records[str(Team2)][2] == '❌'):
                await ctx.message.channel.send(str(Team2) + " does not have 4 players on the roster yet")
            elif(records[str(Team2)][2] == ' ❗'):
                await ctx.message.channel.send(str(Team2) + " is suspended and can not challenge or be challenged")
            else:
                
                records[str(challenger)][2] = '🔴'
                records[str(defender)][2] = '🔴'

                #teams = list(records)
                bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
                bEnumList = list(enumerate(teams, start = 1))

                for i in range(len(bEnumList)):
                    #print(i)
                    bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
                    bMsg = ''.join(bMsgList)

                await ctx.send("```" + bMsg + "```")

                match = str(Team1) + " vs " + str(Team2)
                tiebreaker = random.choice(mapList)
                upcomingMatches[match] = [0, map1, None, tiebreaker, str(Team1), str(Team2)]
                print(upcomingMatches)
            await ctx.message.channel.send(str(challenger) + " has challenged " + str(defender) + " to a match!  The maps will be " + map1 + ", a map of " + str(Team2) + "'s choosing if they accept, and " + tiebreaker + " for the tiebreaker")
        else:
            await ctx.message.channel.send("You can only challenge teams at a higher rank than you..")
    else:
        await ctx.message.channel.send("You are not on that Team or you did the format wrong..")
        
@client.command(pass_context=True)
async def accept(ctx, Team1: discord.Role, map2):
    for i in upcomingMatches:
        if str(Team1) in i:
            upcomingMatches[i][0] = 1
            upcomingMatches[i][2] = map2
            await ctx.send("```" + upcomingMatches[i][5] + " has accepted the challenge from " + upcomingMatches[i][4] + "\nRound 1: " + upcomingMatches[i][1] + "\nRound 2: " + upcomingMatches[i][2] + "\nTiebreaker: " + upcomingMatches[i][3] + "```" )      
        else:
            await ctx.send(str(Team1) + " has no challengers..")
@client.command(pass_context=True)
async def results(ctx, Team1: discord.Role, score1: int, Team2: discord.Role, score2: int):
    global bMsg
    champion = len(ctx.guild.roles) - 3
        
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
    bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
    bEnumList = list(enumerate(teams, start = 1))

    for i in range(len(bEnumList)):
        #print(i)
        bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
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

@client.command(pass_context=True)
async def roster(ctx, TeamName):
    #rosters = list(teamRosters)
    bMsgList =  ['PlayerName     |           STEAMID          |     ROLE   | DATE ADDED |\n', '---------------╪----------------------------╪------------╪------------╪\n']

    for i in teamRosters[TeamName]:
        for j in range(len(teamRosters[TeamName][i])):
            print(teamRosters[TeamName][i][j][0], teamRosters[TeamName][i][j][1], teamRosters[TeamName][i][j][2])
            bMsgList.append(i + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][j][0]) + " " * (27 - len(str(teamRosters[TeamName][i][j][0]))) + "│ " + str(teamRosters[TeamName][i][j][1]) + " " * (11 - len(str(teamRosters[TeamName][i][j][1]))) + "│ "  + str(teamRosters[TeamName][i][j][2]) + " " * (11 - len(str(teamRosters[TeamName][i][j][2]))) + "│\n")
    
    bMsg = ''.join(bMsgList)
    await ctx.send("```" + bMsg + "```")


client.run('NzMyMzcyMTcwMzY5NTMxOTc4.XwzovA.ngNtyusstc8Oz_xV2pM1BH_JZ70') #input your discord token here.  Keep the quotations