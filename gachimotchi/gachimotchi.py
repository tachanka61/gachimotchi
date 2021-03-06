#!/usr/bin/env python3

# TODO: Add saves
from random import choice
from os import name as osname, system

# Try to import colorama
try:
    from colorama import Fore, init
except ImportError:
    print("colorama module is not installed, trying to install")
    try:
        system("pip install colorama")  # Install colorama
        from colorama import Fore, init
    except OSError:
        print("Failed to install colorama")
        exit(1)

init(autoreset=True)

pet_art = """
    |\\__/,|   (`\\
  _.|o o  |_   ) )
-(((---(((--------
"""

# One of these names will be used if no name was provided
default_names = [
    "Benjamin",
    "Daniel",
    "Megumi",
    "Miyoko",
    "Ricardo",  # :)
    "Yoshiko",
]


class Gachimotchi:
    def __init__(self, names: list, ascii_art: str):
        self.names = names
        self.ascii_art = ascii_art
        self.stat_food = 100
        self.stat_mood = 100
        self.stat_fatigue = 0
        self.stat_age = 0
        self.alive = True
        self.move = ""
        self.banner = ""
        self.name = ""

    def select_name(self) -> str:
        """Select a name for the pet.

        Returns name of the pet 'str'
        """

        self.name = (
            input(
                f"{Fore.CYAN}Choose name of your pet (skip to choose random)\n>{Fore.GREEN} "
            )
            .strip()
            .capitalize()
        )

        # Choose random name if no name was selected
        if not self.name:
            self.name = choice(self.names)

        return self.name

    def show_banner(self) -> str:
        """Show banner.

        Returns banner 'str'
        """

        # Clean screen
        if osname == "nt":  # Windows
            system("cls")
        else:  # macOS, Linux, BSD and others
            system("clear")

        self.banner = f"""{Fore.MAGENTA}
        _________________________________
       /   Meow!                         \\
      |     My name is {self.name + ' '* (19 - len(self.name))}|
    O  \\_________________________________/
   o {Fore.CYAN}
{self.ascii_art}{Fore.GREEN}
====== = ======
Alive   -> {self.alive}
{Fore.RED if self.stat_food <= 25 else Fore.GREEN}Food    -> {self.stat_food}{Fore.GREEN}
{Fore.RED if self.stat_fatigue >= 75 else Fore.GREEN}Fatigue -> {self.stat_fatigue}{Fore.GREEN}
{Fore.RED if self.stat_mood <= 25 else Fore.GREEN}Mood    -> {self.stat_mood}{Fore.GREEN}
Age     -> {self.stat_age}
"""

        print(self.banner)

        return self.banner

    def select_move(self) -> str:
        """Get move of the player."""

        self.move = (
            input(
                f"{Fore.CYAN}What do you want to do? (Eat, play, do nothing, sleep, quit)\n>{Fore.GREEN} "
            )
            .strip()
            .lower()
        )

        match self.move:
            case ("e" | "eat"):
                self.move_eat(15)
                self.show_banner()
            case ("p" | "play"):
                self.move_play(food_value=10, mood_value=25, fatigue_value=15)
                self.show_banner()
            case ("s" | "sleep"):
                self.move_sleep(age_value=2, food_value=20)
                self.show_banner()
            case ("n" | "nothing" | "skip" | "do nothing"):
                self.move_do_nothing(
                    age_value=1, food_value=7, mood_value=10, fatigue_value=3
                )
                self.show_banner()
            case ("q" | "quit" | "exit"):
                self.bye()
            case _:
                self.select_move()

        return self.move

    def move_eat(self, value) -> int:
        """Feed pet.

        Increase food.
        """

        self.stat_food += value

        # Food can't be more than 100
        if self.stat_food > 100:
            self.stat_food = 100

        return self.stat_food

    def move_play(
        self, food_value: int, mood_value: int, fatigue_value: int
    ) -> dict[str, int]:
        """Play with the pet.

        Decrease food, increase mood and fatigue.

        Returns 'dict'
        """

        self.stat_food -= food_value
        self.stat_mood += mood_value
        self.stat_fatigue += fatigue_value

        # Mood can't be bigger than 100
        if self.stat_mood > 100:
            self.stat_mood = 100

        self.check_alive()

        return {
            "food": self.stat_food,
            "mood": self.stat_mood,
            "fatigue": self.stat_fatigue,
        }

    def move_do_nothing(
        self, age_value: int, food_value: int, mood_value: int, fatigue_value: int
    ) -> dict[str, int]:
        """Do nothing.

        Increase age and fatigue, decrease food and mood

        Returns 'dict'
        """

        self.stat_age += age_value
        self.stat_fatigue += fatigue_value
        self.stat_food -= food_value
        self.stat_mood -= mood_value

        self.check_alive()

        return {
            "age": self.stat_age,
            "fatigue": self.stat_fatigue,
            "food": self.stat_food,
            "mood": self.stat_mood,
        }

    def move_sleep(self, age_value: int, food_value: int) -> dict[str, int]:
        """Send your pet to bed.

        Increase age, decrease food, set fatigue to 0 and mood to 90.

        Returns 'dict'
        """

        self.stat_age += age_value
        self.stat_food -= food_value
        self.stat_fatigue = 0
        self.stat_mood = 90

        self.check_alive()

        return {
            "age": self.stat_age,
            "food": self.stat_food,
            "fatigue": 0,
            "mood": 90,
        }

    def check_alive(self) -> bool:
        """Checks if pet alive.

        Returns alive 'bool'
        """

        if self.stat_food <= 0 or self.stat_mood <= 0 or self.stat_fatigue >= 100:
            self.alive = False
            print(f"{Fore.RED}Your {self.name} died :(")
            exit(0)

        return self.alive

    def bye(self) -> None:
        print(f"\n{Fore.GREEN}Bye! Your pet will be waiting for you!")
        exit(0)


def main():
    gm = Gachimotchi(default_names, pet_art)

    try:
        gm.select_name()
        gm.show_banner()

        while gm.alive:
            gm.select_move()
    except (KeyboardInterrupt, EOFError):
        gm.bye()
    except Exception:
        print(f"{Fore.RED}Something get wrong!")
        exit(1)


if __name__ == "__main__":
    main()
