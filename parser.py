import json
import keyboard


def parse_file(filename):
    with open(filename, "r") as read_file:
        data = read_file.read()

    return parse_string(data)


def parse_string(data):
    lines = get_lines(data)
    parsed = []

    for line in lines:
        parsed.append(parse_line(line))

    parsed = parse_lines(parsed)

    return parsed


def get_lines(data):
    lines = data.split("\n")
    remove_element(lines, "")
    remove_element(lines, "\t")

    stripped = [x.strip() for x in lines]
    return stripped


def parse_line(line):
    # Remove comments
    temp = line.split("!")
    command = temp[0].strip()

    # Process the command
    if command:
        # Get arguments
        args = command.split(" ")
        args = [x.strip() for x in args]
        remove_element(args, "")
        remove_element(args, "t")

        # Check if command is valid
        if args[0] not in ("mouse", "wait", "loop", "end"):  # Get only keyboard commands
            if len(args) > 2:
                raise SyntaxError(f"Too many arguments: {line}\n Expected 1 argument but got {len(args)-1}")

            if args[0].lower() not in ("click", "hold", "release"):
                raise SyntaxError(f"Illegal operation in line '{line}': Unknown operation '{args[0]}'")

            # Check if arguments are valid
            norm_arg = keyboard._canonical_names.normalize_name(args[1].lower())
            if (norm_arg not in keyboard._canonical_names.canonical_names.values() and
                    norm_arg not in keyboard._canonical_names.all_modifiers):
                if ord(norm_arg[0]) not in range(97, 123) or len(norm_arg) != 1:  # If no single character a-z
                    if norm_arg not in (f"f{x}" for x in range(1, 13)):
                        raise ValueError(f"Invalid argument in line '{line}': '{args[1]}'")

            return args[0], [args[1]]

    return ""


def parse_lines(arr):
    return []


def remove_element(data, c):
    while c in data:
        data.remove(c)


parse_file("example_macro/basic_keys.macro")
parse_file("example_macro/basic_loops.macro")
parse_file("example_macro/comments.macro")
parse_file("example_macro/move_mouse.macro")
parse_file("example_macro/special_keys.macro")
parse_file("example_macro/toggle_keys.macro")
parse_file("example_macro/use_mouse.macro")
parse_file("example_macro/waiting.macro")
