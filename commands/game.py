import discord
from .command_base import Command
import random
import json
import requests
import asyncio

ALPHANUM = ['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

async def display_game_state(channel):
	try:
		img = discord.File('../gamestate.png')
		await channel.send(file=img)
	except FileNotFoundError:
		await channel.send("Je n'ai pas trouvé d'état de jeu à afficher.")

class GameCmd(Command):
	def __init__(self):
		super(GameCmd).__init__()
		self.calls = ['game']
		self.help = "Commandes liées aux défis de programmation."
		self.args = [["command", True, """"help" pour connaître les commandes, "register" pour s'inscrire."""]]
		self.pm_only = False
		self.serv_only = False

		self.gamechannel = None

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message, command, args):
		member: discord.Member = utils.user_to_member(message.author)

		if len(args) == 0:
			args = ["help"]

		response = None
		members_changed = False

		if args[0] == "register":
			data = json.load(open("data/gameusers.json", "r"))
			gameusers = data["gameusers"]

			userid = str(message.author.id)

			found = False
			for gameuser in gameusers:
				if gameuser["id"] == userid:
					found = True
					await message.author.send("Vous êtes déjà enregistré·e, voici votre code secret : " + gameuser["code"])
					break

			if not found:
				code = ''.join([random.choice(ALPHANUM) for _ in range(30)])

				name = member.display_name
				if len(args) > 1:
					name = args[1]

				gameuser = {"id": userid, "code": code, "name": name}
				gameusers.append(gameuser)

				json.dump(data, open("data/gameusers.json", "w"))

				avatar = message.author.avatar_url_as(format="png", size=64)
				await avatar.save(open("../players/" + userid + ".png", "wb"))

				await message.author.send("Vous êtes à présent enregistré·e pour le défi de programmation ! Voici votre code secret : " + code)
				members_changed = True

		elif args[0] == "unregister":
			data = json.load(open("data/gameusers.json", "r"))
			gameusers = data["gameusers"]

			userid = str(message.author.id)

			found = None
			for i, gameuser in enumerate(gameusers):
				if gameuser["id"] == userid:
					found = i
					break

			if found is None:
				response = "vous n'êtes pas enregistré."
			else:
				del gameusers[found]
				json.dump(data, open("data/gameusers.json", "w"))
				response = "je vous ai retiré de la liste des participants. Votre code n'est plus valide !"
				members_changed = True

		elif args[0] == "help":
			response = """- "register" pour s'enregistrer au jeu de programmation, avec un nom de joueur optionnel sans espaces.\n"""
			response += """- "unregister" pour vous retirer du jeu."""

		if utils.is_admin(member):
			if self.gamechannel is None:
				self.gamechannel = message.channel

			if args[0] == "members":
				members_changed = True
				response = "j'ai mis à jour la liste des membres."

			elif args[0] == "channel":
				self.gamechannel = message.channel
				response = "jusqu'au prochain redémarrage, j'afficherai le jeu ici."

			elif args[0] == "init":
				w, h, s = "10", "10", "1500"
				if len(args) >= 3:
					w, h = args[1], args[2]
					if len(args) >= 4:
						s = args[3]
				configdata = json.load(open("config.json", "r"))
				data = configdata["gametoken"] + "INIT|" + w + " " + h + " " + s
				requests.post(configdata["gameurl"], data=data)
				response = "j'ai lancé une nouvelle partie !"

			elif args[0] == "turn":
				configdata = json.load(open("config.json", "r"))
				data = configdata["gametoken"] + "TURN|None"
				requests.post(configdata["gameurl"], data=data)

			elif args[0] == "display":
				await display_game_state(self.gamechannel)

		if members_changed:
			configdata = json.load(open("config.json", "r"))
			data = configdata["gametoken"] + "MEMBERS|" + open("data/gameusers.json", "r").read()
			requests.post(configdata["gameurl"], data=data)

		if response is not None:
			await utils.reply(message, response)
