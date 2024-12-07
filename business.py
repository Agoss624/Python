from dataclasses import dataclass

@dataclass
class Game:
    gameName:str = ""
    genre:str = ""
    platform:str = ""
    length:int = 0
    timePlayed:int = 0
    status:str = ""
    developer:str = ""
    releaseYear:int = 0
    gameOrder:int = 0
    gameID:int = 0

    @property
    def percentComp(self):
        try:
            comper = 100 * (self.timePlayed / self.length)
            return round(comper, 1)
        except ZeroDivisionError:
            return 0.0

class Gamelog:
    def __init__(self):
        self.__list = []

    @property
    def count(self):
        return len(self.__list)

    def add(self, game):
        return self.__list.append(game)
    
    def remove(self, number):
        return self.__list.pop(number-1)
    
    def get(self, number):
        return self.__list[number-1]
    
    def set(self, number, game):
        self.__list[number-1] = game
        
    def move(self, oldNumber, newNumber):
        game = self.__list.pop(oldNumber-1)
        self.__list.insert(newNumber-1, game)

    def __iter__(self):
        for game in self.__list:
            yield game
            
        
def main():
    gamelog = Gamelog()
    
    for game in gamelog:
        print(game.gameOrder, game.gameName, game.genre,
              game.platform, game.length, game.timePlayed, game.percentComp,
              game.status, game.developer, game.releaseYear)
        
    print("Bye!")

if __name__ == "__main__":
    main()
