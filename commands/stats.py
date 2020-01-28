from .command_base import Command

class StatsCmd(Command):
	def __init__(self):
		super(StatsCmd).__init__()
		self.calls = ['stats']
		self.help = 'Donne des statistiques sur les utilisateurs du Laboratoire de Talos.'
		self.args = []
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message, command, args):
		vips = utils.get_vips()
		members = utils.get_members_only()
		await message.channel.send("Il y a actuellement " + str(len(utils.talosLab.members)) +
								   " utilisateurs dans le Lab, dont " + str(len(members) + len(vips)) +
								   " sont membres ! Et puis il y a moi :slight_smile:")
