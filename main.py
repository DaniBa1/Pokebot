import random
from discord.ext import commands
from model.Pokedatabase import Pokedatabase
from model.PokeUserList import UserList

bot = commands.Bot(command_prefix='p!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author != bot.user:

        # if user tries to enter a command and is not registered, tell him
        if message.content != "p!start" and message.content.startswith("p!") and not user_list.user_exists(
                message.author):
            await message.channel.send("Bitte zuerst p!start eingeben!")

        # spawning pokemon
        random_number = random.random()
        if random_number < spawn_rate and not user_list.is_empty():
            await spawn_catch_pokemon(message)

        # adding users via a start command
        if message.content == "p!start" and not user_list.user_exists(message.author):
            user_list.add_user(message.author)
            await message.channel.send("Jetzt bist du auch dabei!")

    # check for commands
    if user_list.user_exists(message.author):
        await bot.process_commands(message)


@bot.command(name="pokemon")
async def show_pokemon(ctx):
    """
    Command to show a list of pokemon
    :param ctx:
    :return:
    """
    user = user_list.get_user(ctx.message.author)
    if not user.has_pokemon():
        await ctx.send("Du hast keine Pokémon!")
        return
    await ctx.send(embed=user.get_current_inventory_page())


@bot.command(name="info")
async def show_info(ctx):
    """
    Command to show a info of a single pokemon
    :param ctx:
    :return:
    """
    user = user_list.get_user(ctx.message.author)
    if not user.has_pokemon():
        await ctx.send("Du hast keine Pokémon!")
        return
    await ctx.send(embed=user.get_current_pokemon())


@bot.command(name="next")
async def show_next(ctx):
    user = user_list.get_user(ctx.message.author)
    if user.get_show_state() == 2:
        await ctx.send(embed=user.get_next_inventory_page())
    elif user.get_show_state() == 1:
        await ctx.send(embed=user.get_next_pokemon())
    elif user.get_show_state() == 0:
        await ctx.send("Bitte zuerst p!info oder p!pokemon eingeben.")


@bot.command(name="prev")
async def show_next(ctx):
    user = user_list.get_user(ctx.message.author)
    if user.get_show_state() == 2:
        await ctx.send(embed=user.get_prev_inventory_page())
    elif user.get_show_state() == 1:
        await ctx.send(embed=user.get_prev_pokemon())
    elif user.get_show_state() == 0:
        await ctx.send("Bitte zuerst p!info oder p!pokemon eingeben.")


@bot.command(name="catch")
async def catch(ctx, name):
    if not pokedatabase.catching_is_active():
        await ctx.send("Es ist gerade kein Pokémon aufgetaucht!")
        return
    poke_name = pokedatabase.get_catch_name()
    poke_level = pokedatabase.get_catch_level()
    if name.lower() == poke_name.lower():
        pokedatabase.assign_pokemon(user_list.get_user(ctx.message.author))
        await ctx.send(
            f"Glückwunsch {ctx.message.author.mention}! Du hast ein Level {poke_level} {poke_name} gefangen!!")
    else:
        await ctx.send("Das ist nicht der Name!")


async def spawn_catch_pokemon(message):
    if pokedatabase.catching_is_active():
        return
    await message.channel.send(embed=pokedatabase.generate_pokemon_to_catch())


# read key from "keys" file
with open("keys", "r") as file:
    key = file.readline()

# setup
spawn_rate = 0.1
pokedatabase = Pokedatabase()
pokedatabase.cache_pokemon_until(151)
user_list = UserList()

# start the bot
bot.run(key)
