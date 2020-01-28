import discord
from .command_base import Command

class SalonCmd(Command):
	def __init__(self):
		super(SalonCmd).__init__()
		self.calls = ['salon']
		self.help = "Change le nom du salon vocal de discussion, depuis le salon textuel lié."
		self.args = [['sujet', False, 'Nouveau nom du sujet. Si non renseigné, le réinitialise.']]
		self.pm_only = False
		self.serv_only = True

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message, command, args):
		if not utils.is_linked_channel(message.channel):
			await utils.reply(message, "je peux seulement changer le nom des salons de discussion.")
			return

		new_name = ' '.join(args)
		voice_chan_name = ''
		if message.channel.name[6] == '1':
			voice_chan_name = "📗 "
		elif message.channel.name[6] == '2':
			voice_chan_name = "📘 "
		else:
			voice_chan_name = "📙 "

		if new_name == '':
			new_name = '...'
			voice_chan_name += "Salon " + message.channel.name[6]
		else:
			voice_chan_name += new_name[:23]

		linked = utils.get_linked_channel(message.channel)
		if linked is not None:
			linked_chan: discord.VoiceChannel = client.get_channel(linked)
			await linked_chan.edit(name=voice_chan_name)
			await utils.reply(message, 'le sujet du salon est maintenant "' + new_name[:23] + '" !')
		else:
			utils.reply(message, "il y a eu une erreur, le salon n'a pas été renommé.")
