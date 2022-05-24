import discord
import os
import random
import asyncio
import time
import re
import diseaseapi
from discord import Member, Intents, Embed
from discord.ext import tasks, commands
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from dinteractions_Paginator import Paginator
from datetime import datetime
import numpy as np
from sympy import *
from sympy.algebras.quaternion import Quaternion
import requests
from google_images_search import GoogleImagesSearch

now = datetime.now()
bot = Bot(command_prefix=["C.","c.","C .","c .","C. ","c. "], intents=Intents.all())
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)

ping=(bot.latency)
pingms = ping*1000

ts = int(time.time())
d4 = datetime.utcfromtimestamp(ts).strftime("%b-%d-%Y")
d5 = now.strftime("%d/%m/%Y at %H:%M GMT")

print(time.time())
print(int(time.time()))
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

gis = GoogleImagesSearch('AIzaSyCjhBQROsJemcsJidNyu2Drxli88yQL9lQ', '74830862dd2874e30')

guild_ids=[906560310217945150,844302791622131732,908835201562574858,895809572294496286,895083927591596042,886877360614412320]

client = diseaseapi.Client().covid19

@slash.slash(
  name="Ban",
  description="Ban a user",
  options=[
                create_option(
                  name="user",
                  description="Target of the punishment",
                  option_type=6,
                  required=True
                ),
                create_option(
                  name="reason",
                  description="Ban reason",
                  option_type=3,
                  required=False
                )
             ])
async def ban(ctx:SlashContext, user: discord.Member, reason: str="No reason given"):

    if ctx.author.guild_permissions.ban_members is False:
        embed=discord.Embed(title="Missing Permissions", description=f"{ctx.author.mention}. You are missing the permission `ʙᴀɴ ᴍᴇᴍʙᴇʀꜱ`", color=0xFF0000)
        embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif user.guild_permissions.ban_members:
        em=discord.Embed(title=":angry: You can't ban other staff members! ", description=f"`{ctx.author.name}`, Don't try to ban `{user.name}` again!", color=0xFF0000)
        em.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    else:
      if user.bot:
        em=discord.Embed(title="Banned User",description=f"**{user.name}** has been banned from the server for: ``{reason}``", color=0x855182)
        em.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await user.ban(reason=reason)
        await ctx.send(embed=em)
      else:
        embed=discord.Embed(title=f"{user.mention}", description=f"You have been banned from **{ctx.guild}** for: {reason}!", color=0x855182)
        em=discord.Embed(title="Banned User",description=f"**{user.name}** has been banned from the server for: ``{reason}``", color=0x855182)
        em.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await user.send(embed=embed)
        await user.ban(reason=reason)
        await ctx.send(embed=em)

#################################################################

@slash.slash(
  name="Kick",
  description="Kick a user",
  options=[
                create_option(
                  name="user",
                  description="Target of the punishment",
                  option_type=6,
                  required=True
                ),
                create_option(
                  name="reason",
                  description="Kick reason",
                  option_type=3,
                  required=False
                )
             ])
async def kick(ctx:SlashContext, user: discord.Member, reason: str="No reason given"):
    if ctx.author.guild_permissions.kick_members is False:
        embed=discord.Embed(title="Missing Permissions", description=f"{ctx.author.mention}. You are missing the permission `ᴋɪᴄᴋ ᴍᴇᴍʙᴇʀꜱ`", color=0xFF0000)
        embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif user.guild_permissions.kick_members:
        em=discord.Embed(title=":angry: You can't kick other staff members! ", description=f"`{ctx.author.name}`, Don't try to ban `{user.name}` again!", color=0xFF0000)
        em.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    else:
        embed=discord.Embed(title=f"{user.mention}", description=f"You have been kicked from **{ctx.guild}** for: {reason}!", color=0x855182)
        em=discord.Embed(title="Kicked User", description=f"**{user.name}** has been kicked from the server for: ``{reason}``", color=0x855182)
        em.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await user.send(embed=embed)
        await user.ban(reason=reason)
        await ctx.send(embed=em)

#################################################################

only_text_option = create_option(
    name="channel",
    description="Targeted announcement channel",
    option_type=7,
    required=True
)
only_text_option['channel_types'] = [0]

