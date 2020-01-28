import discord
from .command_base import Command

class CountCmd(Command):
	def __init__(self):
		super(CountCmd).__init__()
		self.calls = ['count']
		self.help = "Donne le nombre de personnes connectées dans un salon vocal ou textuel."
		self.args = [['channel', True, 'Salon dont les membres doivent êtres comptés.']]
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_staff(member)

	async def __call__(self, client, utils, message, command, args):
		chan_name = ' '.join(args)
		if chan_name == '':
			await message.channel.send("Il me faut un nom de salon dans lequel compter les membres.")
			return
		else:
			channel = utils.find_channel_by_name(chan_name)

		if channel is None:
			await message.channel.send("Le nom du salon n'est pas reconnu.")
			return
		if not isinstance(channel, discord.VoiceChannel) and not isinstance(channel, discord.TextChannel):
			await message.channel.send("Ce n'est ni un salon vocal, ni un salon textuel !")
			return

		await message.channel.send("Il y a " + str(len(channel.members)) + " membres connectés dans le salon " + chan_name + " !")
