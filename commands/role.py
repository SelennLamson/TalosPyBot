import discord
from .command_base import Command

class RoleCmd(Command):
	def __init__(self):
		super(RoleCmd).__init__()
		self.calls = ['role', 'roles']
		self.help = "Donne la liste des rôles auto-attribuables. Attribue/désattribue un rôle si spécifié."
		self.args = [["role", False, "Rôle à attribuer/désattribuer. Si non renseigné, donne la liste des rôles."]]
		self.pm_only = False
		self.serv_only = False

	def has_role(self, utils, member):
		return utils.is_member(member)

	async def __call__(self, client, utils, message, command, args):
		member: discord.Member = utils.user_to_member(message.author)

		role_name = ' '.join(args).lower()
		if role_name == '':
			text = "**Liste des rôles disponibles :**\n```"
			for role_id, role, desc in utils.autoRoles:
				text += '- ' + role
				if utils.has_role(member, [role_id]):
					text += ' [Attribué]'
				text += ' : ' + desc + '\n'
			text += "```\nPour vous attribuer/désattribuer un rôle, utilisez la commande *!role <nom du rôle>*."
			await message.channel.send(text)
			return

		for role_id, role, desc in utils.autoRoles:
			if role.lower() == role_name:
				if utils.has_role(member, [role_id]):
					await member.remove_roles(utils.talosLab.get_role(role_id))
					await utils.reply(message, "je t'ai retiré le rôle : " + role)
					return
				else:
					await member.add_roles(utils.talosLab.get_role(role_id))
					await utils.reply(message, "je t'ai attribué le rôle : " + role)
					return
		await utils.reply(message, "le rôle spécifié n'a pas été reconnu comme rôle auto-attribuable.")
