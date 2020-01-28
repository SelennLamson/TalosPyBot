from .command_base import Command

class PingCmd(Command):
	def __init__(self):
		super(PingCmd).__init__()
		self.calls = ['ping', 'p']
		self.help = 'Permet de tester le bot (renvoie "Pong !").'
		self.args = []
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message, command, args):
		await message.channel.send("Pong !")
