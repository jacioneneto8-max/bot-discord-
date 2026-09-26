import discord
from discord.ext import commands

# Configuração das Intents necessárias
intents = discord.Intents.default()
intents.message_content = True  # Obrigatório para ler comandos por texto
intents.members = True          # Obrigatório para gerenciar membros (ban/kick)

# O prefixo será '!' (Exemplo: !ban, !limpar)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online e logado como {bot.user}!")

# ==========================================
# 1. COMANDO DE LIMPEZA DE MENSAGENS (!limpar)
# ==========================================
@bot.command(name="limpar", help="Apaga uma quantidade específica de mensagens do canal.")
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int):
    if quantidade < 1:
        await ctx.send("Você precisa apagar pelo menos 1 mensagem.", delete_after=4)
        return
    
    apagadas = await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f"🧹 {len(apagadas) - 1} mensagens foram limpas com sucesso!", delete_after=5)

@limpar.error
async def limpar_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para gerenciar mensagens!", delete_after=5)


# ==========================================
# 2. COMANDO DE EXPULSÃO (!kick)
# ==========================================
@bot.command(name="kick", help="Expulsa um membro do servidor.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("❌ Você não pode expulsar a si mesmo!")
        return

    await member.kick(reason=reason)
    await ctx.send(f"👢 O usuário **{member.name}** foi expulso do servidor. Motivo: {reason or 'Não informado'}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para expulsar membros!", delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Você esqueceu de mencionar quem deseja expulsar. Use: `!kick @usuario [motivo]`", delete_after=5)


# ==========================================
# 3. COMANDO DE BANIMENTO (!ban)
# ==========================================
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
        await ctx.send("❌ Você não tem permissão para banir membros!", delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Você esqueceu de mencionar quem deseja banir. Use: `!ban @usuario [motivo]`", delete_after=5)


# Insira o Token do seu bot no lugar de "SEU_TOKEN_AQUI" (mantendo as aspas)
bot.run("SEU_TOKEN_AQUI")