@slash.slash(
  name="Announce",
  description="Announce a message",
  options=[
    create_option(
      name="message",
      description="Announcement message (256 characters maximum)",
      option_type=3,
      required=True
    ),only_text_option,
    create_option(
      name="role",
      description="Announcement mention role",
      option_type=8,
      required=False
    )
  ])
async def Announce(ctx:SlashContext, channel: discord.channel, message: str, role: str=None):
    if ctx.author.guild_permissions.mention_everyone:
        embed=discord.Embed(title=f"Announcement on: {d4}",color=0x855182)
        embed.add_field(name=f"{message}" , value="⠀")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await channel.send(embed=embed)
        if role is not None:
            await channel.send(f"||{role}||")
        await ctx.send(f"Announcement sent in: {channel.mention}")

    else:
        embed=discord.Embed(title="Missing Permissions", description=f"{ctx.author.mention}. You are missing the permission `ᴍᴇɴᴛɪᴏɴ ᴇᴠᴇʀʏᴏɴᴇ/ʀᴏʟᴇ`", color=0xFF0000)
        embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

#################################################################

@slash.slash(
  name="Coinflip",
  description="Test your luck in a coinflip!",
  options=[
    create_option(
      name="choice",
      description="Heads or tails",
      option_type=3,
      required=True,
      choices=[
        create_choice(
          name="Heads",
          value="Heads"
        ),
        create_choice(
          name="Tails",
          value="Tails"
        )
      ]
    )
  ])
async def Coinflip(ctx:SlashContext, choice:str):

    coins = ["Heads", "Tails"]
    coin = random.choice(coins)

    if choice==coin:
        embed=Embed(title="<a:coinflip:930357623717498890> Coinflip", description="⠀", color=0xFFD700)
        embed.add_field(name=f"The bot chose: `{coin}`", value="⠀", inline=False)
        embed.add_field(name=f"Your choice: `{choice}`", value="⠀", inline=False)
        embed.set_footer(text="✔️ You guessed right!")
        await ctx.send(embed=embed)
    else:
        embed=Embed(title="<a:coinflip:930357623717498890> Coinflip", description="⠀", color=0xFF0000)
        embed.add_field(name=f"The bot chose: `{coin}`", value="⠀", inline=False)
        embed.add_field(name=f"Your choice: `{choice}`", value="⠀", inline=False)
        embed.set_footer(text="❌ You guessed wrong!")
        await ctx.send(embed=embed)

#################################################################

@slash.slash(
  name="Purge",
  description="Purge an amount of messages",
  options=[
    create_option(
      name="number",
      description="Number of messages to delete (Up to 100 messages can be deleted)",
      option_type=3,
      required=True
    )
  ])
async def Purge(ctx:SlashContext, number: str, amount=30):
    if ctx.author.guild_permissions.administrator:
        channel = ctx.channel
        amount = int(number)
        messages = []
        async for message in channel.history(limit=amount):
            messages.append(message)
        if amount == 1:
          embed=Embed(description=f'**{amount}** message deleted.', color=0x855182)
          embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
          await channel.delete_messages(messages)
          await ctx.send(embed=embed)

        else:
          embed=Embed(description=f'**{amount}** messages deleted.', color=0x855182)
          embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
          await channel.delete_messages(messages)
          await ctx.send(embed=embed)

    else:
        embed=discord.Embed(title="Missing Permissions", description=f"{ctx.author.mention}. You are missing the permission `ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ`", color=0xFF0000)
        embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

#################################################################

@slash.slash(name="Serverinfo", description="Displays the info of the current server")
async def Serverinfo(ctx:SlashContext):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=0x855182
      )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

#################################################################

