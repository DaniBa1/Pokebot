from model import Pokemon
import discord
import math


class PokeUser:
    """
    A class providing functionality for Users of the PokeBot
    """

    def __init__(self, user):
        self.__poke_list = []
        self.__current_id = 1
        self.__user = user
        # 1 is for pokemon info 2 is for pages 0 is not initialized
        self.__show_state = 0
        self.__current_page = 1

    def has_pokemon(self) -> bool:
        """
        returns if the user posesses any pokemon

        :return:
        """
        return not len(self.__poke_list) == 0

    def add_pokemon(self, pokemon: Pokemon.Pokemon) -> None:
        """
        adds a pokemon to the inventory of the user

        :param pokemon:
        :return:
        """
        if pokemon is not None:
            self.__poke_list.append(pokemon)
        else:
            raise TypeError("Tried to add None")

    def get_show_state(self) -> int:
        """
        returns show state\n
        0 - nothing shown\n
        1 - pokemon info\n
        2 - pokemon list

        :return:
        """
        return self.__show_state

    def get_user(self) -> discord.User:
        """
        returns the discord user

        :return:
        """
        return self.__user

    def __get_num_of_pages(self) -> int:
        if not self.has_pokemon():
            return 0
        return math.floor((len(self.__poke_list) - 1) / 20.0) + 1

    def get_pokemon_at_index(self, index: int) -> discord.Embed:
        """
        Returns the info embed of the pokemon, index starting with 1

        :param index:
        :return :
        """

        if len(self.__poke_list) == 0:
            raise AttributeError("User has no pokemon")
        if 1 <= index <= len(self.__poke_list):
            self.__current_id = index
            self.__show_state = 1
            return self.__poke_list[index - 1].get_info_embed(index, len(self.__poke_list))

        raise IndexError("index out of range, index is " + str(index) + " but size is" + str(len(self.__poke_list)))

    def get_current_pokemon(self) -> discord.Embed:
        """
        Returns the info embed of the current pokemon

        :return:
        """
        return self.get_pokemon_at_index(self.__current_id)

    def get_next_pokemon(self) -> discord.Embed:
        """
        Returns the info embed of the next pokemon\n
        if the current pokemon is the last, this function will return the first pokemon of the list

        :return:
        """
        return self.get_pokemon_at_index((self.__current_id % len(self.__poke_list)) + 1)

    def get_prev_pokemon(self) -> discord.Embed:
        """
        Returns the info embed of the previous pokemon\n
        if the current pokemon is the first, this function will return the last pokemon of the list

        :return:
        """
        return self.get_pokemon_at_index(((self.__current_id - 2) % len(self.__poke_list)) + 1)

    def get_inventory_at_page(self, page: int) -> discord.Embed:
        """
        Returns a embedded list with owned pokemon, showing max 20 pokemon per page

        :param page:
        :return:
        """
        self.__show_state = 2
        if (page - 1) * 20 > len(self.__poke_list):
            raise AttributeError("User only has " +
                                 str(self.__get_num_of_pages()) + "pages of pokemon, tried to acces page " + str(page))

        self.__current_page = page
        with open("./templates/page_template.txt", "r", encoding="utf-8") as file:
            dict_string = file.read()
        dict_string = dict_string.replace("{current_page}", str(self.__current_page))
        dict_string = dict_string.replace("{last_page}", str(self.__get_num_of_pages()))
        info_list = ""

        for i in range(20 * (self.__current_page - 1), min(len(self.__poke_list), 20 * self.__current_page)):
            poke = self.__poke_list[i]
            info_list += f"**{poke.get_name()}** | Level {poke.get_level()} | Position {i + 1}\\n"
        dict_string = dict_string.replace("{info_list}", info_list)
        return discord.Embed.from_dict(eval(dict_string))

    def get_current_inventory_page(self) -> discord.Embed:
        """
        Returns the list embed of the current page\n

        :return:
        """
        return self.get_inventory_at_page(self.__current_page)

    def get_next_inventory_page(self) -> discord.Embed:
        """
        Returns the list embed of the next page\n
        if the current pasg is the last one, this function will return the first page

        :return:
        """
        return self.get_inventory_at_page((self.__current_page % self.__get_num_of_pages()) + 1)

    def get_prev_inventory_page(self) -> discord.Embed:
        """
        Returns the list embed of the previous page\n
        if the current page is the first one, this function will return the last page

        :return:
        """
        return self.get_inventory_at_page(((self.__current_page - 2) % self.__get_num_of_pages()) + 1)
