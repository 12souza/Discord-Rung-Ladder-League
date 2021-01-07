import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import json
from datetime import date
from datetime import timedelta
from datetime import datetime
import random
import os
import sys
from discord.ext.commands import MemberConverter
#from tasks import loop

client = commands.Bot(command_prefix = "!")
bMsg = ' '

randomColor = {'gold': 0xFFD700, 'white': 0xFFFFFF, 'silver': 0xC0C0C0, 'magenta': 0xFC33FF, 'blue': 0x3336FF, 'red': 0xFF3333, 'orange': 0xFFA500, "purple": 0x800080, "cyan": 0x00FFFF}
now = datetime.now()
dDay = now + timedelta(days=2)
dHour = now + timedelta(hours=1)

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

with open('rankings.json') as r:
  teams = json.load(r)

with open('matchhistory.json') as mH:
  matchHistory = json.load(mH)  
print(teams)

for i in records:
    if(records[i][2] == 'ðŸŸ¢'):
        records[i][2] = '🟢'
    if(records[i][2] == 'ðŸ”´'):
        records[i][2] = '🔴'
    if(records[i][2] == 'â›”'):
        records[i][2] = '⛔'
    if(records[i][2] == 'ðŸš«'):
        records[i][2] = '🚫'

#teams = list(records)

'''@tasks.loop(seconds=10)
async def timertest():
    print("False")
    await sleep(10)
    print("True")'''


#PLAYER COMMANDS
@client.event
async def on_ready():
    channel = client.get_channel(754382958885994496)
    await channel.send('Bot is ready to go... place all your commands/transactions here')

print(len(upcomingMatches))
async def check_Expired_Challenges():
    await client.wait_until_ready()
    await asyncio.sleep(60)
    while True:
        currentDay = datetime.now().day
        currentHour = datetime.now().hour
        if (len(upcomingMatches) > 0):    
            for i in list(upcomingMatches):
                if(upcomingMatches[i][0] == 1):    
                    if ((upcomingMatches[i][8] == currentDay) and (upcomingMatches[i][9] == currentHour)):
                        channel = client.get_channel(754382958885994496)
                        await channel.send(i + " has been cancelled and " + upcomingMatches[i][4] + " will receive a forfeit win due to " + upcomingMatches[i][5] + "'s inactivity.")
                        winner = upcomingMatches[i][4]
                        loser = upcomingMatches[i][5]

                        winnerIndex = teams.index(winner)
                        loserIndex = teams.index(loser)

                        newRank = teams.pop(winnerIndex)
                        teams.insert(loserIndex, newRank)

                        records[winner][2] = '🟢'
                        records[loser][2] = '🟢'

                        with open('teamrosters.json', 'w') as tR:
                            json.dump(teamRosters, tR)
                        with open('records.json', 'w') as r:
                            json.dump(records, r)
                        with open('upcomingmatches.json', 'w') as uM:
                            json.dump(upcomingMatches, uM)
                        with open('rankings.json', 'w') as tR:
                            json.dump(teams, tR)

                        del upcomingMatches[i]
        else:
            pass
        await asyncio.sleep(2400)