@slash.slash(name="Userinfo",
description="Displays the info of a server member",
options=[
  create_option(
    name="user",
    description="User to find the info from",
    option_type=6,
    required=False
  )
])
async def Userinfo(ctx:SlashContext, user: discord.Member=None):
    date_format = "%a, %d %b %Y %I:%M %p"
    if user is None:
      user=ctx.author
      role=user.top_role
      emcolor=role.color
      embed = discord.Embed(description=user.mention, color=emcolor)
      embed.set_author(name=str(user), icon_url=user.avatar_url)
      embed.set_thumbnail(url=user.avatar_url)
      embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
      members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
      embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
      if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
      perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
      embed.add_field(name="Guild permissions", value=perm_string, inline=False)
      embed.add_field(name='User ID', value=user.id)
      embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
    else:
      role=user.top_role
      emcolor=role.color
      embed = discord.Embed(description=user.mention, color=emcolor)
      embed.set_author(name=str(user), icon_url=user.avatar_url)
      embed.set_thumbnail(url=user.avatar_url)
      embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
      members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
      embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
      if len(user.roles) > 1:
          role_string = ' '.join([r.mention for r in user.roles][1:])
          embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
      perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
      embed.add_field(name="Guild permissions", value=perm_string, inline=False)
      embed.add_field(name='User ID', value=user.id)
      embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)

#################################################################

@slash.slash(
  name='Membercount',
  description="Displays the member count of the current  (including bots)"
  )
async def Membercount(ctx:SlashContext):
  embed=Embed(title=f"{ctx.guild}'s Member Count", description=f"Member Count: {ctx.guild.member_count}", color=0x855182)
  embed.set_footer(text=f"Requested by {ctx.author} on the {d5}",icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

#################################################################

@slash.slash(
  name="Mute",
  description="Mutes the specified user"
  )
async def mute(ctx:SlashContext, member: discord.Member, *, reason=None):
  if ctx.author.guild_permissions.mute_members is False:
        embed=discord.Embed(title="Missing Permissions", description=f"{ctx.author.mention}. You are missing the permission `ᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀꜱ`", color=0xFF0000)
        embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
  else:
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    if reason is None:
      embed = discord.Embed(description=f"✅  **{member.mention} muted successfuly**", colour=0x855182)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    elif reason is not None:
      embed = discord.Embed(description=f"✅  **{member.mention} was muted successfuly for: {reason}**", colour=0x855182)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)

########################################################################

@slash.slash(
  name="Unmute",
  description="Unmutes the specified user"
  )
async def unmute(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
  if ctx.author.guild_permissions.mute_members is False:
        embed=discord.Embed(title="Missing Permissions", description=f"{ctx.author.mention}. You are missing the permission `ᴜɴᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀꜱ`", color=0xFF0000)
        embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

  else:

    await member.remove_roles(mutedRole)
    embed = discord.Embed(description=f"✅  **{member.mention} was unmuted successfuly**",colour=0x855182)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#########################################################################

@slash.slash(
  name="Tempmute",
  description="Temporarily mutes the specified user",
  options=[
    create_option(
      name="user",
      description="Target of the mute",
      option_type=6,
      required=True
    ),
    create_option(
      name="time",
      description="Length of the mute || Time codes: 's','m','h','d'",
      option_type=3,
      required=True
    )
  ]
)
async def tempmute(ctx:SlashContext, user: discord.Member, time: str, *, reason=None):
    muted_role=discord.utils.get(ctx.guild.roles, name="Muted")
    if ctx.author.guild_permissions.mute_members is False:
        embed=discord.Embed(title="Missing Permissions", description=f"{ctx.author.mention}. You are missing the permission `ᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀꜱ`", color=0xFF0000)
        embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    else:
      embed = discord.Embed(description= f"✅  **{user.mention} was muted successfuly**", color=0x855182)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      await user.add_roles(muted_role)
      if "s" in time:
          length_list=time.split("s")
          length=' '.join([str(item) for item in length_list])
          await asyncio.sleep(int(length))

      if "m" in time:
          length_list=time.split("m")
          length=' '.join([str(item) for item in length_list])
          true_length=int(length)
          await asyncio.sleep(true_length*60)

      if "h" in time:
          length_list=time.split("h")
          length=' '.join([str(item) for item in length_list])
          true_length=int(length)
          await asyncio.sleep(true_length*60*60)

      if "d" in time:
          length_list=time.split("d")
          length=' '.join([str(item) for item in length_list])
          true_length=int(length)
          await asyncio.sleep(true_length*60*60*24)
      
      await user.remove_roles(muted_role)
      
      em = discord.Embed(description= f"✅  **{user.mention} was unmuted successfuly**", color=0x855182)
      em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=em)

#########################################################################

