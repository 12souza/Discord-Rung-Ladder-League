import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
import datetime

client = commands.Bot(command_prefix = "!")


teams = ['auto!', 'TnS,', 'St4ck', 'hello!?']
teamRosters = {'TnS' : [('joe', 'steamid:0:0:1'), ('jane', 'STEAMID::0:0:2')],
               'auto!': [('bert', 'steamid:0:0:4'), ('ernie', 'STEAMID::0:0:3')]}
upcomingMatchs = {}
records = {'TnS': [0, 0, 0, 2],
             'auto!': [0, 0, 0, 4],
             'St4Ck': [0, 0, 0, 1],
             'cc:': [0, 0, 0, 3],
             'Sn#': [0, 0, 0, 5],} # W, L, Status (0 for open (green light), 1 for pending and scheduled (red light), 2 for suspended (yellow light).), placement on standings
standings = []


@client.command(pass_context=True)
async def createteam(ctx, TeamName, TeamCaptain, SteamID):
    if(TeamName in teamRosters):
        await ctx.send("Sorry that team already exists..")
    else:
        teamRosters[TeamName] = [(TeamCaptain, SteamID)]
        print(teamRosters)
        await ctx.guild.create_role(name= TeamName, hoist=True)
        playerAdd = discord.utils.get(ctx.message.guild.roles, name=TeamName)
        await ctx.message.author.add_roles(playerAdd)

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
            player = (player, SteamID)
            teamRosters[TeamName].append(player)
            print(teamRosters)
            playerAdd = discord.utils.get(ctx.message.guild.roles, name=TeamName)
            await ctx.message.author.add_roles(playerAdd)
            await ctx.send(player + " ( " + SteamID + " ) has been successfully added to " + TeamName)
        else:
            await ctx.send("Player is already assigned to a team..")

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
    
    records[str(challenger)][2] = 1
    records[str(defender)][2] = 1

@client.command(pass_context=True)
async def results(ctx, Team1: discord.Role, score1: int, Team2: discord.Role, score2: int):
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

    if(winner.position == champion):
        await ctx.message.channel.send(str(winner) + " are the current **CHAMPIONS**")

    records[str(winner)][0] += 1 #add one to the wins column
    records[str(loser)][1] += 1 #add one to the loss column

    records[str(loser)][2] = 0
    records[str(winner)][2] = 0

'''Just using this as a test so i dont have to pass a lot of parameters.. want to build this into results, and decline commands.  Just to update standings
Trying to take all of the dictionary keys to a list.. then iterate through the list and get them to access discord.Role to get the discord role position in the server...
then finally iterate back through the records dictionary and update their placement on the server equal with the placement on the standings.  Biggest problem is the server role position
counts the bottom position as 0 and the top position as the highest number of roles - (the amount of non-team admin roles).  So the final number for assignment is going to have to be 
the abs(len(allRoles) - number of non-team roles).. i.position is not returning an integer where was winner.position and loser.position in !results does'''

@client.command(pass_context=True)
async def test(ctx):
    key_list = list(records)
    print(key_list)

    for i in key_list:
        print(i)
        i = discord.Role
        print(i.position)


@client.command(pass_context=True)
async def removeteam(ctx, TeamName: discord.Role):
    if(ctx.message.author == teamRosters[str(TeamName.name)][0][0]):
        del teamRosters[str(TeamName.name)]
        print(teamRosters)
        await TeamName.delete()
    else:
        await ctx.send("You are not the captain of this team..")


client.run('TOKEN') #input your discord token here.  Keep the quotations