@client.command(pass_context=True)
async def createteam(ctx, TeamName, TeamCaptain: discord.Member, SteamID):
    if(ctx.message.channel.name == 'commands'):    
        today = date.today()
        if(ctx.author.id == TeamCaptain.id):
            print(TeamCaptain.name)
            print(ctx.author.name)
            if(TeamName in teamRosters):
                await ctx.send("Sorry that team already exists..")
            else:
                teamRosters[TeamName] = {}
                teamRosters[TeamName][TeamCaptain.nick] = []
                teamRosters[TeamName][TeamCaptain.nick] = [SteamID, 'Captain', str(today.strftime("%m/%d/%Y")), TeamCaptain.id]
                records[TeamName] = [0, 0, '🚫', "None", 0]
                teams.append(TeamName)
                print(teamRosters)
                await ctx.guild.create_role(name= TeamName, hoist=True, colour=discord.Colour(0xff0000))
                playerAdd = discord.utils.get(ctx.message.guild.roles, name=TeamName)
                await ctx.message.author.add_roles(playerAdd)

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

            rMsgList =  ['***Roster for ' + TeamName + '***\n\nPlayerName     |           STEAMID          |     ROLE   | DATE ADDED |\n', '---------------╪----------------------------╪------------╪------------╪\n']
            channel2 = client.get_channel(752215115679662151)

            for i in teamRosters[TeamName]:
                print(teamRosters[TeamName][i][0])
                if (len(i) < 16):    
                    rMsgList.append(i + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                elif (len(i) >= 16):
                    rMsgList.append(i[0:15] + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
            rMsg = ''.join(rMsgList)
            msgid = await channel2.send(content="```" + rMsg + "```")
            records[TeamName][4] = msgid.id


        else:
            await ctx.send("You must put name yourself as the Team Captain or have the Team Captain add the team..")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

    with open('teamrosters.json', 'w') as tR:
        json.dump(teamRosters, tR)
    with open('records.json', 'w') as r:
        json.dump(records, r)
    with open('upcomingmatches.json', 'w') as uM:
        json.dump(upcomingMatches, uM)
    with open('rankings.json', 'w') as tR:
        json.dump(teams, tR)

@client.command(pass_context=True)
async def playeradd(ctx, player, SteamID):
    print(ctx.message.author.display_name)
    TeamName = " "
    
    for i in list(teamRosters):
        if(ctx.message.author.display_name in teamRosters[i]):
            TeamName = i
    
    if(ctx.message.channel.name == 'commands'):  
        
        if(teamRosters[TeamName][ctx.message.author.display_name][1] == "Captain"):    
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

                rMsgList =  ['***Roster for ' + TeamName + '***\n\nPlayerName     |           STEAMID          |     ROLE   | DATE ADDED |\n', '---------------╪----------------------------╪------------╪------------╪\n']
                channel2 = client.get_channel(752215115679662151)
                rMsgID = records[TeamName][4]
                for i in teamRosters[TeamName]:
                    print(teamRosters[TeamName][i][0])
                    if (len(i) < 16):    
                        rMsgList.append(i + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                    elif (len(i) >= 16):
                        rMsgList.append(i[0:15] + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                rMsg = ''.join(rMsgList)
                
                rMsgEdit = msg = await channel2.fetch_message(rMsgID)
                await rMsgEdit.edit(content="```" + rMsg + "```")

                

            with open('teamrosters.json', 'w') as tR:
                json.dump(teamRosters, tR)
            with open('records.json', 'w') as r:
                json.dump(records, r)
            with open('upcomingmatches.json', 'w') as uM:
                json.dump(upcomingMatches, uM)

        else:
            await ctx.send("You are not the Captain of this team.  Please let your Captain know a player needs to be added to the roster..")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")   

@client.command(pass_context=True)
async def promote(ctx, player: discord.Member):
    for i in list(teamRosters):
        if(ctx.message.author.display_name in teamRosters[i]):
            TeamName = i
    
    if(ctx.message.channel.name == 'commands'):    
        if(teamRosters[TeamName][ctx.message.author.display_name][1] == "Captain"):
            if(teamRosters[TeamName][str(player.nick)][1] == "Player"):
                teamRosters[TeamName][str(player.nick)][1] = "Captain"
                teamRosters[TeamName][str(player.nick)].append(player.id)
                await ctx.send(str(player.nick) + " has been promoted to **Captain** of " + TeamName)
                print(teamRosters)

                rMsgList =  ['***Roster for ' + TeamName + '***\n\nPlayerName     |           STEAMID          |     ROLE   | DATE ADDED |\n', '---------------╪----------------------------╪------------╪------------╪\n']
                channel2 = client.get_channel(752215115679662151)
                rMsgID = records[TeamName][4]
                for i in teamRosters[TeamName]:
                    print(teamRosters[TeamName][i][0])
                    if (len(i) < 16):    
                        rMsgList.append(i + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                    elif (len(i) >= 16):
                        rMsgList.append(i[0:15] + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                rMsg = ''.join(rMsgList)
                
                rMsgEdit = msg = await channel2.fetch_message(rMsgID)
                await rMsgEdit.edit(content="```" + rMsg + "```")

                with open('teamrosters.json', 'w') as tR:
                    json.dump(teamRosters, tR)
                with open('records.json', 'w') as r:
                    json.dump(records, r)
                with open('upcomingmatches.json', 'w') as uM:
                    json.dump(upcomingMatches, uM)
            else:
                await ctx.send("Player does not exist or is already a Captain")
        else:
            await ctx.send("Only captains can promote players") 
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

@client.command(pass_context=True)
async def demote(ctx, player: discord.Member):
    for i in list(teamRosters):
        if(ctx.message.author.display_name in teamRosters[i]):
            TeamName = i
    
    if(ctx.message.channel.name == 'commands'):    
        if(teamRosters[TeamName][ctx.message.author.display_name][1] == "Captain"):
            if(teamRosters[TeamName][str(player.nick)][1] == "Captain"):
                teamRosters[TeamName][str(player.nick)][1] = "Player"
                teamRosters[TeamName][str(player.nick)].remove(player.id)
                await ctx.send(str(player.nick) + " has been demoted to **Player** of " + TeamName)
                print(teamRosters)

                rMsgList =  ['***Roster for ' + TeamName + '***\n\nPlayerName     |           STEAMID          |     ROLE   | DATE ADDED |\n', '---------------╪----------------------------╪------------╪------------╪\n']
                channel2 = client.get_channel(752215115679662151)
                rMsgID = records[TeamName][4]
                for i in teamRosters[TeamName]:
                    print(teamRosters[TeamName][i][0])
                    if (len(i) < 16):    
                        rMsgList.append(i + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                    elif (len(i) >= 16):
                        rMsgList.append(i[0:15] + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                rMsg = ''.join(rMsgList)
                
                rMsgEdit = msg = await channel2.fetch_message(rMsgID)
                await rMsgEdit.edit(content="```" + rMsg + "```")

                with open('teamrosters.json', 'w') as tR:
                    json.dump(teamRosters, tR)
                with open('records.json', 'w') as r:
                    json.dump(records, r)
                with open('upcomingmatches.json', 'w') as uM:
                    json.dump(upcomingMatches, uM)
            else:
                ctx.send("Player does not exist or is already a Player")
        else:
            ctx.send("Only captains can demote players")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands") 

@client.command(pass_context=True)
async def playerremove(ctx, player):
    for i in list(teamRosters):
        if(ctx.message.author.name in teamRosters[i]):
            TeamName = i
    
    if(ctx.message.channel.name == 'commands'):
        if(teamRosters[TeamName][ctx.message.author.name][1] == "Captain"):    
            print(teamRosters)
            #player = (player, SteamID, role, dateAdded)
            if(TeamName in teamRosters):
                if(player in teamRosters[TeamName]):
                    await ctx.send("Player " + player + " ( " + teamRosters[TeamName][str(player)][0] + " ) has been successfully removed from " + TeamName)
                    del teamRosters[TeamName][player]
                    print(teamRosters)

                    rMsgList =  ['***Roster for ' + TeamName + '***\n\nPlayerName     |           STEAMID          |     ROLE   | DATE ADDED |\n', '---------------╪----------------------------╪------------╪------------╪\n']
                    channel2 = client.get_channel(752215115679662151)
                    rMsgID = records[TeamName][4]
                    for i in teamRosters[TeamName]:
                        print(teamRosters[TeamName][i][0])
                        if (len(i) < 16):    
                            rMsgList.append(i + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                        elif (len(i) >= 16):
                            rMsgList.append(i[0:15] + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
                    rMsg = ''.join(rMsgList)
                    
                    rMsgEdit = msg = await channel2.fetch_message(rMsgID)
                    await rMsgEdit.edit(content="```" + rMsg + "```")

                    with open('teamrosters.json', 'w') as tR:
                        json.dump(teamRosters, tR)
                    with open('records.json', 'w') as r:
                        json.dump(records, r)
                    with open('upcomingmatches.json', 'w') as uM:
                        json.dump(upcomingMatches, uM)
                    
                else:
                    await ctx.send("Player does not exist on team.. Maybe mistyped player name or SteamID")
            else:
                await ctx.send("No such team exists..")
        else:
            await ctx.send("You are not the Captain of this team.  Please let your Captain know a player needs to be removed from the roster..")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

@client.command(pass_context=True)
async def challenge(ctx, Team2, map1):
    alreadyPending = 0
    if(map1.lower() in mapList):    
        for i in list(teamRosters):
            if(ctx.message.author.display_name in teamRosters[i]):
                Team1 = i

        for i in list(upcomingMatches):
            if(Team1 in upcomingMatches[i]):
                alreadyPending = 1

        if (alreadyPending == 0):
            if(ctx.message.channel.name == 'commands'):    
                #teams = list(records)
                print(teams)
                challenger = Team1
                defender = Team2

                defenderIndex = teams.index(str(defender))
                challengerIndex = teams.index(str(challenger))

                for i in teams:
                    if (i in str(ctx.message.author.roles)):
                        teamCheck = i
                if(teamCheck == str(challenger)):
                    if(teamRosters[str(Team1)][ctx.message.author.display_name][1] == "Captain"):
                        if(Team2 not in records[Team1][3]):
                            print(defenderIndex)
                            print(challengerIndex)
                            if((defenderIndex < challengerIndex) and ((challengerIndex - defenderIndex) < 5)):
                                print(defenderIndex)
                                print(challengerIndex)
                                if(records[str(Team2)][2] == '🟡'):
                                    await ctx.message.channel.send(str(Team2) + " has a challenge pending")
                                elif(records[str(Team2)][2] == '🚫'):
                                    await ctx.message.channel.send(str(Team2) + " does not have 4 players on the roster yet")
                                elif(records[str(Team2)][2] == '⛔'):
                                    await ctx.message.channel.send(str(Team2) + " is suspended and can not challenge or be challenged")
                                elif(records[str(Team2)][2] == '🔵'):
                                    await ctx.message.channel.send(str(Team2) + " Has an upcoming match")
                                else:
                                    
                                    records[str(challenger)][2] = '🟡'
                                    records[str(defender)][2] = '🟡'

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
                                    upcomingMatches[match] = [1, map1, 'TBA', tiebreaker, str(Team1), str(Team2), 'TBA', 'TBA', dDay.day, dHour.hour, None]
                                    print(upcomingMatches[match][8])
                                    print(upcomingMatches[match][9])
                                    records[Team1][3] = Team2
                                    records[Team2][3] = Team1
                                    print(Team1)
                                    print(Team2)
                                    
                                    #uMsgList =  ['Defender │ Challenger │    Round 1 Map     │    Round 2 Map     │   Tiebreaker Map   │     Date    │     Time    │     Status   │\n---------╪------------╪--------------------╪--------------------╪--------------------╪-------------╪-------------╪--------------╪\n ']
                                    '''uMsgList = [str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4]
                                                +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                                +"\n Round 2 Map: " + upcomingMatches[i][2]
                                                +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                                +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][6])'''
                                    uMsgList = []

                                    uMsgList.append("\n\n" + str(upcomingMatches[match][5]) + " vs " + str(upcomingMatches[match][4] + "       **PENDING**"
                                                    +"\n\n Round 1 Map: " + upcomingMatches[match][1]
                                                    +"\n Round 2 Map: " + upcomingMatches[match][2]
                                                    +"\n Tiebreaker Map: " + upcomingMatches[match][3]
                                                    +"\n\n Date and Time: " + upcomingMatches[match][6] + " " + upcomingMatches[match][7]))

                                    uMsg = ''.join(uMsgList)
                                    
                                    channel2 = client.get_channel(752215154430574742)
                                    message = await channel2.send(content= "```" + uMsg + "```")

                                    upcomingMatches[match][10] = message.id

                                    for i in teamRosters[Team1]:
                                        if(teamRosters[Team1][i][1] == "Captain"):
                                            user = client.get_user(teamRosters[Team1][i][3])
                                            await user.send("You have challenged " + Team2 + " to a match on " + map1 + " with " + tiebreaker + " being the tiebreaker!  I will let you know when they accept.")
                                            #await user.send(user, "You have challenged " + Team2 + " to a match!") 
                                    for i in teamRosters[Team2]:    
                                        if(teamRosters[Team2][i][1] == "Captain"):
                                            user = client.get_user(teamRosters[Team2][i][3])
                                            await user.send(Team1 + " has challenged you to a match on " + map1 + " with " + tiebreaker + " being the tiebreaker!  Please !accept or !decline in the #commands channel")

                                await ctx.message.channel.send(str(challenger) + " has challenged " + str(defender) + " to a match!  The maps will be " + map1 + ", a map of " + str(Team2) + "'s choosing if they accept, and " + tiebreaker + " for the tiebreaker")

                                with open('teamrosters.json', 'w') as tR:
                                    json.dump(teamRosters, tR)
                                with open('records.json', 'w') as r:
                                    json.dump(records, r)
                                with open('upcomingmatches.json', 'w') as uM:
                                    json.dump(upcomingMatches, uM)
                                with open('rankings.json', 'w') as tR:
                                    json.dump(teams, tR)
                            
                            else:
                                await ctx.message.channel.send("You can only challenge teams at a higher rank than you..")
                        else:
                            await ctx.message.channel.send("You have just recently played or have been challenged by this team..")
                    else:
                        await ctx.message.channel.send("You are not the captain of " + str(Team1) + ".  Please advise your captain to challenge this team!")
                else:
                    await ctx.message.channel.send("You are not on that Team or you did the format wrong..")
            else:
                await ctx.message.author.send("Wrong channel.. please do the commands in #commands")
        else:
            await ctx.message.author.send("You already have an upcoming match!")
            await ctx.send("You already have an upcoming match!")
    else:
            await ctx.send(map1 + " is currently not an eligible map.  Please select another and try again..")
            
@client.command(pass_context=True)
async def accept(ctx, map2):
    for i in list(teamRosters):
        if(ctx.message.author.display_name in teamRosters[i]):
            Team1 = i
    if(map2 in mapList):
        if(ctx.message.channel.name == 'commands'):    
            if(teamRosters[str(Team1)][ctx.message.author.display_name][1] == "Captain"):
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
            for i in list(upcomingMatches):
                if(Team1 in i):
                    currentMatch = i
                #print(upcomingMatches[i])

            uMsgList.append("\n\n" + str(upcomingMatches[currentMatch][5]) + " vs " + str(upcomingMatches[currentMatch][4] + "       **PENDING**"
                            +"\n\n Round 1 Map: " + upcomingMatches[currentMatch][1]
                            +"\n Round 2 Map: " + upcomingMatches[currentMatch][2]
                            +"\n Tiebreaker Map: " + upcomingMatches[currentMatch][3]
                            +"\n\n Date and Time: " + upcomingMatches[currentMatch][6] + " " + upcomingMatches[currentMatch][7]))

            uMsg = ''.join(uMsgList)
                            
            channel2 = client.get_channel(752215154430574742)
            msg_id2 = upcomingMatches[currentMatch][10]
                            
            msg = await channel2.fetch_message(msg_id2)
            await msg.edit(content= "```" + uMsg + "```")

            with open('teamrosters.json', 'w') as tR:
                    json.dump(teamRosters, tR)
            with open('records.json', 'w') as r:
                    json.dump(records, r)
            with open('upcomingmatches.json', 'w') as uM:
                    json.dump(upcomingMatches, uM)
            with open('rankings.json', 'w') as tR:
                            json.dump(teams, tR)
        else:
            await ctx.message.author.send("Wrong channel.. please do the commands in #commands")
        if(upcomingMatches[currentMatch][0] == 2):
            for i in teamRosters[Team1]:
                if(teamRosters[Team1][i][1] == "Captain"):
                    user = client.get_user(teamRosters[Team1][i][3])
                    await user.send("```You have accepted the match vs " + str(upcomingMatches[currentMatch][4]) + " and the maps will be: \n"
                                    + "Round 1: " + upcomingMatches[currentMatch][1] + "\n" 
                                    + "Round 2: " + upcomingMatches[currentMatch][2] + "\n"
                                    + "Tiebreaker: " + upcomingMatches[currentMatch][3] + "\n  Next and final step is to set a Date and Time with the other team.```")                               
            
            Team2 = str(upcomingMatches[currentMatch][4])
            for i in teamRosters[Team2]:    
                if(teamRosters[Team2][i][1] == "Captain"):
                    user = client.get_user(teamRosters[Team2][i][3])
                    await user.send("```" + Team1 + " has accepted your challenge! The maps will be: \n"
                                    + "Round 1: " + upcomingMatches[currentMatch][1] + "\n" 
                                    + "Round 2: " + upcomingMatches[currentMatch][2] + "\n"
                                    + "Tiebreaker: " + upcomingMatches[currentMatch][3] + "\n  Next and final step is to set a Date and Time with the other team.```")
    else:
        await ctx.send(map2 + " is currently not in the map pool.  Please select another and try again..")

@client.command(pass_context=True)
async def decline(ctx):
    for i in list(teamRosters):
        if(ctx.message.author.name in teamRosters[i]):
            Team1 = i
    
    if(ctx.message.channel.name == 'commands'):    
        if(teamRosters[str(Team1)][ctx.message.author.name][1] == "Captain"):    
            for i in list(upcomingMatches):
                if (str(Team1) in i):
                    
                    currentList = i.split()
                    loser = Team1
                    currentList.remove(loser)
                    currentList.remove('vs')
                    winner = currentList[0]
                    winnerIndex = teams.index(winner)
                    loserIndex = teams.index(loser)
                    await ctx.send(loser + " has declined the challenge from " + winner)
                    if (winnerIndex > loserIndex):
                        newRank = teams.pop(winnerIndex)
                        teams.insert(loserIndex, newRank)

                    if(winnerIndex == 0):
                        await channel.send(str(winner) + " are the current **CHAMPIONS**")
                    
                    records[str(loser)][2] = '🟢'
                    records[str(winner)][2] = '🟢'

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
                                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))

                        else:
                            uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                                            +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                            +"\n Round 2 Map: " + upcomingMatches[i][2]
                                            +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))
                    uMsg = ''.join(uMsgList)
                            
                    channel2 = client.get_channel(752215154430574742)
                    msg_id2 = 752246430906712104
                            
                    msg = await channel2.fetch_message(msg_id2)
                    await msg.edit(content= "```" + uMsg + "```")

                    with open('teamrosters.json', 'w') as tR:
                        json.dump(teamRosters, tR)
                    with open('records.json', 'w') as r:
                        json.dump(records, r)
                    with open('upcomingmatches.json', 'w') as uM:
                        json.dump(upcomingMatches, uM)
                    with open('rankings.json', 'w') as tR:
                            json.dump(teams, tR)

            for i in teamRosters[loser]:
                if(teamRosters[loser][i][1] == "Captain"):
                    user = client.get_user(teamRosters[loser][i][3])
                    await user.send("```You have declined the match against " + winner + "```")                          
            
            for i in teamRosters[winner]:    
                if(teamRosters[winner][i][1] == "Captain"):
                    user = client.get_user(teamRosters[winner][i][3])
                    await user.send("```" + loser + " has declined your challenge```")

        else:
            ctx.send("You are not the captain of this team..")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")
            
@client.command(pass_context=True)
async def results(ctx, Team1, score1: int, Team2: discord.Role, score2: int, writeup = "No match write-up available", r1logs = "None", r2logs = "None", r3logs = "None"):
    if(ctx.message.channel.name == 'commands'):    
        if(teamRosters[Team1][ctx.message.author.display_name][1] == "Captain"):
            global bMsg

            for i in list(upcomingMatches):
                if(Team1 in i):
                    #resultable = 1
                    currentMatch = i        
            
            if (upcomingMatches[currentMatch][0] == 3):    
                channel = client.get_channel(752274967973986326)    
                if (score1 > score2):
                    winner = Team1
                    loser = Team2
                    winningscore = str(score1)
                    losingscore = str(score2)
                else:
                    winner = Team2
                    winningscore = str(score2)
                    loser = Team1
                    losingscore = str(score1)
                
                
                matchHistory[currentMatch] = [str(winner), str(winningscore), str(loser), str(losingscore), "None", "None", "None", "No Writeup Available", None]

                match = await channel.send("```" + "Match ID: "
                                            + "\n\nWinner: " + str(winner)
                                            + "\nLoser: " + str(loser)
                                            + "\n\nRound 1 Logs: " + matchHistory[currentMatch][4]
                                            + "\nRound 2 Logs: " + matchHistory[currentMatch][5]
                                            + "\nRound 3 Logs: " + matchHistory[currentMatch][6]
                                            + "\n\n" + matchHistory[currentMatch][7] + "```")

                matchHistory[currentMatch][8] = match.id

                msg = await channel.fetch_message(matchHistory[currentMatch][8])
                await msg.edit(content = "```" + "Match ID: " + str(matchHistory[currentMatch][8])
                                            + "\n\nWinner: " + str(winner)
                                            + "\nLoser: " + str(loser)
                                            + "\n\nRound 1 Logs: " + matchHistory[currentMatch][4]
                                            + "\nRound 2 Logs: " + matchHistory[currentMatch][5]
                                            + "\nRound 3 Logs: " + matchHistory[currentMatch][6]
                                            + "\n\n" + matchHistory[currentMatch][7] + "```")



                winnerIndex = teams.index(str(winner))
                loserIndex = teams.index(str(loser))
                    
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

                channel2 = client.get_channel(752215154430574742)
                msg_id2 = upcomingMatches[currentMatch][10]
                                
                msg = await channel2.fetch_message(msg_id2)
                await msg.delete()

                del upcomingMatches[currentMatch]
                    

            else:
                await ctx.message.author.send("You do not have any SCHEDULED matches..")
                await ctx.send(Team1 + " does not have any SCHEDULED matches..")
            
            with open('teamrosters.json', 'w') as tR:
                json.dump(teamRosters, tR)
            with open('records.json', 'w') as r:
                json.dump(records, r)
            with open('upcomingmatches.json', 'w') as uM:
                json.dump(upcomingMatches, uM)
            with open('rankings.json', 'w') as tR:
                json.dump(teams, tR)
            with open('matchhistory.json', 'w') as mH:
                json.dump(matchHistory, mH)
        else:
            await ctx.send("Only Captains can report results")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

#matchHistory[currentMatch] = [winner, winningscore, loser, losingscore, "None", "None", "None", "No Writeup Available", None]
@client.command(pass_context=True)
async def writeup(ctx, matchID, writeup):
    if(ctx.message.channel.name == 'commands'):   
        for i in list(teamRosters):
                if(ctx.message.author.display_name in teamRosters[i]):
                    Team1 = i
        for i in list(matchHistory):
            print(i)
            if(Team1 in i):
                currentMatch = i

        if(teamRosters[Team1][ctx.message.author.display_name][1] == "Captain"):
            if (len(writeup) < 1001):    
                channel = client.get_channel(752274967973986326)
                msgid = int(matchID)

                msg = await channel.fetch_message(msgid)

                matchHistory[currentMatch][7] = writeup

                await msg.edit(content = "```" + "Match ID: " + matchID
                                                + "\n\nWinner: " + matchHistory[currentMatch][0]
                                                + "\nLoser: " + matchHistory[currentMatch][2]
                                                + "\n\nRound 1 Logs: " + matchHistory[currentMatch][4]
                                                + "\nRound 2 Logs: " + matchHistory[currentMatch][5]
                                                + "\nRound 3 Logs: " + matchHistory[currentMatch][6]
                                                + "\n\n" + matchHistory[currentMatch][7] + "```")

                with open('matchhistory.json', 'w') as mH:
                    json.dump(matchHistory, mH)
            else:
                ctx.send("Writeup not submitted.  Your write was " + len(writeup) + "characters long and the limit is 1000")
        else:
            ctx.send("Only Captains of the match played can add a writeup..")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

@client.command(pass_context=True)
async def matchlogs(ctx, matchID, log1 = "None", log2 = "None", log3 = "None"):
    print(matchHistory)
    if(ctx.message.channel.name == 'commands'):   
        for i in list(teamRosters):
                if(ctx.message.author.display_name in teamRosters[i]):
                    Team1 = i
        for i in list(matchHistory):
            print(i)
            if(Team1 in i):
                currentMatch = i
        if(teamRosters[Team1][ctx.message.author.display_name][1] == "Captain"):    
            channel = client.get_channel(752274967973986326)
            msgid = int(matchID)

            msg = await channel.fetch_message(msgid)

            matchHistory[currentMatch][4] = log1
            matchHistory[currentMatch][5] = log2  
            matchHistory[currentMatch][6] = log3

            await msg.edit(content = "```" + "Match ID: " + matchID
                                            + "\n\nWinner: " + matchHistory[currentMatch][0]
                                            + "\nLoser: " + matchHistory[currentMatch][2]
                                            + "\n\nRound 1 Logs: " + matchHistory[currentMatch][4]
                                            + "\nRound 2 Logs: " + matchHistory[currentMatch][5]
                                            + "\nRound 3 Logs: " + matchHistory[currentMatch][6]
                                            + "\n\n" + matchHistory[currentMatch][7] + "```")

            with open('matchhistory.json', 'w') as mH:
                json.dump(matchHistory, mH)
        else:
            ctx.send("Only Captains of the match played can add logs..")
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")



@client.command(pass_context=True)
async def removeteam(ctx, TeamName: discord.Role):
    
    if(ctx.message.channel.name == 'commands'):    
        if(teamRosters[str(TeamName)][ctx.message.author.display_name][1] == "Captain"):
            del teamRosters[str(TeamName)]
            del records[str(TeamName)]
            teams.remove(str(TeamName))
            print(teamRosters)
            await TeamName.delete()
        else:
            await ctx.send("You are not the captain of this team..")

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

        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
        with open('rankings.json', 'w') as tR:
            json.dump(teams, tR)
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

'''@client.command(pass_context=True)
async def roster(ctx, TeamName):
    if(ctx.message.channel.name == 'commands'):    
        #rosters = list(teamRosters)
        bMsgList =  ['***Roster for ' + TeamName + '***\n\nPlayerName     |           STEAMID          |     ROLE   | DATE ADDED |\n', '---------------╪----------------------------╪------------╪------------╪\n']

        channel = client.get_channel(752215115679662151)

        for i in teamRosters[TeamName]:
            print(i)
            print(teamRosters[TeamName][i][0])
            if (len(i) < 16):    
                bMsgList.append(i + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
            elif (len(i) >= 16):
                bMsgList.append(i[0:15] + " " * (15 - len(i)) + '│ ' + str(teamRosters[TeamName][i][0]) + " " * (27 - len(str(teamRosters[TeamName][i][0]))) + "│ " + str(teamRosters[TeamName][i][1]) + " " * (11 - len(str(teamRosters[TeamName][i][1]))) + "│ "  + str(teamRosters[TeamName][i][2]) + " " * (11 - len(str(teamRosters[TeamName][i][2]))) + "│\n")
            bMsg = ''.join(bMsgList)
            #print(teamRosters[TeamName])

        await channel.send(content="```" + bMsg + "```")

        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")'''

@client.command(pass_context=True)
async def schedulematch(ctx, date, time):
    for i in list(teamRosters):
        if(ctx.message.author.display_name in teamRosters[i]):
            Team1 = i
    
    if(ctx.message.channel.name == 'commands'):    
        if(teamRosters[str(Team1)][ctx.message.author.display_name][1] == "Captain"):
            for i in list(upcomingMatches):
                if (str(Team1) in i):
                    currentMatch = i
            
            upcomingMatches[currentMatch][6] = date
            upcomingMatches[currentMatch][7] = time
            upcomingMatches[currentMatch][0] = 3

            uMsgList = []

            uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                            +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                            +"\n Round 2 Map: " + upcomingMatches[i][2]
                             +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))

                   
            uMsg = ''.join(uMsgList)
                        
            channel2 = client.get_channel(752215154430574742)
            msg_id2 = upcomingMatches[currentMatch][10]
                        
            msg = await channel2.fetch_message(msg_id2)
            await msg.edit(content= "```" + uMsg + "```")

            
            if(Team1 == str(upcomingMatches[currentMatch][4])):
                Team2 = str(upcomingMatches[currentMatch][5])
            elif(Team1 == str(upcomingMatches[currentMatch][5])):
                Team2 = str(upcomingMatches[currentMatch][4])
            
            for i in teamRosters[Team1]:
                if(teamRosters[Team1][i][1] == "Captain"):
                    user = client.get_user(teamRosters[Team1][i][3])
                    await user.send("```Your match with " + Team2 + " will be on " + upcomingMatches[currentMatch][6] + " at " + upcomingMatches[currentMatch][7] + "```")                              
            
            #Team2 = str(upcomingMatches[currentMatch][4])
            for i in teamRosters[Team2]:    
                if(teamRosters[Team2][i][1] == "Captain"):
                    user = client.get_user(teamRosters[Team2][i][3])
                    await user.send("```Your match with " + Team1 + " will be on " + upcomingMatches[currentMatch][6] + " at " + upcomingMatches[currentMatch][7] + "```")
            print(Team2)
            records[Team2][2] = '🔵'
            records[Team1][2] = '🔵'

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

        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

@client.command(pass_context=True)
async def setTeamColor(ctx, TeamName: discord.Role, color):
    if(ctx.message.channel.name == 'commands'):    
        if(teamRosters[str(TeamName)][ctx.message.author.display_name][1] == "Captain"):
            await TeamName.edit(colour=discord.Colour(randomColor[color]))
    


#ADMIN COMMANDS

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.send("Restarting the bot..")
    print(sys.executable)
    print(['python'] + sys.argv)
    os.execv(sys.executable, ['python'] + sys.argv) 

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def reinstate(ctx, Team):
    if(records[str(Team)][2] == '⛔'):
        if(len(teamRosters[Team]) >= 4):
            records[str(Team)][2] = '🟢'
        else:
            records[str(Team)][2] = '🚫' 

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

        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
    else:
        await ctx.send("This team was never suspended...")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
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

        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
    else:
        await ctx.message.author.send("Wrong channel.. please do the commands in #commands")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def suspend(ctx, Team):
    
    records[str(Team)][2] = '⛔'

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

    with open('teamrosters.json', 'w') as tR:
        json.dump(teamRosters, tR)
    with open('records.json', 'w') as r:
        json.dump(records, r)
    with open('upcomingmatches.json', 'w') as uM:
        json.dump(upcomingMatches, uM)

@client.command(pass_context=True)
async def admin_removeteam(ctx, TeamName):
    if(ctx.message.author.guild_permissions.administrator):
        del teamRosters[str(TeamName)]
        del records[str(TeamName)]
        teams.remove(str(TeamName))
        print(teamRosters)
        #await TeamName.delete()
    else:
        await ctx.send("You are not the captain of this team..")

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

    with open('teamrosters.json', 'w') as tR:
        json.dump(teamRosters, tR)
    with open('records.json', 'w') as r:
        json.dump(records, r)
    with open('upcomingmatches.json', 'w') as uM:
        json.dump(upcomingMatches, uM)
    with open('rankings.json', 'w') as tR:
        json.dump(teams, tR)

@client.command(pass_context=True)
async def admin_results(ctx, Team1: discord.Role, score1: int, Team2: discord.Role, score2: int):
    if(ctx.message.author.guild_permissions.administrator):
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
                                +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))

            else:
                uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                                +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                +"\n Round 2 Map: " + upcomingMatches[i][2]
                                +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))
            uMsg = ''.join(uMsgList)
                    
        channel2 = client.get_channel(752215154430574742)
        msg_id2 = 752246430906712104
                    
        msg = await channel2.fetch_message(msg_id2)
        await msg.edit(content= "```" + uMsg + "```")

        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
        with open('rankings.json', 'w') as tR:
            json.dump(teams, tR)
    else:
        await ctx.send("Only Captains can report results")