@slash.slash(
  name="Unban",
  description="Unban the specified user",
  options=[
    create_option(
      name="user",
      description="Username of the person to be unbanned",
      option_type=3,
      required=True
    )
  ]
)
async def unban(ctx, *,user: str):
  if ctx.author.guild_permissions.ban_members is False:
        embed=discord.Embed(title="Missing Permissions", description=f"{ctx.author.mention}. You are missing the permission `ᴜɴʙᴀɴ ᴍᴇᴍʙᴇʀꜱ`", color=0xFF0000)
        embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
  else:
    banned_user = await ctx.guild.bans()

    for ban_entry in banned_user:
        users = ban_entry.user

        if (users.name) == (user):
          em=discord.Embed(description=f"{users.mention} has been successfully unbanned from the server", color=0x855182)
          em.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
          await ctx.guild.unban(users)
          await ctx.send(embed=em)

#########################################################################

@slash.slash(
  name="Avatar",
  description="Display the avatar of a user",
  options=[
  create_option(
    name="user",
    description="User to pull the avatar from",
    option_type=6,
    required=False
  )
]
)
async def avatar(ctx:SlashContext,user: discord.Member=None):
  if user is None:
    user=ctx.author
    embed=Embed(description=f"This is the avatar of **{user.name}**",color=0x855182)
    embed.set_image(url=user.avatar_url)
  else:
    embed=Embed(description=f"This is the avatar of **{user.name}**",color=0x855182)
    embed.set_image(url=user.avatar_url)
  await ctx.send(embed=embed)

#################################################################

@slash.slash(
  name="Roulette",
  description="Try your luck in a fun game of roulette by choosing red or black!",
  options=[
    create_option(
      name="choice",
      description="Red or Black",
      option_type=3,
      required=True,
      choices=[
        create_choice(
          name="Red",
          value="Red"
        ),
        create_choice(
          name="Black",
          value="Black"
        )
      ]
    )
  ]
  )
async def Roulette(ctx:SlashContext, choice:str):

    colors = ["Red", "Black"]
    color = random.choice(colors)
    
    if choice==color:
        embed=Embed(title="🎰 Roulette", description="⠀", color=0xFFD700)
        embed.add_field(name=f"The bot chose: `{color}`", value="⠀", inline=False)
        embed.add_field(name=f"Your choice: `{choice}`", value="⠀", inline=False)
        embed.set_footer(text="✔️ You guessed right!")
        await ctx.send(embed=embed)
    else:
        embed=Embed(title="🎰 Roulette", description="⠀", color=0xFF0000)
        embed.add_field(name=f"The bot chose: `{color}`", value="⠀", inline=False)
        embed.add_field(name=f"Your choice: `{choice}`", value="⠀", inline=False)
        embed.set_footer(text="❌ You guessed wrong!")
        await ctx.send(embed=embed)

#################################################################

@slash.slash(
  name="Ping",
  description="Find out the ping of the discord bot"
)
async def ping(ctx:SlashContext):
  botping=round(bot.latency*1000)
  if botping=="nan":
    embed=Embed(title="Comet Ping",
    description="The current response time of the bot", color=0x000000)
    embed.add_field(name="Bot Ping:", value="The bot is dead")
    await ctx.send(embed=embed)
  else:
    embed=Embed(title="Comet Ping",
    description="The current response time of the bot", color=0x000000)
    embed.add_field(name="Bot Ping:", value=f"{botping} ms")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#################################################################

@slash.slash(
  name="Calculate",
  description="Calculate any equation",
  options=[
    create_option(
      name="equation",
      description="The equation to find the answer from",
      option_type=3,
      required=True
    )
  ]
)
async def calc(ctx:SlashContext, equation:str=None):
  str_expr = equation
  expr = sympify(str_expr)
  answer = round(expr.evalf())
  embed=Embed(title=":abacus: Calculator",
  description="Find out the answer of any equation",color=0x000000)
  embed.add_field(name="Equation answer:", value=f"{answer}")
  embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

#################################################################

only_text_option = create_option(
    name="channel",
    description="The channel to host the giveaway in",
    option_type=7,
    required=True
)
only_text_option['channel_types'] = [0]

