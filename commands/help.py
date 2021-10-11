from discord import Message, Member, User
from .command_base import Command

class HelpCmd(Command):
	def __init__(self):
		super(HelpCmd).__init__()
		self.calls = ['help', 'h']
		self.help = "Donne de l'aide sur les commandes de TalosBot."
		self.args = [['command', False, 'Donne une aide détaillée de la commande si spécifiée.']]
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message: Message, command, args):
		user = message.author
		if not utils.is_pm(message):
			await user.send("Salut, je préfère voir ça en MP, pour éviter de spammer le serveur.")

		member = utils.user_to_member(user)
		details = args[0] if len(args) > 0 else None
		helptext = ""

		commands = utils.commands

		if details:
			for c in commands:
				if details in c.calls and c.has_role(utils, member):
					helptext = "```!" + c.calls[0]
					for a in c.args:
						helptext += " " + ('<' if a[1] else '[') + a[0] + ('>' if a[1] else ']')
					helptext += "\n\n" + c.help

					if len(c.args) > 0:
						helptext += '\n\nArguments :'
						for a in c.args:
							helptext += "\n     " + ('<' if a[1] else '[') + a[0] + ('>' if a[1] else ']') + "       " + a[2]

					if len(c.calls) > 1:
						helptext += "\n\nRaccourcis :"
						for ca in c.calls[1:]:
							helptext += "   " + ca

					helptext += "```"
					break
			if helptext == "":
				helptext = "La commande !" + details + " n'existe pas ou ne vous est pas accessible, désolé !"
		else:
			helptext = "```Commandes accessibles :\n"
			for c in commands:
				if c.has_role(utils, member):
					helptext += "\n    !" + c.calls[0]
					for a in c.args:
						helptext += " " + ('<' if a[1] else '[') + a[0] + ('>' if a[1] else ']')
					helptext += " - " + c.help
			helptext += "\n\nTapez !help cmd pour avoir des détails sur une commande en particulier.```"

		await user.send(helptext)