@client.command(pass_context=True)
async def admin_decline(ctx, Team1):
    if(ctx.message.author.guild_permissions.administrator):    
        for i in list(upcomingMatches):
            if (str(Team1) in i):
                
                currentList = i.split()
                loser = Team1
                currentList.remove(loser)
                currentList.remove('vs')
                winner = currentList[0]
                winnerIndex = teams.index(winner)
                loserIndex = teams.index(loser)
                await ctx.send(loser + " has declined the challenge from " + winner)
                if (winnerIndex > loserIndex):
                    newRank = teams.pop(winnerIndex)
                    teams.insert(loserIndex, newRank)

                if(winnerIndex == 0):
                    await channel.send(str(winner) + " are the current **CHAMPIONS**")
                
                records[str(loser)][2] = '🟢'
                records[str(winner)][2] = '🟢'

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
                                        +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))

                    else:
                        uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + "vs" + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                                        +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                        +"\n Round 2 Map: " + upcomingMatches[i][2]
                                        +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                        +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))
                uMsg = ''.join(uMsgList)
                        
                channel2 = client.get_channel(752215154430574742)
                msg_id2 = 752246430906712104
                        
                msg = await channel2.fetch_message(msg_id2)
                await msg.edit(content= "```" + uMsg + "```")

        for i in teamRosters[loser]:
            if(teamRosters[loser][i][1] == "Captain"):
                user = client.get_user(teamRosters[loser][i][3])
                await user.send("```You have declined the match against " + winner + "```")                          
        
        for i in teamRosters[winner]:    
            if(teamRosters[winner][i][1] == "Captain"):
                user = client.get_user(teamRosters[winner][i][3])
                await user.send("```" + loser + " has declined your challenge```")
        
        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
        with open('rankings.json', 'w') as tR:
            json.dump(teams, tR)

    else:
        ctx.send("You are not the captain of this team..")

