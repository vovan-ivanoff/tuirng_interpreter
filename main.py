import argparse


word = input()
lenta = list(word.rjust(99) + " ")[::-1]
init_position = len(word)+1
states = {}

parser = argparse.ArgumentParser(
                    prog='TU4py',
                    description='Python implementation of tu4 interpreter',
                    epilog='madeby vovan_ivanoff')
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename, "r", encoding="UTF-8") as f:
    lines = f.readlines()
for i in reversed(range(len(lines))):
    lines[i] = lines[i].split("//")[0].rstrip()
for line in lines:
    if len(line) < 1:
        continue
    toks = line.split(",")
    if int(toks[0]) not in states.keys():
        states[int(toks[0])] = {}
    states[int(toks[0])] = {**states[int(toks[0])], **{toks[1]: [toks[2],
                            int(toks[3])]}}


def print_lenta(plenta: list, pposition: int, pstate: int):
    """функция печати ленты машины тьюринга"""
    result = ""
    for char in plenta:
        if char == " ":
            result += "_"
        else:
            result += char
    print(result)
    print(" " * pposition + "^"+f"({pstate})")


def run_tu4(rlenta: list, rstates: dict, init_pos: int):
    """основная функция машины тьюринга"""
    state = 0
    position = init_pos
    command: dict = rstates[state]
    while state in states.keys():
        if position < 0 or position > 99:
            print(f"Вышли за пределы ленты!\n состояние: {state}")
            break
        if rlenta[position] in command.keys():
            doing = command[rlenta[position]]
            if rlenta[position] == doing[0] and doing[0] == " ":
                break
            if doing[0] == "<":
                position -= 1
            elif doing[0] == ">":
                position += 1
            else:
                lenta[position] = doing[0]
            state = doing[1]
        command = rstates[state]
        print_lenta(rlenta, position, state)
    if state not in states.keys():
        print(f"Состояние {state} не определено!")


run_tu4(lenta, states, init_position)
