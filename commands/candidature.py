import discord
from .command_base import Command

class CandidCmd(Command):
	def __init__(self):
		super(CandidCmd).__init__()
		self.calls = ['candidature', 'candid']
		self.help = "Envoie votre candidature à l'administration."
		self.args = [['text', True, 'Texte de la candidature']]
		self.pm_only = True
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message, command, args):
		full_text = ' '.join(args)
		if full_text == '':
			await utils.reply(message, "vous n'avez spécifié aucun texte après la commande.")
			return

		await utils.candidChan.send("**<@&438380418514026497> - " +
									utils.user_to_member(message.author).display_name +
									" a envoyé une candidature :**\n\n" +
									full_text)
		await utils.reply(message, "j'ai bien envoyé ta candidature ! Le staff va en prendre connaissance.")
