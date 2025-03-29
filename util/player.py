from base import Player

player = Player("Dudley")

player.connect()
while True:
    player.take_turn(input('Player:'))
