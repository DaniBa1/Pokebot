from bs4 import BeautifulSoup
import requests
from model.Pokemon import AbstractPokemon, Pokemon
import random
import discord
from model.PokemonUser import PokeUser


class Pokedatabase:
    """
    Class for managing pokemon and providing an interface for information
    """

    def __init__(self):
        self.__pokemon_list = []
        self.__current_pokemon_to_catch: Pokemon = None

    def cache_pokemon_until(self, last_id: int) -> None:
        """
        Load Pokemon data from https://www.pokewiki.de/ until last_id
        Last_id per Gen:\n
        Gen I    151\n
        Gen II   251\n
        Gen III  386\n
        Gen IV   493\n
        Gen V    649\n
        Gen VI   721\n
        Gen VII  809\n
        Gen VIII 893

        :param last_id:
        :return:
        """

        # inital values
        current_pokemon = "Bisasam"
        number = 0

        # base link for scraping
        base_link = "https://www.pokewiki.de/"

        # loop over index
        for _ in range(last_id):
            types = []

            # get main page of current pokemon
            response = requests.get(f"{base_link}{current_pokemon}")
            soup = BeautifulSoup(response.text, "html.parser")

            # find next name
            next_name = soup.find("td", {"style": "text-align:right"}).find("a")["title"]

            # get the types of base pokemon, ignoring special forms
            all_type_soup = soup.find("table", {"class": "right round innerround"}).find_all("tr")[3].find_all("td")[1]
            original_type_soup = BeautifulSoup(str(all_type_soup).split("<sup></sup>")[0], "html.parser")
            for tag in original_type_soup.find_all("a"):
                if tag["title"] != "Typen":
                    types.append(tag["title"])

            # increase national dex number
            number = number + 1

            # add pokemon to database
            self.__pokemon_list.append(AbstractPokemon(current_pokemon, types, number))

            # update current pokemon name
            current_pokemon = next_name

    def assign_pokemon(self, user: PokeUser) -> None:
        """
        If user guessed the pokémon name, this function assigns the pokemon to the user

        :param user:
        :return:
        """

        # check if pokemon has to be catched
        if self.__current_pokemon_to_catch is None:
            raise AttributeError("No Pokémon to catch generated")

        # assign pokemon and resets current pokemon
        user.add_pokemon(self.__current_pokemon_to_catch)
        self.__current_pokemon_to_catch = None

    def generate_pokemon_to_catch(self) -> discord.Embed:
        """
        Generates random pokémon to catch and returns the embed for the discord message

        :return:
        """

        abstract_pokemon = random.choice(self.__pokemon_list)
        self.__current_pokemon_to_catch = Pokemon(abstract_pokemon, random.randint(1, 100))
        return self.__current_pokemon_to_catch.get_catch_embed()

    def catching_is_active(self) -> bool:
        """
        Returns whether theres currently a pokémon to catch

        :return:
        """
        if self.__current_pokemon_to_catch is None:
            return False
        return True

    def get_catch_name(self) -> str:
        """
        returns the name of the pokémon to catch

        :return:
        """
        if self.catching_is_active():
            return self.__current_pokemon_to_catch.get_name()
        raise AttributeError("No pokemon to catch")

    def get_catch_level(self) -> int:
        """
        returns the level of the pokémon to catch

        :return:
        """
        return self.__current_pokemon_to_catch.get_level()
