import discord
from discord.ext import commands
import os
TOKEN = os.environ['TOKEN']

# Intents nécessaires pour accéder aux messages
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ID du salon où l'état du serveur sera affiché
CHANNEL_ID = 1290719396272017409  # Remplace par l'ID de ton salon

# Variable pour suivre l'état du serveur
server_status_message = None

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    # Récupérer le salon d'état du serveur
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        global server_status_message
        # Si le message existe déjà, ne pas le recréer
        async for message in channel.history(limit=100):
            if message.author == bot.user:
                server_status_message = message
                break
        # Si aucun message trouvé, en créer un nouveau
        if not server_status_message:
            server_status_message = await channel.send("# 🟢 Serveur On")

# Commande pour mettre le serveur sur "off"
@bot.command()
@commands.has_permissions(administrator=True)
async def off(ctx):
    global server_status_message
    if server_status_message:
        await server_status_message.edit(content="# 🔴 Serveur Off")
        await ctx.author.send("Le serveur est maintenant hors ligne.")
        await ctx.message.delete()  # Supprimer la commande après exécution
    else:
        await ctx.author.send("Aucun message d'état du serveur trouvé.")
        await ctx.message.delete()  # Supprimer la commande après exécution

# Commande pour mettre le serveur sur "on"
@bot.command()
@commands.has_permissions(administrator=True)
async def on(ctx):
    global server_status_message
    if server_status_message:
        await server_status_message.edit(content="🟢 Serveur On")
        await ctx.author.send("Le serveur est maintenant en ligne.")
        await ctx.message.delete()  # Supprimer la commande après exécution
    else:
        await ctx.author.send("Aucun message d'état du serveur trouvé.")
        await ctx.message.delete()  # Supprimer la commande après exécution

# Gérer les erreurs de permissions
@off.error
@on.error
async def on_off_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.author.send("Vous n'avez pas la permission d'utiliser cette commande.")
        await ctx.message.delete()  # Supprimer la commande après l'erreur

bot.run(TOKEN)
