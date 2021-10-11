from .command_base import Command
import random
import discord
from time import time
import os

class FunCmd(Command):
	def __init__(self):
		super(FunCmd).__init__()
		self.calls = []
		self.help = ''
		self.args = []
		self.pm_only = False
		self.serv_only = False

		self.joke_cooldown = 3600
		self.max_jokes = 3
		self.joke_power = self.joke_cooldown * self.max_jokes
		self.last_joke_time = 0
		self.last_joke_index = 0
		self.random_indices = []

	def has_role(self, utils, member):
		return False

	async def __call__(self, client, utils, message, command, args):
		if command is None and args is None:
			return
		elif command is None and args is not None:
			text = ' '.join(args)
		elif command is not None and args is None:
			text = command
		else:
			text = ' '.join([command] + args)
		rep = ''
		mes = ''

		if ('raconte' in text or 'dis' in text or 'fais' in text) and ('blague' in text or 'drôle' in text or 'histoire' in text):
			delta = time() - self.last_joke_time
			self.last_joke_time = time()

			self.joke_power = min(self.joke_power + delta, self.joke_cooldown * self.max_jokes)

			if self.joke_power >= self.joke_cooldown:
				self.joke_power -= self.joke_cooldown

				jokes = open("data/jokes.txt", 'r', encoding='utf-8').readlines()
				memes = os.listdir("data/memes")
				total_length = len(jokes) + len(memes)
				self.last_joke_index += 1

				if len(self.random_indices) != total_length or self.last_joke_index >= total_length:
					self.random_indices = list(range(total_length))
					random.shuffle(self.random_indices)

					self.last_joke_index = 0

				joke_index = self.random_indices[self.last_joke_index]
				if joke_index < len(jokes):
					mes = jokes[joke_index].strip().replace("\\n", "\n")
				else:
					img_path = "data/memes/" + memes[joke_index - len(jokes)]
					rep = mes = ""
					img = discord.File(img_path)
					await message.channel.send(file=img)

			else:
				mes = "Vous m'avez pris pour Cortana ? J'en aurai peut-être tout à l'heure..."

		elif 'uppercut' in text:
			rep = "arrête de me frapper, stp. Je prône la non-violence."
		elif 'bonjour' in text or 'hello' in text:
			rep = "salut."
		elif "je t'aime" in text:
			rep = "j'imagine que moi aussi, mais je suis assez occupé·e pour l'instant... :blue_heart:"

		if rep != '':
			await utils.reply(message, rep)
		elif mes != '':
			await message.channel.send(mes)
