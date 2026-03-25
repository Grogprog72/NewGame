from typing import List
import random as rd


possible_move = ['stone', 'scissors', 'paper']
game_score = {'total_move': 0,
              'player_score': 0,
              'bot_score': 0}

def bot_turn(possible_move: List[str]) -> str:
    bot_move = rd.choice(possible_move)
    return bot_move

def player_turn() -> str:
    player_move = input()
    return player_move

def move_result(player_move: str, bot_move: str) -> None:
    if player_move.upper() == "К":
        enter = possible_move[0]
    elif player_move.upper() == "Н":
        enter = possible_move[1]
    elif player_move.upper() == "З":
        exit()
    else:
        enter = possible_move[2]
    print(f"Your move: {enter}\n Bot move: {bot_move}")
    game_score['total_move'] += 1
    if (possible_move.index(enter) - 1 == possible_move.index(bot_move)) or (possible_move.index(enter) == 0 and possible_move.index(bot_move) == 2):
        game_score['bot_score'] += 1
        print('bot win')
    elif possible_move.index(enter) == possible_move.index(bot_move):
        print('nothing win')
    else:
        game_score['player_score'] += 1
        print('player win')


def main_game() -> None:
    pass

print('Если хотите завершить игру и увидеть счёт, введите З')
vvod = input()
while vvod != 'З':
    move_result(vvod, bot_turn(possible_move))
    vvod = input()
print(f"Всего игр было сыграно {game_score['total_move']}.\nочки игрока равны {game_score['player_score']}.\nочки бота равны {game_score['bot_score']}.")