from discord import Guild, TextChannel, VoiceChannel, DMChannel, Member

from commands.help import HelpCmd
from commands.count import CountCmd
from commands.ping import PingCmd
from commands.purge import PurgeCmd
from commands.report import ReportCmd
from commands.candidature import CandidCmd
from commands.salon import SalonCmd
from commands.role import RoleCmd
from commands.stats import StatsCmd
from commands.say import SayCmd
from commands.addjoke import AddJokeCmd

# Important roles
botRole = 439113523616808961
adminRole = 438380418514026497
moderatorRole = 438380476944875522
animatorRole = 446775652792926208
videomakerRole = 438380570125271050
memberRole = 442678135847256080
everyoneRole = 438379867218771968

# Utilities
class Utils:
	def __init__(self, client):
		self.client = client
		self.talosLab: Guild = None
		self.testChan: TextChannel = None
		self.candidChan: TextChannel = None
		self.modChan: TextChannel = None
		self.linkedChannels = []
		self.autoRoles = []
		self.commands = [
			AddJokeCmd(),
			CandidCmd(),
			CountCmd(),
			HelpCmd(),
			PingCmd(),
			PurgeCmd(),
			ReportCmd(),
			RoleCmd(),
			SalonCmd(),
			SayCmd(),
			StatsCmd(),
			]

	def initialize(self):
		self.talosLab = next(g for g in self.client.guilds if g.id == 438379867218771968)
		self.testChan = self.talosLab.get_channel(439113892048928790)
		self.candidChan = self.talosLab.get_channel(438433444070948864)
		self.modChan = self.talosLab.get_channel(438433444070948864)

		# [[VoiceChan, TextChan], [..., ...], ...]
		self.linkedChannels =[[438440224368885790, 440164468207517699],
							  [438440317134307350, 440164488478720012],
							  [440112635367915520, 440164519143014410]]
	
		self.autoRoles =[[450314792595488782, "Ciné 2.39", "pour être notifié par les news du club ciné."],
						 [450315068660383764, "Débatoire", "pour être notifié par les news du débatoire."],
						 [450784702761009154, "FrogLover", "parce les grenouilles ouvrent les portes d'un monde étrange."],
						 [457272560053125123, "Jeux", "pour être notifié des différents jeux organisés."],
						 [479405523293175818, "Sciences", "pour être notifié des annonces concernant les sciences."],
						 [513044467876364307, "Paradigmes", "pour être notifié des annonces concernant le projet de définition des paradigmes scientifiques."],
						 [515584314180894731, "Métaphysique", "pour être notifié des débats et événements organisés autour de la métaphysique."]]

	def user_to_member(self, user) -> Member:
		return self.talosLab.get_member(user.id)

	def is_pm(self, message):
		return isinstance(message.channel, DMChannel)

	def has_role(self, member, rolesin):
		return any(r.id in rolesin for r in member.roles)

	def is_admin(self, member):
		return self.has_role(member, [adminRole])

	def is_moderation(self, member):
		return self.has_role(member, [adminRole, moderatorRole])

	def is_staff(self, member):
		return self.has_role(member, [adminRole, moderatorRole, animatorRole])

	def is_vip(self, member):
		return self.has_role(member, [adminRole, moderatorRole, animatorRole, videomakerRole])

	def is_member(self, member):
		return self.has_role(member, [adminRole, moderatorRole, animatorRole, videomakerRole, memberRole])

	def is_member_only(self, member):
		return self.has_role(member, [memberRole]) and not self.is_vip(member)

	def get_admins(self):
		return self.talosLab.roles.get(adminRole).members

	def get_moderators(self):
		return self.talosLab.roles.get(moderatorRole).members

	def get_animators(self):
		return self.talosLab.roles.get(animatorRole).members

	def get_videomakers(self):
		return self.talosLab.roles.get(videomakerRole).members

	def get_members(self):
		return self.talosLab.roles.get(memberRole).members

	def get_vips(self):
		return [m for m in self.talosLab.members if self.is_vip(m)]

	def get_members_only(self):
		return [m for m in self.talosLab.members if self.is_member_only(m)]

	def is_linked_channel(self, channel):
		return any(channel.id in l for l in self.linkedChannels)

	def get_linked_channel(self, channel: VoiceChannel):
		for l in self.linkedChannels:
			if l[0] == channel.id:
				return l[1]
			elif l[1] == channel.id:
				return l[0]
		return None

	async def reply(self, message, text):
		await message.channel.send('{0.author.mention}, '.format(message) + text)

	def find_channel_by_name(self, name):
		for c in self.talosLab.channels:
			if c.name == name:
				return c
		return None
