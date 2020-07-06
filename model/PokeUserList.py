from model.PokemonUser import PokeUser
import discord


class UserList:
    """
    A class providing a list for PokeUser with functionality
    """

    def __init__(self):
        self.__user_list = []

    def add_user(self, user: discord.User) -> None:
        """
        creates a pokeuser and ads it to the list

        :param user:
        :return:
        """
        self.__user_list.append(PokeUser(user))

    def get_user(self, user: discord.User) -> PokeUser:
        """
        returns matching pokeuser

        :param user:
        :return:
        """
        u: PokeUser
        for u in self.__user_list:
            if u.get_user() == user:
                return u
        raise AttributeError("User " + str(user) + "isn't in list")

    def is_empty(self) -> bool:
        """
        returns if the list is empty

        :return:
        """
        return len(self.__user_list) == 0

    def user_exists(self, user: discord.User) -> bool:
        """
        returns if the user exists in list

        :param user:
        :return:
        """
        for u in self.__user_list:
            if u.get_user() == user:
                return True
        return False
