#! /usr/bin/env python3

#Author:        Asher Goss
#Last Updated:  May 15, 2024
#Version:       1.1
#Description:   Simple python program to track personal gaming
#               progression and statistics.


#module import
import db
import webbrowser
from business import Game, Gamelog

#defining constants
GENRE = ("FPS", "OpenWorld", "Soulslike", "Pixel", "Survival", "Crafting")
PLATFORM = ("PS5", "PC", "XBOX", "SWITCH")
STATUS = ("Playing", "Incomplete", "Completed", "Abandoned")

#display header/ui/menu
def display_header():
    print("*" * 80)
    print("*"+" " * 35 + "GameLog" + " " * 36 + "*")
    print("*"+" " * 78 + "*")

def display_menu():
    print("*" * 80)
    print("*" + "     MAIN MENU" + " " * 64 + "*")
    print("*" + " 1 – Display gamelog" + " " * 58 + "*")
    print("*" + " 2 - Fetch game information" + " " * 51 + "*")
    print("*" + " 3 – Add game" + " " * 65 + "*")
    print("*" + " 4 – Remove game" + " " * 62 + "*")
    print("*" + " 5 – Move game" + " " * 64 + "*")
    print("*" + " 6 – Update Game Status" + " " * 55 + "*")
    print("*" + " 7 – Update Play Time" + " " * 57 + "*")
    print("*" + " 8 - Display Menu" + " " * 61 + "*")
    print("*" + " 9 - Exit Gamelog" + " " * 61 + "*")
    print("*" + " " * 78 + "*")

def display_gamelog(games):
    if games == None:
        print("You haven't played any games lately.")        
    else:
        print(f"{'':2}{'Game':15}{'Genre':11}{'Sys':7}" + \
              f"{'Hrs':5}{'Done%':7}" + \
              f"{'Status':11}{'Developer':16}{'Year':4}")
        print("-" * 80)
        for game in games:
            print(f"{game.gameOrder:<2d}{game.gameName:<15}" + \
                  f"{game.genre:11}{game.platform:<7}" + \
                  f"{game.timePlayed:<5}{game.percentComp:<7.1f}" + \
                  f"{game.status:11}{game.developer:16}{game.releaseYear:4}")
            print()
    print()

def display_genre():
    print("*" * 32 + "Genre Selection" + "*" * 33)
    print("*          " + " | ".join(GENRE) + "           *")
    print("*" + " " * 78 + "*")

def display_platform():
    print("*" * 31 + "Platform Selection" + "*" * 31)
    print("*" + " " * 27 + " | ".join(PLATFORM) + " " * 27 + "*")
    print("*" + " " * 78 + "*")

def display_status():
    print("*" * 32 + "Status Selection" + "*" * 32)
    print("*" + " " * 17 + " | ".join(STATUS) + " " * 17 + "*")
    print("*" + " " * 78 + "*")

def display_separator():
    print("*" * 80)

#fetch information website    
def get_game_info():
    webbrowser.open(f"https://howlongtobeat.com")

#add a new game to the log
#website will launch with specified game info
def add_game(games):
    gameName = input("Game Title: ")
    webbrowser.open(f"https://howlongtobeat.com/?q={gameName}")
    genre = get_game_genre()
    platform = get_platform()
    length = input("Game Length(hrs): ") #round to nearest whole number
    timePlayed = input("Time Played(hrs): ") #round to nearest whole number
    status = get_status()
    developer = input("Game Developer: ")
    releaseYear = get_year()
    game_order = games.count + 1

    game = Game(gameName, genre, platform, length, timePlayed, status, developer, releaseYear, game_order)
    games.add(game)
    db.add_game(game)
    print(f"{game.gameName} slotted.\n")

#get and validate genre
def get_game_genre():
    while True:
        genre = input("Genre: ")
        if genre in GENRE:
            return genre
        else:
            print("Let's try that again.")
            display_genre()

def get_gamelog_number(games, prompt):
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("Invalid entry. Try that again.")
            continue

        if number < 1 or number > games.count:
            print("Invalid slot number. Try that again.")
        else:
            return number
        
#get and validate status       
def get_status():
    while True:
        status = input("Status: ")
        if status in STATUS:
            return status
        else:
            print("Let's try that again.")
            display_status()

#get and validate platform 
def get_platform():
    while True:
        platform = input("Platform: ")
        if platform in PLATFORM:
            return platform
        else:
            print("Let's try that again.")
            display_platform()            

#get and validate release year
def get_year():
    while True:
        try:
            year = int(input("Release Year: "))
        except ValueError:
            print("Invalid integer. Try again.")
            continue

        if year < 1975 or year > 2025:        
            print(f"Invalid entry. Must be between 1975 and 2024.")
        else:
            return year
        
#edit, remove, move games
def edit_game_status(games):
    number = get_gamelog_number(games, "Game slot: ")
    game = games.get(number)
    print()
    print(f"<>{game.gameName}<> | Current Status = {game.status}\n")
    display_status()
    print()
    game.status = get_status()
    db.update_game(game)
    print(f"{game.gameName}'s status has been updated.\n")
    print()
    
def edit_game_time(games):
    number = get_gamelog_number(games, "Gamelog number: ")
    game = games.get(number)
    print()
    print(f"<>{game.gameName}<>")
    print()
    game.timePlayed = int(input("Time Played(hrs): "))
    db.update_game(game)
    print(f"{game.gameName}'s time played has been updated.\n")
    print()
    
def move_game(games):
    old_number = get_gamelog_number(games, "Current game slot: ")
    game = games.get(old_number)
    print()
    print(f"{game.gameName}")
    new_number = get_gamelog_number(games, "New game slot: ")
    print()
    games.move(old_number, new_number)
    db.update_gamelog_order(games)
    print(f"{game.gameName} moved.\n")

def delete_game(games):
    number = get_gamelog_number(games, "Game slot: ")
    game = games.remove(number)
    print()
    db.delete_game(game)
    db.update_gamelog_order(games)
    print(f"{game.gameName} deleted.\n")
    print()

#run main  
def main():
    display_header()
    display_menu()
    display_genre()
    display_platform()
    display_status()

    db.connect()
    games = db.get_games()
    if games == None:
        games = Gamelog()         
    
    display_separator()
    
    while True:
        try:
            option = int(input(" Choose Menu Option (1-9): "))
        except ValueError:
            option = -1
            
        if option == 1:
            display_gamelog(games)
        elif option == 2:
            get_game_info()
        elif option == 3:
            add_game(games)
            games = db.get_games()
        elif option == 4:
            delete_game(games)
        elif option == 5:
            move_game(games)
        elif option == 6:
            edit_game_status(games)
        elif option == 7:
            edit_game_time(games)
        elif option == 8:
            display_menu()
        elif option == 9:
            db.close()
            print("See ya next time!")
            break
        else:
            print("Let's try that again.\n")
            display_menu()

if __name__ == "__main__":
    main()
