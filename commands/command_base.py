
class Command:
	def __init__(self):
		self.calls = []
		self.help = ""
		self.args = []
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return False

	async def __call__(self, client, utils, message, command, args):
		pass