@client.command(pass_context=True)
async def admin_default(ctx, Team1):
    if(ctx.message.author.guild_permissions.administrator):    
        for i in list(upcomingMatches):
            if (str(Team1) in i):
                
                currentList = i.split()
                loser = Team1
                currentList.remove(loser)
                currentList.remove('vs')
                winner = currentList[0]
                winnerIndex = teams.index(winner)
                loserIndex = teams.index(loser)
                await ctx.send(loser + " have been forced a default vs " + winner)
                if (winnerIndex > loserIndex):
                    newRank = teams.pop(winnerIndex)
                    teams.insert(loserIndex, newRank)

                if(winnerIndex == 0):
                    await channel.send(str(winner) + " are the current **CHAMPIONS**")
                
                records[str(loser)][2] = '🟢'
                records[str(winner)][2] = '🟢'

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
                                        +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))

                    else:
                        uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + "vs" + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                                        +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                        +"\n Round 2 Map: " + upcomingMatches[i][2]
                                        +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                        +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))
                uMsg = ''.join(uMsgList)
                        
                channel2 = client.get_channel(752215154430574742)
                msg_id2 = 752246430906712104
                        
                msg = await channel2.fetch_message(msg_id2)
                await msg.edit(content= "```" + uMsg + "```")

        for i in teamRosters[loser]:
            if(teamRosters[loser][i][1] == "Captain"):
                user = client.get_user(teamRosters[loser][i][3])
                await user.send("```You have declined the match against " + winner + "```")                          
        
        for i in teamRosters[winner]:    
            if(teamRosters[winner][i][1] == "Captain"):
                user = client.get_user(teamRosters[winner][i][3])
                await user.send("```" + loser + " has declined your challenge```")
        
        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
        with open('rankings.json', 'w') as tR:
            json.dump(teams, tR)

    else:
        ctx.send("You are not the captain of this team..")

