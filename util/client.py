from base import Player

player_1 = Player('inesa')
player_1.connect()
while True: 
    turn = input("Client: ")
    player_1.take_turn(turn)