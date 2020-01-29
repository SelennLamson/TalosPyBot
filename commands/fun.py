from .command_base import Command
import random

class FunCmd(Command):
	def __init__(self):
		super(FunCmd).__init__()
		self.calls = []
		self.help = ''
		self.args = []
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return False

	async def __call__(self, client, utils, message, command, args):
		text = ' '.join([command] + args)
		rep = ''
		mes = ''

		if ('raconte' in text or 'dis' in text or 'fais' in text) and ('blague' in text or 'drôle' in text or 'histoire' in text):
			with open("data/jokes.txt", 'r', encoding='utf-8') as file:
				lines = [l for l in file]
				mes = random.choice(lines).strip().replace('\\n', '\n')
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
