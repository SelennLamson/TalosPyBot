from .command_base import Command

class SayCmd(Command):
	def __init__(self):
		super(SayCmd).__init__()
		self.calls = ['say', 's']
		self.help = "Fait parler le bot dans le channel indiqué."
		self.args = [["channel", True, "Salon textuel dans lequel le bot va parler."],
					 ["text", True, "Ce que le bot va dire."]]
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_admin(member)

	async def __call__(self, client, utils, message, command, args):
		if len(args) == 0:
			await utils.reply(message, "vous devez spécifier un channel où envoyer le texte.")
			return
		if len(args) == 1:
			await utils.reply(message, "vous devez spécifier un texte à envoyer, après le channel.")
			return

		channel = utils.find_channel_by_name(args[0].lower())
		if channel is not None:
			await channel.send(' '.join(args[1:]))
		else:
			await utils.reply(message, "le nom du channel n'a pas été reconnu comme un channel textuel.")
