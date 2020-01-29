import discord
import json
import re

from utils import *
from commands.fun import FunCmd

config = json.loads(open("config.json", "r").read())
cmd_prefix = config['prefix']

client = discord.Client()
utils = Utils(client)
funcmd = FunCmd()


@client.event
async def on_ready():
    print('{} has started, with {} users, in {} channels of {} guilds.'.format(client.user.name, len(client.users), len(list(client.get_all_channels())), len(client.guilds)))
    utils.initialize()
    await client.change_presence(activity=discord.Game(name="ASSO en binaire"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    mention = "<@!{}>".format(client.user.id)
    content = message.content
    slicelen = 0

    if utils.is_pm(message):
        if re.match(r"j[ '’′´]?(ai|es?t)( bien)? (pri[st]? con+ais+[ae]n(c|s+)es? de|lu[ets]?) ([lt]a|votre) chartr?es?,?( et)? je ((m[ '’′´]?engages? [aà]|vais) [eéèêë]tre|serai[st]?) sympas?", content.lower()):
            member = utils.user_to_member(message.author)
            if utils.is_member(member):
                await message.channel.send("Vous êtes déjà membre, merci d'avoir lu la charte ! :smile:")
                return

            await message.channel.send("Je vous ajoute...")
            await member.add_roles(utils.talosLab.get_role(memberRole))
            await utils.testChan.send(member.display_name + " vient d'accepter la charte.")
            await message.channel.send("Et voilà !\n\nMerci d'avoir lu la charte ! Vous pouvez maintenant écrire dans les channels et vous connecter aux salons vocaux :smile:\n" +
                                       "Allez tout d'abord vous présenter dans le channel dédié !\n\n" +
                                       "**Important :** votre présentation pourra servir à d'autres membres pour chercher des personnes compétents dans un domaine qui les intéresse.\n" +
                                       "Par exemple, si vous êtes professeur ou étudiant en philo, mentionnez-le ! :slight_smile:")
            return

    if str.startswith(content, mention):
        slicelen = len(mention)
    elif str.startswith(content, cmd_prefix):
        slicelen = len(cmd_prefix)
    elif not utils.is_pm(message):
        return

    command = None
    args = content[slicelen:].strip().split(' ')
    args = [a for a in args if a != '']
    if len(args) > 0:
        command = args.pop(0).lower()

    called_cmd = None
    member = utils.user_to_member(message.author)
    for cmd in utils.commands:
        if command in cmd.calls:
            if cmd.has_role(utils, member):
                if (utils.is_pm(message) and not cmd.serv_only) or (not utils.is_pm(message) and not cmd.pm_only):
                    called_cmd = cmd
                elif utils.is_pm(message):
                    await message.author.send("Cette commande doit s'utiliser sur le serveur uniquement.")
                else:
                    await message.author.send("Cette commande s'utilise en MP uniquement.")
            else:
                await utils.reply(message, "vous n'avez pas la permission d'utiliser cette commande.")
            break

    if called_cmd is not None:
        await called_cmd(client, utils, message, command, args)
        return

    await funcmd(client, utils, message, command, args)


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    old_chan = before.channel
    new_chan = after.channel

    if old_chan == new_chan:
        return

    if old_chan is not None:
        if utils.is_admin(member):
            return
        linked = utils.get_linked_channel(old_chan)
        if linked is not None:
            linked_chan: discord.TextChannel = client.get_channel(linked)
            await linked_chan.set_permissions(member, overwrite=None)


    if new_chan is not None:
        if utils.is_admin(member):
            return
        linked = utils.get_linked_channel(new_chan)
        if linked is not None:
            linked_chan: discord.TextChannel = client.get_channel(linked)

            over = discord.PermissionOverwrite()
            over.update(read_messages=True)
            await linked_chan.set_permissions(member, overwrite=over)


client.run(config['token'])