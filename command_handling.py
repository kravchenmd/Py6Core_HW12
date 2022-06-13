import functions as f
from classes import AddressBook


def choose_command(cmd: str) -> tuple:
    # redone with match-statement instead of if-ones
    # code is more readable and shorter! =)
    cmd = parse_command(cmd)

    match cmd:
        case ['close'] | ['exit'] | ['good', 'bye']:
            return f.exit_program, []
        case ['hello']:
            return f.hello, cmd[1:]
        case ['add', *_]:
            return f.add_contact, cmd[1:]
        case ['change', *_]:
            return f.edit_phone, cmd[1:]
        case ['remove', *_]:
            return f.remove_phone, cmd[1:]
        case ['phone', *_]:
            return f.show_phone, cmd[1:]
        case ['show', 'all'] | ['show_all']:
            return f.show_all_phones, []
        case ['edit', 'birthday'] | ['edit_birthday']:
            return f.edit_birthday, cmd[2:]
        case ['days', 'to', 'birthday', *_] | ['days_to_birthday', *_]:
            return f.days_to_birthday, cmd[1:]
        case ['save']:
            return f.save_contacts, cmd[1:]
        case ['load']:
            return f.load_contacts, cmd[1:]
        case ['find', *_]:
            return f.find_contact, cmd[1:]
        case _:
            return None, "Unknown command!"

    # Just in case here is old block with if-statements

    # if cmd in EXIT_COMMANDS:
    #     return exit_program, []
    #
    # cmd = parse_command(cmd)
    # cmd_check = cmd[0].lower()
    # if cmd_check == 'hello':
    #     return hello, cmd[1:]
    # if cmd_check == 'add':
    #     return add_contact, cmd[1:]
    # if cmd_check == 'change':
    #     return edit_phone, cmd[1:]
    # if cmd_check == 'remove':
    #     return remove_phone, cmd[1:]
    # if cmd_check == 'phone':
    #     return show_phone, cmd[1:]
    # if cmd_check == 'show' and len(cmd) > 1:
    #     # take into account that this command consists 2 words
    #     cmd_check = cmd[1].lower()
    #     if cmd_check == 'all':
    #         return show_all_phones, []
    # if cmd_check == 'edit' and len(cmd) > 1:
    #     # take into account that this command consists 2 words
    #     cmd_check = cmd[1].lower()
    #     if cmd_check == 'birthday':
    #         return edit_birthday, cmd[2:]
    # if cmd_check == 'days_to_birthday':
    #     return days_to_birthday, cmd[1:]
    # return None, "Unknown command!"


def parse_command(cmd: str) -> list:
    return cmd.strip().split(' ')  # apply strip() as well to exclude spaces at the ends


def handle_cmd(cmd: str, contacts: AddressBook) -> tuple:
    func, result = choose_command(cmd)
    if func:
        args = [contacts] + result if func not in (f.hello, f.exit_program) else result
        # else part to take into account hello() and show()
        result = func(*args)
    return func, result
