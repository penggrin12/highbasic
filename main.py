# Forked edits by penggrin12 licensed under MIT.
# Full license text in LICENSE.

# 2025 BISCGAMES
# --- DISCORD: biscgames
# --- GITHUB: biscgames
# PLEASE DO NOT COPY ANY OF MY CODE, THANK YOU
# YOU MAY ONLY FORK THE REPOSITORY FOR MAJOR CODE CHANGES, AND NOTHING MINOR

from shlex import split as lex_split
from sys import argv as args, exit
import traceback
from typing import Any, Callable, Iterable

cut = False
variables: dict[str, Any] = {"!ver": "1.3_1", "!newline": "\n", "!emptyline": "", "!$": "$"}
functions: dict[str, Callable]
classes = {}
arguments = []
macros: dict[str, list[str]] = {"exampleMacro": ['println "Hello, World!"']}


def interpret_each(code: Iterable[str]) -> None:
    for token in code:
        token: str = token.strip()
        if not token:
            continue

        tokenSplit: list[str] = lex_split(token, False)  # TODO: treat : as actual comments
        try:
            functions[tokenSplit[0]](tokenSplit[1:])
        except Exception as e:
            traceback.print_exception(e)  # TODO: why not just let it raise?


def convert_to_num(value: str) -> int | float | str:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def is_referencing_var(value: str) -> bool:
    return value.startswith("$")


def test_for_variable(value: str):
    if is_referencing_var(value):
        while is_referencing_var(value):
            pointer = 0
            while value[pointer] == "$":
                pointer += 1
            val = variables[value[pointer:]]
            value = value.replace(value[pointer:], str(val))
            value = value[1:]
    else:
        if ">>" in value:
            classRef = value.split(">>")
            if classRef[0] in classes:
                return (
                    classes[classRef[0]][classRef[1]]
                    if not isinstance(classes[classRef[0]][classRef[1]], list)
                    else "MACRO"
                )
            else:
                return (
                    variables[classRef[0]][classRef[1]]
                    if not isinstance(variables[classRef[0]][classRef[1]], list)
                    else "MACRO"
                )
    return value


def println(args: list) -> None:
    print(test_for_variable(args[0]))


def var(args: list) -> None:
    val = test_for_variable(args[0])
    value = (
        convert_to_num(test_for_variable(args[1]))
        if str(test_for_variable(args[1])).isdigit()
        else test_for_variable(args[1])
    )
    if "." not in val:
        if not val.startswith("!") or val not in variables:
            variables[val] = value
        else:
            print(
                "Attempt to modify read-only variable handled with this message. Variable: {}".format(
                    args[0]
                )
            )
    else:
        item, prop = val.split(".", 1)
        if item not in variables:
            print("o0w =eo0ooot0-iii-kfe")
            return
        variables[item][prop] = value


def operator(args: list) -> None:
    left = test_for_variable(args[0])
    if isinstance(variables[left], str):
        rights = args[1:-1]
    else:
        rights = [convert_to_num(test_for_variable(s)) for s in args[1:-1]]
    op = args[-1]

    for right in rights:
        rightVal = test_for_variable(str(right))
        if isinstance(variables[left], str):
            if op == "+":
                variables[left] += str(rightVal)
            elif op == "*":
                variables[left] = variables[left] * convert_to_num(rightVal)
        else:
            if op == "+":
                variables[left] += convert_to_num(rightVal)
            elif op == "-":
                variables[left] -= convert_to_num(rightVal)
            elif op == "*":
                variables[left] *= convert_to_num(rightVal)
            elif op == "/":
                variables[left] /= convert_to_num(rightVal)
            elif op == "%":
                variables[left] %= convert_to_num(rightVal)


def noop(_) -> None:
    pass


def macro(args: list) -> None:
    global arguments
    val = test_for_variable(args[0])
    if val not in macros:
        if "." in val:
            item = val.split(".")[0]
            var = val.split(".")[1]

            arr = list(
                s.replace("this", item)
                for s in (classes[item][var] if item in classes else variables[item][var])
            )
            if len(args) > 2:
                arguments = args[2:]
            interpret_each(arr)
        else:
            macros[val] = []
    else:
        interpret_each(macros[val])


def in_item(args: list) -> None:
    item = test_for_variable(args[1])
    if args[0] == "macro":
        macros[item].append(" ".join(args[2:]))
    else:
        if args[0] not in classes[item]:
            classes[item][args[0]] = []
        if len(args) > 2:
            classes[item][args[0]].append(" ".join(args[2:]))


def readln(args: list) -> None:
    if not args[1].startswith("!"):
        variables[args[1]] = input(args[0])
    else:
        print(
            "Attempt to modify read-only variable handled with this message. Variable: {}".format(
                args[1]
            )
        )


def equal_int(args: list) -> None:
    true = " ".join(args[2:])
    if int(variables[test_for_variable(args[0])]) == int(test_for_variable(args[1])):
        interpret_each([true])


def unless_int(args: list) -> None:
    true = " ".join(args[2:])
    if int(variables[test_for_variable(args[0])]) != int(test_for_variable(args[1])):
        interpret_each([true])


