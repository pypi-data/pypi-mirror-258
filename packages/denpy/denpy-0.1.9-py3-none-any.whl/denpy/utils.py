import discord
from rich.table import Table
from rich.console import Console
from json import load
import inspect
import psutil

def create_table(params, values):
    table = Table()
    for param, value in zip(params, values):
        table.add_column(param)
    table.add_row(*values)
    console = Console()
    console.print(table)

def get_ram_usage():
    return f'{round(psutil.virtual_memory().used / 10000000)} MB'

async def send_custom_message(id, channel: discord.TextChannel, view=None, variables=None, edit: discord.Message or discord.Interaction = False):
    if variables is None:
        variables = {}
    path = inspect.stack()[1].filename.replace('\\', '/').split('/')
    path.pop(-1)
    with open(f'{"/".join(path)}/embeds/{id}.json', 'r', encoding='utf-8') as file:
        config = load(file)

    # Replace variables
    embeds = []
    for embed2 in config['embeds']:
        try:
            embed2['title']
        except KeyError:
            embed2['title'] = None
        try:
            embed2['image']['url']
        except KeyError:
            embed = discord.Embed(
                title=embed2['title'],
                description=embed2['description'],
                color=embed2['color']
            )
        else:
            embed = discord.Embed(
                title=embed2['title'],
                description=embed2['description'],
                color=embed2['color']
            ).set_image(url=embed2['image']['url'])
        try:
            embed2['thumbnail']['url']
        except KeyError:
            pass
        else:
            embed.set_thumbnail(url=embed2['thumbnail']['url'])
        try:
            embed2['fields']
        except KeyError:
            pass
        else:
            for field in embed2['fields']:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        embeds.append(embed)
    for variable in variables:
        if config['content'] is not None:
            config['content'] = config['content'].replace(f'{variable}', variables[variable])
        for embed in embeds:
            embed.title = embed.title.replace(f'{variable}', variables[variable])
            embed.description = embed.description.replace(f'{variable}', variables[variable])
            for field in embed.fields:
                field.name = field.name.replace(f'{variable}', variables[variable])
                field.value = field.value.replace(f'{variable}', variables[variable])

    # Send message
    if edit is False:
        message = await channel.send(content=config['content'], embeds=embeds, view=view)
    else:
        if discord.message.Message == type(edit):
            message = await edit.edit(content=config['content'], embeds=embeds, view=view)
        else:
            message = await edit.response.edit_message(content=config['content'], embeds=embeds, view=view)
    return message
