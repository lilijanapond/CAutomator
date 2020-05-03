#the thing
import discord
from discord.ext import commands
from discord.utils import get

from tinydb import TinyDB, Query
db = TinyDB('db.json')

#the other thing
import os

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import csv
import re

def read_cell(row, col): # Getting name of entry. Thanks @GradyDal on Repl.it
	with open('speeds.csv', 'r') as f:
		data=list(csv.reader(f))
		return(data[int(row)][int(col)])

testing = False
linecount = 0
lvl30ID = 547360918930194443

bot = commands.Bot(command_prefix='-')

#the code
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='-help'))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global testing
    global linecount
    if message.author.bot: return #avoid every bots instead of only itself

    if(not message.content.startswith('-')): return

    args = message.content.split()
    args.pop(0) # removes the command from arguments

    if message.content.startswith('-about'):
        await message.channel.send(file=discord.File('cautomator.png'))
        await message.channel.send('> :wave: > **Hello! I am CAutomator, the Calculated Anarchy Automator!**\nI am a bot built by @Hyperfresh#8080, tasked to automate some tasks and make things a little easier on this server!\nYou can find more information on my GitHub: https://github.com/Hyperfresh8080/CAutomator\n Also, thanks to https://github.com/iwaQwQ for some errands :)')

    if message.content.startswith('-thankshy'):
        await message.channel.send("My creator told me to say \"you're welcome\" :)")

    if message.content.startswith('-help'):
        await message.channel.send("> **Help**\n `-speed`: See how fast my host's network is!\n `-abspeed`: Tells you some info about the `-speed` command.\n `-help`: This command!\n `-about`: Tells you some info about me!\n `-whoami`: Tells you who you are!\n `-role`: **Level 30+ only**: Add or edit your custom role: `-role <name> <colour>`\n `-delrole`: **Level 30+ only**: Delete your custom role")
    if message.content.startswith('-whoami'):
        await message.channel.send("You are " + str(message.author))

    if message.content.startswith('-shutdown'):
        if str(message.author) == 'Hyperfresh#8080':
            await message.channel.send(':wave: > Shut down at hyperfresh.ddns.net:7777, ' + str(message.author) + '!')
        else:
            await message.channel.send(':x: > Nice try, ' + str(message.author) + ". <:squinteyes:563998593460076544>")

    if message.content.startswith('-abspeed'):
        speedabout = '''**Speedtest CLI by Ookla** (speedtest.exe) is the official command line client for testing the speed and performance of an internet connection, provided by Ookla.
Your use of this command (speed) is subject to the Speedtest End User License Agreement, Terms of Use and Privacy Policy at these URLs:
        https://www.speedtest.net/about/eula
        https://www.speedtest.net/about/terms
        https://www.speedtest.net/about/privacy
        '''
        await message.channel.send(str(speedabout))

