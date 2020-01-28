import discord
from .command_base import Command

class PurgeCmd(Command):
	def __init__(self):
		super(PurgeCmd).__init__()
		self.calls = ['purge']
		self.help = "Supprime des messages dans le channel où la commande est utilisée."
		self.args = [['quantity', True, 'Nombre de messages à supprimer (entre 2 et 100).']]
		self.pm_only = False
		self.serv_only = True

	def has_role(self, utils, member):
		return utils.is_staff(member)

	async def __call__(self, client, utils, message, command, args):
		try:
			delete_count = int(args[0])
			assert 2 <= delete_count <= 100
		except (ValueError, IndexError, AssertionError):
			await utils.reply(message, "combien de messages voulez-vous que je supprime ? (entre 2 et 100)")
			return

		await message.channel.purge(limit=delete_count + 1)