import json


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
    multi_comment = ""

    # Remove comments
    temp = line.split("!")
    command = temp[0].strip()
    if len(temp) > 1:
        if len(temp[1]) > 0:
            # Check if start of multiline-comment
            if temp[1][0] == "-":
                multi_comment = "s"

    if len(command) > 0:
        # Check if end of multiline-comment
        if command[len(command)-1] == "-":
            multi_comment = "e"
            command = None
    else:
        command = None

    print(command, temp, multi_comment)

    return ""


def parse_lines(arr):
    return []


def remove_element(data, c):
    while c in data:
        data.remove(c)


parse_file("example_macro/comments.macro")