# ATT - The following code won't work unless you have Speedtest CLI installed somewhere
# Okay... this is a lil janky so hear me out.
# The reason why I did it the way I did it was because this was the most "efficient" way.
# There's definitely other ways but with CMD Batch, implying /wait will uh do thing
# Code will be optimised later
    if message.content.startswith('-speed'):
        speeder = open("inprocess.txt", 'r')
        for line in speeder:
            if 'Process' in line:
                count = open('speeds.csv','r')
                lines = 0
                for line in count:
                    lines = lines + 1
                count.close
                if lines == linecount:
                    speeder.close
                    print('SPEED TEST REQUESTED BUT DENIED - IN PROCESS')
                    await message.channel.send("> :x: > **I'm still testing speed!**\n Please wait a bit longer.")           
                else:
                    speeder.close
                    downspeed = int(read_cell(lines-1,5))
                    upspeed = int(read_cell(lines-1,6))
                    downspeed = float(downspeed/100000)
                    upspeed = float(upspeed/100000)
                    downspeed = round(downspeed,2)
                    upspeed = round(upspeed,2)
                    await message.channel.send('> :white_check_mark: > **Results**\nServer: **' + read_cell(lines-1, 0) + '**\nPing: **' + read_cell(lines-1,2) + " ms**\nDownload: **" + str(downspeed) + " Mbps**\nUpload: **" + str(upspeed) + " Mbps**\n\n*Conducted using Ookla's Speedtest CLI: https://speedtest.net\nSpeeds are converted from bits to megabits, and rounded to two decimal places.*")
                    speeder = open('inprocess.txt','w')
                    speeder.write('Idle')
                    speeder.close

            elif 'Idle' in line:
                linecount = 0
                speeder.close
                count = open('speeds.csv','r')
                lines = 0
                for line in count:
                    lines = lines + 1
                count.close
                linecount = lines
                await message.channel.send('> :bullettrain_side: > **Testing speed...**\nRun this command again in two minutes to see results!')
                print('SPEED TEST REQUESTED:')
                print(os.system('speed.cmd'))

    if message.content.startswith('-role'):
        member = message.author
        if(lvl30ID in member.roles): # check if the member has level 30 role


            User = Query()
            result = db.search(User.memberId == member.id)

            if(len(result) == 1):
                # edit role name
                roleName = ""
                for x in range(0, len(args)-1):
                    roleName = roleName + args[x] + " "

                hexColorMatch = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args[len(args)-1])

                if hexColorMatch:
                    roleColour = discord.Colour(int(args[len(args)-1][1:], 16))
                    print('ROLE CHANGE REQUESTED for ' + member.name + "#" + member.discriminator + ': ' + str(roleName) + ' with colour ' + str(roleColour))
                    role = message.guild.get_role(result[0]['roleId'])
                    await role.edit(name=roleName, colour=roleColour)
                    await message.channel.send("> :white_check_mark: > **Role edited**\n<@{0}>, I edited your role **<@&{1}>**".format(message.author.id, role.id))
                else:
                    print('ROLE CHANGE REQUESTED for ' + member.name + "#" + member.discriminator + ': ' + str(roleName) + ' without colour change')
                    role = message.guild.get_role(result[0]['roleId'])
                    roleName = roleName + args[len(args)-1]
                    await role.edit(name=roleName)
                    await message.channel.send("> :white_check_mark: > **Role edited**\n<@{0}>, I edited your role **<@&{1}>**".format(message.author.id, role.id))
            # edit role colour
            else:
                roleName = ""
                for x in range(0, len(args)-1):
                    roleName = roleName + args[x] + " "

                hexColorMatch = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args[len(args)-1])

                if hexColorMatch:
                    roleColour = discord.Colour(int(args[len(args)-1][1:], 16))
                    print('ROLE CHANGE REQUESTED for ' + member.name + "#" + member.discriminator + ': ' + str(roleName) + ' with colour ' + str(roleColour))
                    role = await message.guild.create_role(name=roleName, colour=roleColour)
                    await member.add_roles(role)
                    db.insert({'memberId': member.id, 'roleId': role.id})
                    await message.channel.send("> :white_check_mark: > **Role given**\n<@{0}>, I gave you the role **<@&{1}>**".format(message.author.id, role.id))
                else:
                    await message.channel.send("> :x: > **Something went wrong**\n <@{.author.id}>, the colour hex code you entered is incorrect!".format(message))
        else:
            await message.channel.send("> :x: > **You can't do that**\nThis is for Level 30+ use only.")

    if message.content.startswith('-delrole'):
        member = message.author
        if(lvl30ID in member.roles): # check if the member has level 30 role

            User = Query()
            result = db.search(User.memberId == member.id)

            if(len(result) == 1):

                print('ROLE DELETION REQUESTED for ' + member.name + "#" + member.discriminator)

                role = message.guild.get_role(result[0]['roleId'])
                await role.delete()
                db.remove(User.memberId == member.id)
                await message.channel.send("> :white_check_mark: > **Role removed**\n<@{0}>, I removed your custom role.\nDo `-role` to create a new custom role".format(member.id))
            else:
                await message.channel.send("> :x: > **You can't do that**\n<@{0}>, you don't have any custom role!".format(member.id))
        else:
            await message.channel.send("> :x: > **You can't do that**\nThis is for Level 30+ use only.")

client.run(TOKEN)