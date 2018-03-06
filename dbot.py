#dbot
#Mathieu Dombrock

import discord
import requests
from pathlib import Path
import glob
client = discord.Client()

bot_command = "?"

@client.event
async def on_message(message):
	global bot_command
	msgin_original = message.content #some functions need case sensitive input
	msgin = message.content.lower()
	msgin = msgin.split(" ")
	msgin_original = msgin_original.split(" ")
	print(msgin)
	tag = '{0.author.mention} : \n'.format(message)
	if message.author == client.user:#make sure we are not talking to ourselves 
		return
	if (bot_command+'tutorial') in msgin[0] or (bot_command+'tut') in msgin[0]:
		if ('list') in msgin[1]:
			tut_dir = 'tutorials/'
			ftype = ".txt"
			tut_list = (glob.glob(tut_dir+"*.txt"))
			msgout = "**TUTORIALS AVAILABLE:**"
			for title in tut_list:
				title = title.replace(tut_dir,"")
				title = title.replace(ftype,"")
				msgout += "\n**"+title+"**"
		else:
			tutorial_location = 'tutorials/'+msgin[1]+'.txt'
			print(tutorial_location)
			#tutorail_file = Path(tutorial_location)
			if Path(tutorial_location).is_file():
				file = open(tutorial_location, "r")
				msgout = file.read()
				#msgout += "\n \n[If you have suggestions for a new tutorial or concerns about this one, please let us know in #suggestions-and-meta]"
			else:
				msgout = tag+"I can't find any saved tutorials on "+msgin[1]+"... sorry :/"
		await client.send_message(message.channel, msgout)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



client.run('Your key')