# imports modules
import discord
import asyncio
from discord.ext import commands 
from lightdb import LightDB as ldb 
client = commands.Bot(command_prefix='t!')
token = "Bot token here ...."
db = ldb('tdb.json')
@client.event 
async def on_ready():
    print("---------------------------------")
    print("    Running as    ",client.user)
    print("---------------------------------")
@client.event 
async def on_reaction_add(reaction,user):
    if user.bot:
        pass 
    else: 
        if reaction.emoji == "🎫":
            if reaction.message.content.startswith('[ TICKET PANEL ]'):
                if reaction.message.author == client.user:
                    everyone = discord.PermissionOverwrite(view_channel=False)
                    mine = discord.PermissionOverwrite(view_channel=True)
                    name = f'ticket-{user}-{user.id}'
                    t = db.get(f'{reaction.message.guild.id}-{user}-ticket')
                    if t is not None:
                        pass
                    else: 
                        ch = await reaction.message.guild.create_text_channel(name)
                        await ch.overwrites_for(user,mine)
                        await ch.overwrites_for(reaction.message.guild.default_role,everyone)
        if reaction.emoji == "🔒":
            if reaction.message.content.startswith('[ TICKET ]'):
                if reaction.message.author == client.user:
                    await reaction.message.channel.delete()
                    db.pop(f'{reaction.message.guild.id}-{user}-ticket')
@client.command()
async def ticket(ctx):
    role = db.get(f'{ctx.message.guild.id}-role')
    t = db.get(f'{ctx.guild.id}-{ctx.message.author}-ticket')
    msg = db.get(f'{ctx.message.guild.id}-tkmsg')
    
    if role is None:
        await ctx.send(':x: **You cant Create a ticket because this server dont have the system configured !**')
    else:
        channel_name = f"ticket-{ctx.message.author.name}-{ctx.message.author.id}"
        if t is not None:
            embed = discord.Embed(title=":x: **You have a ticket openeded!**")
            await ctx.send(embed=embed)
        else:
            db.set(f'{ctx.guild.id}-{ctx.message.author}-ticket','OPENED_TICKET')
            user = ctx.message.author
            everyone = discord.PermissionOverwrite(view_channel=False)
            mine = discord.PermissionOverwrite(view_channel=True)
            name = f'ticket-{user}-{user.id}'
            ch = await ctx.guild.create_text_channel(channel_name)
            
            if msg is None:
                msg = "Please wait until someone respond!"
                embed = discord.Embed(title="Welcome!",description=msg,color=0xeb9234)
                await ch.set_permissions(ctx.message.author,overwrite=mine)
                await ch.set_permissions(ctx.guild.default_role,overwrite=everyone)
                a = await ch.send(f"[ TICKET ] {ctx.message.author.mention},{role}",embed=embed)
                await a.add_reaction('🔒')
            else:
                embed = discord.Embed(title="Welcome!",description=msg,color=0xeb9234)
                a = await ch.send(f"[ TICKET ] {ctx.message.author.mention},{role}",embed=embed)

@client.command()
@commands.has_permissions(manage_roles = True)
async def set_ticketrole(ctx, role:discord.Role):
    db.set(f'{ctx.message.guild.id}-role',role.mention)
    await ctx.send(embed=discord.Embed(title="Done!",description="I have added the role to my db!",color=0xeb9234))
@client.command()
@commands.has_permissions(manage_channels = True)
async def set_ticketmsg(ctx, *,msg):
    db.set(f'{ctx.message.guild.id}-tkmsg',msg)
    await ctx.send('**Success** I have changed ticket  message!')
@client.command()
@commands.has_permissions(manage_channels = True)
async def send_ticketpanel(ctx, channel:discord.TextChannel):
    embed = discord.Embed(title=":ticket: Open a ticket!",description="React with :ticket: To open a ticket!",color=0x5865F2)
    msg = await channel.send("[ TICKET PANEL ]",embed=embed)
    await msg.add_reaction('🎫')
    await ctx.send(f'**Success** Sent ticket panel message on `{channel}`')
    db.set(f'{ctx.guild.id}-panel',{"msg_id":msg.id,"channel_id":channel.id})
@client.command()
@commands.has_permissions(manage_channels = True)
async def set_panelmsg(ctx, *,a):
    c = db.get(f'{ctx.guild.id}-panel')
    if c is None:
        await ctx.send(':x: **Error, this server dont have a ticket panel!**')
    else:
        cid = c['channel_id']
        mid = c['msg_id']
        ch = client.get_channel(cid)
        msg = await ch.fetch_message(mid)
        embed = discord.Embed(title=":ticket: Open a ticket!",description=a,color=0x5865F2)
        await msg.edit(content="[ TICKET PANEL ]",embed=embed)
        await ctx.send('**Success** Changed panel description!')
client.run(token)
