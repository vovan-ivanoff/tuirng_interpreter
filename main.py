import argparse


states = {}

parser = argparse.ArgumentParser(
                    prog='TU4py',
                    description='Python implementation of tu4 interpreter',
                    epilog='madeby vovan_ivanoff')
parser.add_argument('filename')
parser.add_argument('-c', '--convert', action='store_true')
parser.add_argument("-o", "--out", default=".\\out.tu4")
args = parser.parse_args()


def read_states():
    """Функция чтения файла и составления словаря состояний"""
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
                rlenta[position] = doing[0]
            state = doing[1]
        command = rstates[state]
        print_lenta(rlenta, position, state)
    if state not in states.keys():
        print(f"Состояние {state} не определено!")


def export_states(rstates: dict, output_path: str):
    """Функция экспорта состояний в файл для MT Зайцева"""
    sorted_state_list = list(rstates.keys())
    sorted_state_list.sort()
    with open(output_path, "w", encoding="UTF-8") as f:
        for key in sorted_state_list:
            for key_inner in rstates[key]:
                f.write(f"{key:02},{key_inner},{rstates[key][key_inner][0]},\
{rstates[key][key_inner][1]:02}\n")


if __name__ == "__main__":
    read_states()
    if not args.convert:
        word = input()[::-1]
        lenta = list(word.rjust(99) + " ")[::-1]
        init_position = len(word)+1
        run_tu4(lenta, states, init_position)
    if args.convert:
        export_states(states, args.out)
