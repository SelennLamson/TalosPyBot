import discord
from .command_base import Command

class ReportCmd(Command):
	def __init__(self):
		super(ReportCmd).__init__()
		self.calls = ['report', 'staff', 'moderation']
		self.help = "Envoie un message à la modération."
		self.args = [['text', True, 'Texte du message']]
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message, command, args):
		full_text = ' '.join(args)
		if full_text == '':
			await utils.reply(message, "vous n'avez spécifié aucun texte après la commande.")
			return

		await utils.modChan.send("**<@&438380476944875522>, <@&438380418514026497> - " +
								 utils.user_to_member(message.author).display_name +
								 " a envoyé un message à la modération :**\n\n" +
								 full_text)
		await utils.reply(message, "j'ai bien envoyé ton message ! La modération va bientôt te répondre.")