def equal_str(args: list) -> None:
    true = " ".join(args[2:])
    if str(variables[test_for_variable(args[0])]) == str(test_for_variable(args[1])):
        interpret_each([true])


def unless_str(args: list) -> None:
    true = " ".join(args[2:])
    if str(variables[test_for_variable(args[0])]) != str(test_for_variable(args[1])):
        interpret_each([true])


def string(args: list) -> None:
    val = test_for_variable(args[0])
    if not val.startswith("!"):
        variables[val] = str(test_for_variable(args[1]))
    else:
        print(
            "Attempt to modify read-only variable handled with this message. Variable: {}".format(
                args[0]
            )
        )


def num(args: list) -> None:
    val = test_for_variable(args[0])
    if not val.startswith("!"):
        variables[val] = convert_to_num(test_for_variable(args[1]))
    else:
        print(
            "Attempt to modify read-only variable handled with this message. Variable: {}".format(
                args[0]
            )
        )


def to_num(args: list) -> None:
    variables[test_for_variable(args[0])] = convert_to_num(variables[args[0]])


def to_string(args: list) -> None:
    variables[test_for_variable(args[0])] = str(variables[args[0]])


def dynamic_if(args: list) -> None:
    pass


def dynamic_unless(args: list) -> None:
    pass


def print_(args: list) -> None:
    print(test_for_variable(args[0]), end="")


def module(args: list) -> None:
    val = test_for_variable(args[0])
    if len(args) > 0:
        try:
            with open(val, "r") as f:
                lines = f.readlines()
                if lines[0].strip() == "module":
                    interpret_each(lines[1:])
                else:
                    print(
                        '"Module" {} is not a valid module. (put "module" at the first line of the file to confirm it is a module)'.format(
                            args[0]
                        )
                    )
        except Exception as e:
            print('Filepath "{}" cannot be run. {}'.format(args[1], e))


def destroy(args: list) -> None:
    if args[0] == "macro":
        if args[-1] == "r":
            macros[test_for_variable(args[1])] = []
        else:
            del macros[test_for_variable(args[1])]
    if args[0] == "var":
        del variables[test_for_variable(args[1])]


def concat(args: list) -> None:
    rights = args[1:]
    for right in rights:
        variables[test_for_variable(args[0])] += test_for_variable(right)


def iterate(args: list) -> None:
    global cut
    cut = False
    i = int(test_for_variable(args[0]))
    while i < int(test_for_variable(args[1])) and not cut:
        interpret_each(macros[test_for_variable(args[-1])])
        i += 1


def nick(args: list) -> None:
    if not test_for_variable(args[0]) == "macro":
        functions[test_for_variable(args[1])] = functions[test_for_variable(args[0])]
        del functions[test_for_variable(args[0])]
    else:
        macros[test_for_variable(args[2])] = macros[test_for_variable(args[1])]
        del macros[test_for_variable(args[1])]


def cut_func(args: list) -> None:
    global cut
    cut = True


def class_for(args: list) -> None:
    global arguments
    val = test_for_variable(args[0])
    variables[val] = classes[test_for_variable(args[1])]
    if "classConstructor" in variables[val].keys():
        if len(args) > 2:
            arguments = args[2:]
        interpret_each(s.replace("this", val) for s in variables[val]["classConstructor"])


def get_arg(args: list) -> None:
    global arguments
    var([args[0], arguments[int(test_for_variable(args[1]))]])


def class_func(args: list) -> None:
    classes[test_for_variable(args[0])] = {}


def get_class_val(args: list) -> None:
    val = test_for_variable(args[0])
    arg1 = test_for_variable(args[1])
    variables[test_for_variable(args[-1])] = (
        classes[val][arg1] if val in classes else variables[val][arg1]
    )


functions: dict[str, Callable] = {
    "var": var,
    "operator": operator,
    "println": println,
    ":": noop,
    "#": noop,
    "group": noop,
    "macro": macro,
    "in": in_item,
    "readln": readln,
    "equalInt": equal_int,
    "unlessInt": unless_int,
    "equalString": equal_str,
    "unlessString": unless_str,
    "if": dynamic_if,
    "unless": dynamic_unless,
    "string": string,
    "num": num,
    "toNum": to_num,
    "toString": to_string,
    "print": print_,
    "module": module,
    "del": destroy,
    "concat": concat,
    "iterate": iterate,
    "nick": nick,
    "cut": cut_func,
    "classFor": class_for,
    "class": class_func,
    "classVal": get_class_val,
    "arg": get_arg,
}


def main() -> None:
    code: list[str] = []

    if len(args) < 2:
        code = input(
            f"Welcome to HighBasic\n!ver: {variables['!ver']}\nAdd an argument for filename next time to interpret a .hb file!\n>> "
        ).split("\n")
    else:
        try:
            with open(args[1], "r") as f:
                lines: list[str] = f.readlines()
                if lines[0].strip() == "module":
                    code = [
                        'println "Modules cannot run by theirselves and must be run by a main .hb file."'
                    ]
                else:
                    code = lines
        except Exception as e:
            print(f'Filepath "{args[1]}" cannot be run. {e}')
            exit(1)

    interpret_each(code)


if __name__ == "__main__":
    main()
