import discord
from discord.ext import commands
from discord import app_commands
import requests

client = commands.AutoShardedBot(command_prefix=">", intents=discord.Intents.default())

@client.tree.command(name="roulette", description="A r6 strat roulette command!")
@app_commands.describe(gamemode="The gamemode you are playing.", team="The team you are on.")
@app_commands.choices(
    gamemode = [
        app_commands.Choice(name="Bomb", value=1),
        app_commands.Choice(name="Hostage", value=2),
        app_commands.Choice(name="Secure Area", value=3)
    ],
    team = [
        app_commands.Choice(name="Attack", value=1),
        app_commands.Choice(name="Defend", value=2)
    ]
)
async def _roulette_command(interaction: discord.Interaction, gamemode: app_commands.Choice[int], team: app_commands.Choice[int]):
    url = f"https://squadstrats.com/api/?type={str(gamemode.name)}&team={str(team.name)}"
    res = requests.get(url)
    content = res.content
    lst = content.split(b":", 1)

    embed = discord.Embed(title=str(lst[0].decode()), description=str(lst[1].decode()))
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"{client.user} connected to Discord")

client.run("token", reconnect=True)