@client.command(pass_context=True)
async def admin_accept(ctx, Team1, map2):
    if(ctx.message.author.guild_permissions.administrator):
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
    for i in list(upcomingMatches):
        if(Team1 in i):
            currentMatch = i
        #print(upcomingMatches[i])
        if(upcomingMatches[i][0] == 0):
            uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "       **PENDING**"
                            +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                            +"\n Round 2 Map: " + upcomingMatches[i][2]
                            +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))

        else:
            uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                            +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                            +"\n Round 2 Map: " + upcomingMatches[i][2]
                            +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                            +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))

        uMsg = ''.join(uMsgList)
                    
        channel2 = client.get_channel(752215154430574742)
        msg_id2 = 752246430906712104
                    
        msg = await channel2.fetch_message(msg_id2)
        await msg.edit(content= "```" + uMsg + "```")

    if(upcomingMatches[currentMatch][0] == 2):
        for i in teamRosters[Team1]:
            if(teamRosters[Team1][i][1] == "Captain"):
                user = client.get_user(teamRosters[Team1][i][3])
                await user.send("```You have accepted the match vs " + str(upcomingMatches[currentMatch][4]) + " and the maps will be: \n"
                                + "Round 1: " + upcomingMatches[currentMatch][1] + "\n" 
                                + "Round 2: " + upcomingMatches[currentMatch][2] + "\n"
                                + "Tiebreaker: " + upcomingMatches[currentMatch][3] + "\n  Next and final step is to set a Date and Time with the other team.```")                               
        
        Team2 = str(upcomingMatches[currentMatch][4])
        for i in teamRosters[Team2]:    
            if(teamRosters[Team2][i][1] == "Captain"):
                user = client.get_user(teamRosters[Team2][i][3])
                await user.send("```" + Team1 + " has accepted your challenge! The maps will be: \n"
                                + "Round 1: " + upcomingMatches[currentMatch][1] + "\n" 
                                + "Round 2: " + upcomingMatches[currentMatch][2] + "\n"
                                + "Tiebreaker: " + upcomingMatches[currentMatch][3] + "\n  Next and final step is to set a Date and Time with the other team.```")
    with open('teamrosters.json', 'w') as tR:
        json.dump(teamRosters, tR)
    with open('records.json', 'w') as r:
        json.dump(records, r)
    with open('upcomingmatches.json', 'w') as uM:
        json.dump(upcomingMatches, uM)
    with open('rankings.json', 'w') as tR:
        json.dump(teams, tR)

