from base import Player

player_1 = Player('inesa')
player_1.connect()
while True: 
    player_1.take_turn(input('Player: '))