@slash.slash(
  name="Giveaway",
  description="Host a giveaway 🎉",
  options=[
    create_option(
      name="prize",
      description="The prize of the giveaway",
      option_type=3,
      required=True
    ),
    create_option(
      name="givtime",
      description="Time of the giveaway || Time codes: 's','m','h','d'",
      option_type=3,
      required=True
    ),only_text_option
  ]
)
async def giveaway(ctx:SlashContext, givtime: str, prize:str, channel:discord.channel, *, reason=None):
      embed = discord.Embed(description= f"✅  Giveaway for: **{prize}** created in {channel}")
      await ctx.send(embed=embed)
#//////////////////////////////////////////////////////////
      if "s" in givtime:
        length_list=givtime.split("s")
        length=' '.join([str(item) for item in length_list])
        timestamp=int(time.time())+int(length)
        one = discord.Embed(title=f"🎉  {prize}  🎉", color=0x855182)
        one.add_field(name="‎‎‎‎‎‎ㅤ", value=f"Hosted by: {ctx.author.mention}\nEnding in: <t:{timestamp}:R> ")
        one.add_field(name="📃 To Do",value="- Remain in the server", inline=False)
        one.set_footer(text="React with 🎉 to enter the giveaway")
        msg = await channel.send(embed=one)
        await msg.add_reaction('🎉')
        await asyncio.sleep(int(length))

      if "m" in givtime:
        length_list=givtime.split("m")
        length=' '.join([str(item) for item in length_list])
        true_length=int(length)
        timestamp=int(time.time())+(true_length*60)
        one = discord.Embed(title=f"🎉  {prize}  🎉", color=0x855182)
        one.add_field(name="‎‎‎‎‎‎ㅤ", value=f"Hosted by: {ctx.author.mention}\nEnding in: <t:{timestamp}:R>")
        one.add_field(name="📃 To Do",value="- Remain in the server", inline=False)
        one.set_footer(text="React with 🎉 to enter the giveaway")
        msg = await channel.send(embed=one)
        await msg.add_reaction('🎉')
        await asyncio.sleep(true_length*60)

      if "h" in givtime:
        length_list=givtime.split("h")
        length=' '.join([str(item) for item in length_list])
        true_length=int(length)
        timestamp=int(time.time())+(true_length*60*60)
        one = discord.Embed(title=f"🎉  {prize}  🎉", color=0x855182)
        one.add_field(name="‎‎‎‎‎‎ㅤ", value=f"Hosted by: {ctx.author.mention}\nEnding in: <t:{timestamp}:R>")
        one.add_field(name="📃 To Do",value="- Remain in the server", inline=False)
        one.set_footer(text="React with 🎉 to enter the giveaway")
        msg = await channel.send(embed=one)
        await msg.add_reaction('🎉')
        await asyncio.sleep(true_length*60*60)

      if "d" in givtime:
        length_list=givtime.split("d")
        length=' '.join([str(item) for item in length_list])
        true_length=int(length)
        timestamp=int(time.time())+(true_length*60*60*24)
        one = discord.Embed(title=f"🎉  {prize}  🎉", color=0x855182)
        one.add_field(name="‎‎‎‎‎‎ㅤ", value=f"Hosted by: {ctx.author.mention}\nEnding in: <t:{timestamp}:R>")
        one.add_field(name="📃 To Do",value="- Remain in the server", inline=False)
        one.set_footer(text="React with 🎉 to enter the giveaway")
        msg = await channel.send(embed=one)
        await msg.add_reaction('🎉')
        await asyncio.sleep(true_length*60*60*24)

      new_msg = await channel.fetch_message(msg.id)
      users = await new_msg.reactions[0].users().flatten()
      users.pop(users.index(bot.user))

      winner = random.choice(users)
      await channel.send(f":tada: Congratulations {winner.mention}! You won: **{prize}**!")

      embed2 = discord.Embed(title=f"🎉  {prize}  🎉",
                             description=f":trophy: **Winner:** {winner.mention}")
      embed2.set_footer(text="Giveaway Has Ended")
      await msg.edit(embed=embed2)

#################################################################

@slash.slash(
  name="Random",
  description="Randomly chooses a number in between 2 given numbers",
  options=[
    create_option(
      name="lowest",
      description="The lowest number to choose from",
      option_type=4,
      required=True
    ),
    create_option(
      name="highest",
      description="The highest number to choose from",
      option_type=4,
      required=True
    )
  ]
)
async def randnum(ctx:SlashContext, lowest:int, highest:int):
  answer=random.randrange(lowest, highest)
  embed=Embed(title=":game_die: Random Number Generator",
  description="Let Comet choose a random number from a given range",color=0x000000)
  embed.add_field(name="__Numbers:__", value=f"**Lowest Number:** ``{lowest}``\n **Highest Number:** ``{highest}``\n **Random Number:** ``{answer}``")
  embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