@client.command(pass_context=True)
async def admin_playeradd(ctx, TeamName, player, SteamID):
    if(ctx.message.author.guild_permissions.administrator):    
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

        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
    else:
        await ctx.send("You are not the Captain of this team.  Please let your Captain know a player needs to be added to the roster..")

@client.command(pass_context=True)
async def admin_demote(ctx, TeamName, player: discord.User):
    if(ctx.message.author.guild_permissions.administrator):
        if(teamRosters[TeamName][str(player.display_name)][1] == "Captain"):
            teamRosters[TeamName][str(player.display_name)][1] = "player"
            teamRosters[TeamName][str(player.display_name)].remove(player.id)
            await ctx.send(str(player.display_name) + " has been demoted to **Player** of **auto!**")
            print(teamRosters)
            with open('teamrosters.json', 'w') as tR:
                json.dump(teamRosters, tR)
            with open('records.json', 'w') as r:
                json.dump(records, r)
            with open('upcomingmatches.json', 'w') as uM:
                json.dump(upcomingMatches, uM)
        else:
            ctx.send("Player does not exist or is already a Player")
        
        
        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)
    else:
        ctx.send("Only captains can demote players") 

@client.command(pass_context=True)
async def admin_promote(ctx, TeamName, player: discord.User):
    if(ctx.message.author.guild_permissions.administrator):
        if(teamRosters[TeamName][str(player.display_name)][1] == "Player"):
            teamRosters[TeamName][str(player.display_name)][1] = "Captain"
            teamRosters[TeamName][str(player.display_name)].append(player.id)
            await ctx.send(str(player.display_name) + " has been promoted to **Captain** of **auto!**")
            print(teamRosters)
        else:
            ctx.send("Player does not exist or is already a Captain")
        
        
        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)

    else:
        ctx.send("Only captains can promote players")

