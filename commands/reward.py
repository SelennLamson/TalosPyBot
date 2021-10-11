import discord
from .command_base import Command
import json
from discord import VoiceChannel

USERS_FILE = "data/users.json"

def create_user(user_id):
	new_user = dict()
	new_user["id"] = user_id
	new_user["xp"] = 0
	new_user["talos"] = 0
	return new_user

class RewardCmd(Command):
	def __init__(self):
		super(RewardCmd).__init__()
		self.calls = ['reward', 'addxp', 'addtalos', 'chanxp', 'give']
		self.help = "Pour récompenser les membres ou obtenir ses propres statistiques."
		self.args = [["command", False, """"help" pour connaître les commandes, affiche ses propres rewards si pas de commande."""]]
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message, command, args):
		member: discord.Member = utils.user_to_member(message.author)

		if command == 'addtalos':
			args.insert(0, 'addtalos')
		elif command == 'addxp':
			args.insert(0, 'addxp')
		elif command == 'chanxp':
			args.insert(0, 'chanxp')
		elif command == 'give':
			args.insert(0, 'give')

		response = None
		data = json.load(open(USERS_FILE, "r"))
		users = data["users"]

		user_id = message.author.id
		current_user = None
		for user in users:
			if user["id"] == user_id:
				current_user = user
				break

		if len(args) == 0:
			# Display member's rewards
			if current_user is not None:
				response = "voici tes récompenses :\n\n"
				if "xp" in current_user:
					xp = current_user["xp"]

					level = 0
					level_multiple = 1
					increment = 2
					req_xp = 0
					while req_xp + (level_multiple * 50) <= xp:
						req_xp += level_multiple * 50
						level_multiple = int(level_multiple * increment)
						increment = max(1.1, increment - 0.1)
						level += 1

					response += ":military_medal: Niveau " + str(level) + "\n\n"
					response += ":diamond_shape_with_a_dot_inside: " + str(xp) + " XP (prochain niveau à " + str(req_xp + level_multiple * 50) + " XP)\n\n"
				if "talos" in current_user:
					talos = current_user["talos"]
					response += ":moneybag: " + str(talos) + " Talos sur ton compte philobank.\n\n"
			else:
				response = "tu n'as pour le moment aucune récompense. Participe à des challenges et à des événements pour en obtenir !"

		# elif args[0].startswith("<@"):
		#

		elif args[0] == "give":
			if len(args) == 3:
				try:
					amount = int(args[1])
					target_id = int(args[2][3:-1])

					if "talos" in current_user and current_user["talos"] >= amount:
						current_user["talos"] -= amount

						target_user = None
						for user in users:
							if user["id"] == target_id:
								target_user = user
								break

						if target_user is not None:
							if "talos" in target_user:
								target_user["talos"] += amount
							else:
								target_user["talos"] = amount
						else:
							new_user = create_user(target_id)
							new_user["talos"] = amount
							users.append(new_user)

						json.dump(data, open(USERS_FILE, "w"))

						for mem in utils.talosLab.members:
							if mem.id == target_id:
								await message.channel.send(mem.mention + ", tu as reçu :moneybag: " + str(
									amount) + " Talos de la part de " + member.mention + " ! Tape \"!reward\" pour consulter ton total !")
								break

					else:
						response = "tu n'as pas assez de Talos pour en donner autant !"


				except ValueError:
					response = "le format n'est pas le bon. \"!reward give 100 @membre\" pour verser 100 Talos au membre de votre choix."
			else:
				response = "le format n'est pas le bon. \"!reward give 100 @membre\" pour verser 100 Talos au membre de votre choix."

		elif args[0] == "help":
			response = """- !reward sans argument supplémentaire pour consulter vos récompenses.\n"""
			response += """- "give 100 @member" pour verser des Talos au membre de votre choix.\n"""

		elif utils.is_moderation(member):

			if args[0] == "addxp":
				if len(args) >= 3:
					try:
						amount = int(args[1])

						target_ids = list(map(int, [arg[3:-1] for arg in args[2:]]))

						target_users = []
						unfound_users = set(target_ids.copy())
						for user in users:
							if user["id"] in target_ids:
								target_users.append(user)
								unfound_users.discard(user["id"])

						for target_user in target_users:
							if "xp" in target_user:
								target_user["xp"] += amount
							else:
								target_user["xp"] = amount

						for unfound_id in unfound_users:
							new_user = create_user(unfound_id)
							new_user["xp"] = amount
							users.append(new_user)

						json.dump(data, open(USERS_FILE, "w"))

						for mem in utils.talosLab.members:
							if mem.id in target_ids:
								await message.channel.send(mem.mention + ", tu as gagné :diamond_shape_with_a_dot_inside: " + str(amount) + " XP ! Tape \"!reward\" pour consulter ton total !")

					except ValueError:
						response = "le format n'est pas le bon. \"!reward addxp 100 @membre1 ...\" pour ajouter 100 XP aux membres de votre choix."
				else:
					response = "le format n'est pas le bon. \"!reward addxp 100 @membre1 ...\" pour ajouter 100 XP aux membres de votre choix."

			elif args[0] == 'chanxp':
				if len(args) == 3:
					try:
						amount = int(args[1])
						chan_id = int(args[2])
						target_channel = None

						for chan in utils.talosLab.channels:
							if chan.id == chan_id:
								target_channel = chan
								break

						if target_channel is not None and isinstance(target_channel, VoiceChannel):
							target_users = []
							mem_ids = [m.id for m in target_channel.members]
							unfound_users = set(mem_ids.copy())
							for user in users:
								if user["id"] in mem_ids:
									target_users.append(user)
									unfound_users.discard(user["id"])

							for target_user in target_users:
								if "xp" in target_user:
									target_user["xp"] += amount
								else:
									target_user["xp"] = amount

							for unfound_id in unfound_users:
								new_user = create_user(unfound_id)
								new_user["xp"] = amount
								users.append(new_user)

							json.dump(data, open(USERS_FILE, "w"))

							for mem in target_channel.members:
								await mem.send("Tu as gagné :diamond_shape_with_a_dot_inside: " + str(amount) + " XP ! Consulte ton total en écrivant 'reward'.")

							response = "les membres du salon " + target_channel.name + " ont gagné :diamond_shape_with_a_dot_inside: " + str(amount) + " XP !"
						else:
							response = "je ne reconnais pas cet identifiant de salon, ou ce n'est pas un salon vocal."

					except ValueError:
						response = "le format n'est pas le bon. \"!reward chanxp 100 438436126563368971 ...\" pour ajouter 100 XP aux membres du channel 438436126563368971 (copier l'ID)."
				else:
					response = "le format n'est pas le bon. \"!reward chanxp 100 438436126563368971 ...\" pour ajouter 100 XP aux membres du channel 438436126563368971 (copier l'ID)."

			elif args[0] == "addtalos":
				if len(args) == 3:
					try:
						amount = int(args[1])

						target_ids = list(map(int, [arg[3:-1] for arg in args[2:]]))

						target_users = []
						unfound_users = set(target_ids.copy())
						for user in users:
							if user["id"] in target_ids:
								target_users.append(user)
								unfound_users.discard(user["id"])

						for target_user in target_users:
							if "talos" in target_user:
								target_user["talos"] += amount
							else:
								target_user["talos"] = amount

						for unfound_id in unfound_users:
							new_user = create_user(unfound_id)
							new_user["talos"] = amount
							users.append(new_user)

						json.dump(data, open(USERS_FILE, "w"))

						for mem in utils.talosLab.members:
							if mem.id in target_ids:
								await message.channel.send(mem.mention + ", tu as gagné :moneybag: " + str(amount) + " Talos ! Tape \"!reward\" pour consulter ton total !")

					except ValueError:
						response = "le format n'est pas le bon. \"!reward addtalos 100 @membre1 ...\" pour ajouter 100 Talos aux membres de votre choix."
				else:
					response = "le format n'est pas le bon. \"!reward addtalos 100 @membre1 ...\" pour ajouter 100 Talos aux membres de votre choix."

		if response is not None:
			await utils.reply(message, response)
