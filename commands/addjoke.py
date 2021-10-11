from .command_base import Command

class AddJokeCmd(Command):
	def __init__(self):
		super(AddJokeCmd).__init__()
		self.calls = ['addjoke']
		self.help = "Ajoute une blague à la base de données du bot."
		self.args = [["joke", True, "Une blague, entre 50 et 300 caractères."]]
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_staff(member)

	async def __call__(self, client, utils, message, command, args):
		if len(args) == 0:
			await utils.reply(message, "vous devez spécifier une blague à envoyer, après le channel.")
			return

		text = ' '.join(args)
		if len(text) < 20 or len(text) > 500:
			await utils.reply(message, "la blague doit faire entre 50 et 300 caractères.")
			return

		with open("data/jokes.txt", "a", encoding='utf-8') as file:
			file.write('\n' + text.replace('\n', '\\n'))

		await utils.reply(message, "la blague a été ajoutée, merci !")

		await message.channel.send(text)