@client.command(pass_context=True)
async def admin_schedulematch(ctx, Team1, date, time):
    if(ctx.message.author.guild_permissions.administrator):
        for i in list(upcomingMatches):
            if (str(Team1) in i):
                upcomingMatches[i][6] = date
                upcomingMatches[i][7] = time

                uMsgList = []
        for i in upcomingMatches:
            #print(upcomingMatches[i])
            if(upcomingMatches[i][0] == 0):
                uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "       **PENDING**"
                                +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                +"\n Round 2 Map: " + upcomingMatches[i][2]
                                +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))

            else:
                uMsgList.append("\n\n" + str(upcomingMatches[i][5]) + " vs " + str(upcomingMatches[i][4] + "          **SCHEDULED**"
                                +"\n\n Round 1 Map: " + upcomingMatches[i][1]
                                +"\n Round 2 Map: " + upcomingMatches[i][2]
                                +"\n Tiebreaker Map: " + upcomingMatches[i][3]
                                +"\n\n Date and Time: " + upcomingMatches[i][6] + " " + upcomingMatches[i][7]))
            uMsg = ''.join(uMsgList)
                    
        channel2 = client.get_channel(752215154430574742)
        msg_id2 = 752246430906712104
                    
        msg = await channel2.fetch_message(msg_id2)
        await msg.edit(content= "```" + uMsg + "```")

        for i in list(upcomingMatches):
            if(Team1 in i):
                currentMatch = i
        Team2 = str(upcomingMatches[currentMatch][4])
        for i in teamRosters[Team1]:
            if(teamRosters[Team1][i][1] == "Captain"):
                user = client.get_user(teamRosters[Team1][i][3])
                await user.send("```Your match with " + Team2 + " will be on " + upcomingMatches[currentMatch][6] + " at " + upcomingMatches[currentMatch][7] + "```")                              
        
        Team2 = str(upcomingMatches[currentMatch][4])
        for i in teamRosters[Team2]:    
            if(teamRosters[Team2][i][1] == "Captain"):
                user = client.get_user(teamRosters[Team2][i][3])
                await user.send("```Your match with " + Team1 + " will be on " + upcomingMatches[currentMatch][6] + " at " + upcomingMatches[currentMatch][7] + "```")

        with open('teamrosters.json', 'w') as tR:
            json.dump(teamRosters, tR)
        with open('records.json', 'w') as r:
            json.dump(records, r)
        with open('upcomingmatches.json', 'w') as uM:
            json.dump(upcomingMatches, uM)


