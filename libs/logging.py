
debug = False


def print_log(message):
    global debug
    if debug:
        print(message)


def turn_on_debug(debug_value):
    global debug
    debug = debug_value