################################################################

only_text_option = create_option(
    name="channel",
    description="The channel of the giveaway",
    option_type=7,
    required=True
)
only_text_option['channel_types'] = [0]

@slash.slash(
  name="Reroll",
  description="Reroll the winner of a past giveaway.",
  options=[
    create_option(
      name="messageid",
      description="The ID of the giveaway message",
      option_type=3,
      required=True
    ),only_text_option
  ]
)
async def reroll(ctx, channel: discord.TextChannel, messageid: str):
  new_msg = await channel.fetch_message(messageid)
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(bot.user))
  winner = random.choice(users)
  almost_title=new_msg.embeds[0].title
  title_list=almost_title.split("🎉")
  title=' '.join([str(item) for item in title_list])
  await ctx.send(f"The giveaway for:**{title}**has been rerolled.")
  await ctx.channel.send(f":tada: The new winner is: {winner.mention}!")

################################################################

@slash.slash(
  name="Bigrat",
  description="Shows an image of a very big rat."
)
async def rat(ctx):
  embed=discord.Embed(title="Big Rat", color=0x808080)
  embed.set_image(url="https://cometbot.cc/bigrat.png")
  embed.set_footer(text="Image courtesy of https://bigrat.monster/", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)
  
################################################################

@slash.slash(
  name="rat",
  description="Find cute rat pictures."
)
async def ratsearch(ctx):
  amnt=random.randrange(1, 999)
  print(amnt)
  _search_params = {
    'q': 'rat',
    'num': 1,
  }
  gis.search(search_params=_search_params)
  for image in gis.results():
    embed=Embed(title="Rat Image Search", color=0x808080)
    embed.set_image(url=image.url)
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

################################################################

@slash.slash(
  name="Cap",
  description="The cap meter."
)
async def cap(ctx):
  cap=random.randrange(0,100)
  range_1=range(0,10,1)
  range_2=range(11,20,1)
  range_3=range(21,30,1)
  range_4=range(31,40,1)
  range_5=range(41,50,1)
  range_6=range(51,60,1)
  range_7=range(61,70,1)
  range_8=range(71,80,1)
  range_9=range(81,90,1)
  range_10=range(91,100,1)
  embed=Embed(title="🧢 Cap Meter", color=0x855182)
  if cap in range_1:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_2:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_3:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_4:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_5:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_6:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_7:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_8:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_9:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if cap in range_10:
    embed.add_field(name=f"Cap Percentage: {cap}%",value="🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩")
    embed.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

################################################################