@client.command(pass_context = True)
async def clear(ctx):
    await ctx.message.channel.delete_messages(ctx)
    #await ctx.send("Deleted messages")      

@client.command(pass_context=True)
async def setColor(ctx, rolename: discord.Role, color):
    if(ctx.message.author.guild_permissions.administrator):
        await rolename.edit(colour=discord.Colour(randomColor[color]))

@client.command(pass_context=True)
async def test(ctx, TeamName = None):
    bMsgList =  ['Rank│ Team Name    W     L   Status  \n', '----╪-----------╪-----╪-----╪----\n']
    bEnumList = list(enumerate(teams, start = 1))
    for i in range(len(bEnumList)):
        if(len(bEnumList[i][1]) < 11):
            bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + bEnumList[i][1] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
        elif (len(bEnumList[i][1]) >= 11):
            bMsgList.append(" " + str(bEnumList[i][0]) + " " * (1 - len(str(bEnumList[i][0]))) + "  │ " + (bEnumList[i][1])[0:10] + (" " * (10 - len(bEnumList[i][1]))) + "│  " + str(records[bEnumList[i][1]][0]) + (" " * (3 - len(str(records[bEnumList[i][1]][0]))))  + "│  " + str(records[bEnumList[i][1]][1]) + (" " * (3 - len(str(records[bEnumList[i][1]][1])))) + "│ " + records[bEnumList[i][1]][2] + "\n")
    bMsg = ''.join(bMsgList)

    await ctx.send("```" + bMsg + "```")

#timertest.before_loop(client.wait_until_ready())    
#timertest.start()
client.loop.create_task(check_Expired_Challenges())
client.run('TOKEN') #input your discord token here.  Keep the quotations
