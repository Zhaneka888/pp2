# 1
class Bird:
    def move(self):
        return "walk"

class Duck(Bird):
    def move(self):
        return "swim"

print(Bird().move())
print(Duck().move())

# 2
class Printer:
    def print_text(self, text):
        return f"Print: {text}"

class FancyPrinter(Printer):
    def print_text(self, text):
        return super().print_text(text.upper()) + " !!!"

fp = FancyPrinter()
print(fp.print_text("hello"))

# 3
class Game:
    def __init__(self, name):
        self.name = name

class OnlineGame(Game):
    def __init__(self, name, players):
        super().__init__(name)
        self.players = players

g = OnlineGame("Chess", 2)
print(g.name, g.players)

# 4
def show_move(bird):
    print(bird.move())

show_move(Bird())
show_move(Duck())