@slash.slash(
  name="Help",
  description="Display the help menu"
)
async def help(ctx: SlashContext):
    one = discord.Embed(title="Command Categories", description="`Please use /help <category> to explore the bots categories`", color=0x855182)
    one.add_field(name="Bot Related Links", value="• Official Support Server: https://discord.gg/KZWghWSYE5")
    one.add_field(name="⠀",value="• Invite Comet to your server: https://dsc.gg/cometmod", inline=False)
    one.set_image(url="https://cdn.discordapp.com/attachments/844302791622131735/915391264235614229/fixed_twitter_banner.png")
    one.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)

    #//////////////////////////////////////////////////////////////

    two = discord.Embed(title="📰 Informative Commands", description="These commands all display useful information about discord and the real world", color=0x855182)
    two.add_field(name="📡 `/serverinfo`", value="Displays the servers information")
    two.add_field(name=":person_pouting: `/userinfo`", value="Displays a users information")
    two.add_field(name=":person_pouting: `/membercount`", value="Displays the member count of a server (this includes bots)")
    two.add_field(name="<:covid:915325442402160691> `/covid`",value="Shows COVID-19 statistics from around the world")
    two.add_field(name="<:covidhist:915389337586270249> `/covidhistory`",value="Historical COVID-19 statistics from arround the world")
    two.add_field(name="<:covidtop:915388183406063666> `/covidtop`",value="Shows COVID-19 statistics for the top 15 countries around the world")
    two.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)

    #//////////////////////////////////////////////////////////////

    three = discord.Embed(title="🛠️ Moderation Commands", description="These commands can only be used by server staff", color=0x855182)
    three.add_field(name="🔨 `/ban`", value="Bans a targeted user from the server")
    three.add_field(name="💐 `/unban`", value="Unbans a targeted user from the server")
    three.add_field(name="🚪 `/kick`", value="Kicks a targeted user from the server")
    three.add_field(name="🔇 `/mute`", value="Mutes a targeted user from the server")
    three.add_field(name="🔊 `/unmute`", value="Unmutes a targeted user from the server")
    three.add_field(name="🔇 `/tempmute`", value="Temporarily mutes a targeted user from the server")
    three.add_field(name="🗑️ `/purge`", value="Deletes a chosen amount of messages from the server")
    three.add_field(name="📢 `/announce`",value="Announces a message in a chosen channel and mentions a chosen role")
    three.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)

    #//////////////////////////////////////////////////////////////

    four = discord.Embed(title="🎈 Fun Commands", description="These commands are just to mess around and can be used by everyone", color=0x855182)
    four.add_field(name=":coin: `/coinflip`", value="Choose heads or tails to win in this randomized game of coinflip!")
    four.add_field(name="🎰 `/roulette`", value="Try your luck in a fun game of roulette by choosing red or black!")
    four.set_footer(text=f"Requested by {ctx.author} on the {d5}", icon_url=ctx.author.avatar_url)

    #//////////////////////////////////////////////////////////////
    pages = [one, two, three, four]

    await Paginator(bot=bot, ctx=ctx, pages=pages, useButtons=False, timeout=60, deleteAfterTimeout=True).run()

#################################################################

@slash.slash(
  name="queuing",
  description="test command",
  options=[
    create_option(
      name="message",
      description="thing to add",
      option_type=3,
      required=True
    )
  ]
)
async def queuing(ctx: SlashContext):
  with open(f'{ctx.guild.id}.txt', 'a') as f:
    f.write(message)
  with open(f'{ctx.guild.id}.txt') as f:
    line = f.read()
  await ctx.send(line)

@bot.command()
async def test(ctx):
  text_file = open(f"./{ctx.guild.id}.txt", "x")
  f = open(f"./{ctx.guild.id}.txt", "r")
  if ctx.author in f:
    await ctx.send("You are already in the database!")
  else:
    txt_file = open(f"./{ctx.guild.id}.txt", "a")
    txt_file.write(f'{ctx.author}\n')
    txt_file.close()
    await ctx.send("You have been added to the database!")

@bot.command()
async def testing(ctx):
  with open(f'{ctx.guild.id}.txt', 'a') as f:
    if ctx.author in f"{ctx.guild.id}.txt":
      ctx.send("You are in the database")
    else:
      f.write(ctx.author)
      await ctx.send(f"You have been added to the database")

@bot.command(pass_context=True)
async def servcount(ctx):
  amnt=0
  for guild in bot.guilds:
    amnt+=1
    pass
  await ctx.send(f"Server count: {amnt} servers")

guild_name=(guild.name for guild in bot.guilds)
guild_memcount=(guild.member_count for guild in bot.guilds)
amount=0

@bot.command()
async def servers(ctx):
  for guild in bot.guilds:
    amount+=1
    pass
  await ctx.send(f"{guild_name[amount]} : {guild_memcount[amount]}")

@bot.event
async def on_ready():
  print("AAAAAAAAAAAAAAA")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(bot.users)} users"))

@bot.event
async def on_guild_join(guild):
  channel = guild.system_channel
  embed=Embed(title="🎉 Thank you for choosing Comet as your moderation bot of choice! 🎉", color=0x2ecc71)
  embed.add_field(name="The Comet moderation bot uses slash commands as its prefix.", value="To get started, run the /help command to show more commands.", inline=True)
  embed.set_footer(text="If you encounter any issues or bugs with the bot, message our support over on Twitter: @OffCometBot")
  await channel.send(embed=embed)

bot.load_extension("cogs")
bot.run("OTA4NzYxMDYyMDkyOTcyMDQz.YY6bsQ.XU3pyCx1QK8RpPtONPManOqkX_4")