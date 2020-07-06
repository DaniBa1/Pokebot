import requests
from bs4 import BeautifulSoup
import discord


class AbstractPokemon:
    """
    A class for an Pokemon that has not been initialised, e.g. has no level or individual values
    """

    def __init__(self, name: str, types: list, number: int):
        self.__name = name
        self.__types = types
        self.__number = number

        # converting the number to a string
        number_string = "{:03d}".format(self.__number)

        # get the link of the png
        base_link = "https://www.pokewiki.de"
        path_png_findable = f"/Datei:Sugimori_{number_string}.png"
        response = requests.get(base_link + path_png_findable)
        soup = BeautifulSoup(response.text, "html.parser")
        self.__path_png = base_link + soup.find("div", {"class": "fullImageLink"}).find("a")["href"]

    def __str__(self):
        nr_string = "{:03d}".format(self.__number)
        if len(self.__types) == 1:
            return f"{self.__name}, Type 1: {self.__types[0]}, Nr: #{nr_string}"

        return f"{self.__name}, Type 1: {self.__types[0]}, Type 2: {self.__types[1]}, Nr: #{nr_string}"

    def get_number(self) -> int:
        return self.__number

    def get_name(self) -> str:
        return self.__name

    def get_types(self) -> list:
        return self.__types

    def get_png_path(self) -> str:
        return self.__path_png


class Pokemon(AbstractPokemon):
    """
    A class for an actual pokémon
    """

    def __init__(self, pokemon: AbstractPokemon, level: int):
        super().__init__(pokemon.get_name(), pokemon.get_types(), pokemon.get_number())
        self.__level = level

    def get_level(self) -> int:
        return self.__level

    def get_catch_embed(self) -> discord.Embed:
        """
        Returns an embed asking the user to guess the name of the pokémon

        :return:
        """
        with open("./templates/catch_template.txt", "r", encoding="utf-8") as file:
            dict_string = file.read()
        dict_string = dict_string.replace("{link}", self.get_png_path())

        return discord.Embed.from_dict(eval(dict_string))

    def get_info_embed(self, current_id: int, last_id: int) -> discord.Embed:
        """
        returns an embed showing information of the pokemon

        :param current_id:
        :param last_id:
        :return:
        """
        with open("./templates/info_template.txt", "r", encoding="utf-8") as file:
            template_txt = file.read()
        dict_string = template_txt.replace("{current_id}", str(current_id))
        dict_string = dict_string.replace("{last_id}", str(last_id))
        dict_string = dict_string.replace("{link}", self.get_png_path())
        dict_string = dict_string.replace("{Level}", str(self.get_level()))
        dict_string = dict_string.replace("{Name}", self.get_name())
        if len(self.get_types()) == 1:
            dict_string = dict_string.replace("{Typen}", self.get_types()[0])
        elif len(self.get_types()) == 2:
            dict_string = dict_string.replace("{Typen}", self.get_types()[0] + " | " + self.get_types()[1])
        else:
            raise AttributeError("Types has to be of length 1 or 2 but is " + str(len(self.get_types())))

        return discord.Embed.from_dict(eval(dict_string))
