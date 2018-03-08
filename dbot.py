#dbot
#Mathieu Dombrock

import discord
import re
import random
import string
import requests
import json
import pickle
import glob
from pathlib import Path

client = discord.Client()

@client.event
async def on_message(message):
	global ban_list
	bot_command = "?"
	memories = []
	memories_file = 'memories.pk'
	help_list = []
	tut_dir = 'tutorials/'
	ftype = ".txt"
	
	msgin_original = message.content #some functions need case sensitive input
	msgin = message.content.lower()
	msgin = msgin.split(" ")
	msgin_original = msgin_original.split(" ")
	print(msgin)
	tag = '{0.author.mention} : \n'.format(message)

	print("chan: "+str(message.channel))
	if message.author == client.user:#make sure we are not talking to ourselves 
		return

	for word in ban_list:
		if str(word).lower() in str(msgin_original).lower():
			msgout = tag+"**WOAH THERE!**\n\n**RULES:**\n```4.) NO HATE SPEECH OF ANY KIND (SEE RULE #1 & #3)```\n"
			msgout += "This incident has been logged.\nIf you feel like this happened in error, please contact a helper and let us know what happened."
			log_path = "deletion-log.txt"
			with open(log_path, 'r') as file:
				old = file.read()
			with open(log_path, 'w') as file:
				file.write(str(message.author)+": "+str(msgin_original)+"\n"+"OFFENDING WORD: "+str(word)+"\n-------\n"+old)
			await client.delete_message(message)
			await client.send_message(message.channel, msgout)
			return

	if str(message.channel)=="welcome":
		tutorial_location = 'tutorials/welcome-message.txt'
		file = open(tutorial_location, "r")
		msgout = file.read()
		await client.send_message(message.channel, msgout)
		return

	if random.randrange(50)<2:
		msgout = tag+"Thanks for being here!"
		await client.send_message(message.channel, msgout)


	help_list.append(["tutorial <topic>","Display a preset tutorial message."])
	help_list.append(["tutorial list","List available tutorial topics."])
	if (bot_command+'tutorial') in msgin[0] or (bot_command+'tut') in msgin[0]:
		if ('list') in msgin[1]:
			print("printing tut list")
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

	help_list.append(["test","See if I am working. Or more specifically, still responding to messages."])
	if ((bot_command+'test') in msgin[0]):
		msgout = "Yeah, yeah I, oh, I'm still alive."
		await client.send_message(message.channel, msgout)

	help_list.append(["roll <x>d<y>","Example: roll 1d3"])
	if ((bot_command+'roll') in msgin[0]):
		msgin = msgin[1].split("d")
		result = ""
		results = ""
		for x in range(int(msgin[0])):
			result = random.randrange( 0, int(msgin[1]) ) +1
			results += str(result)+"\n"
		msgout = tag+results
		await client.send_message(message.channel, msgout)

	help_list.append(["choose <choice1> <choice2> <choice3> <...>","Helps you make a choice. \nExample: choose Debian Ubuntu CentOS\nOutput: Ubuntu"])
	if ((bot_command+'choose') in msgin[0]):
		print("choose")
		msgin = msgin[1:]
		print(msgin)
		msgout = tag+"Choosing from: "+', '.join(msgin)+"\n"+random.choice(msgin)
		await client.send_message(message.channel, msgout)

	help_list.append(["google <search-term>","I'm feeling lucky"])
	if ((bot_command+'google') in msgin[0]):
		r = requests.get("http://www.google.com/search?q="+' '.join(msgin[1:])+"&btnI");
		msgout = r.url
		msgout = tag+str(msgout)
		await client.send_message(message.channel, msgout)

	help_list.append(["wiki <search-term>","searches wikipedia"])
	if ((bot_command+'wiki') in msgin[0]):
		r = requests.get("https://en.wikipedia.org/w/api.php?action=opensearch&search="+' '.join(msgin[1:])+"&limit=1&namespace=0&format=json");
		msgout = json.loads(r.text)
		msgout = tag+str(msgout[3]).strip("[\"']")
		await client.send_message(message.channel, msgout)

	help_list.append(["remember <topic/key> <memory/value>","Remember the following\nExample: remember Dre hip-hop mastermind"])
	if ((bot_command+'remember') in msgin[0]):
		subject = msgin[1]
		memory = ' '.join(msgin_original[2:])
		msgout = tag+'Remembered '+subject+" as "+memory
		memories.append([subject, memory])
		#open a pickle file
		with open(memories_file, 'wb') as fi:
		# dump your data into the file
			pickle.dump(memories, fi)
		await client.send_message(message.channel, msgout)

	help_list.append(["recall <topic/key>","recall a memory\nExample: recall Dre"])
	if ((bot_command+'recall') in msgin[0]):
		with open(memories_file, 'rb') as fi:
			memories = pickle.load(fi)
		found = False
		for x in memories:
			if x[0] == msgin[1]:
				found = True
				subject = x[0]
				memory = x[1]
				msgout = tag+"I Recall "+subject+" as "+memory
		if found == False:
			msgout = tag+"I don't recall that."
		await client.send_message(message.channel, msgout)


	#help must be last to ensure the help list is loaded
	help_list.append(["help","Displays Help Message."])
	if ((bot_command+'help') in msgin[0]):
		msgout = "```CSS\nDiscover-Bot```"
		for x in sorted(help_list):
			msgout += "```\n"
			msgout += bot_command+'\n'.join(x).replace("\n", "\n--")+"\n\n"
			msgout += "\n```"
		msgout += "\nhttps://github.com/matdombrock/Discover-Bot\n"
		await client.send_message(message.channel, msgout)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


print("Loading Ban List")
ban_list = []
with open('banned_words.txt') as f:
	ban_list = f.read().splitlines()
client.run('NDIwMzk4MzEwNTQxNDkyMjI1.DX_Z7A.5IO-BQcbK-HlsfmBZ4WdUkTp1wg')