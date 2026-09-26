import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")

@bot.command(name="ban", help="Bane um membro do servidor.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("❌ Você não pode banir a si mesmo!")
        return
    
    await member.ban(reason=reason)
    await ctx.send(f"🔨 O usuário **{member.name}** foi banido do servidor. Motivo: {reason or 'Não informado'}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para banir membros!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Você esqueceu de mencionar quem deseja banir. Use: `!ban @usuario [motivo]`", delete_after=5)

bot.run("MTU1MzQ5MzAzMTk4MDYzMDA1Ng.GbZ23W.VE0J2ouZjT4Rx9mM3HUNm3Q6qLN6k-SwFBdL-U")
