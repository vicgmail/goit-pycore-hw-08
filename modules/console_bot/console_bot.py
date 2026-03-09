from .command_parser import command_parser, bot_init, bot_exit


def main():
    bot_init()
    while True:
        command = input("Enter a command (type 'exit' to quit): ").lower().strip()
        if command == "exit" or command == "close":
            bot_exit()
            break
        else:
            command_parser(command)


if __name__ == "__main__":
    main()