import inspect

from typing import Callable

ListOfFunctions = list[Callable]
AllowedType = int | str | list | tuple | bool | float

def add(x: int, y: int) -> int:
    print(x + y)

def testing(x, y: int, z, a, b, c):
    return x, y, z, a, b, c

class VisualTest(object):

    def __init__(self, func: Callable): 
        self.func = func
        self.types: dict[str, AllowedType] = {
            int.__name__: int,
            str.__name__: str,
            list.__name__: list,
            tuple.__name__: tuple,
            bool.__name__: bool,
            float.__name__: float
        }

    @classmethod
    def _str_to_bool(cls, val: str) -> bool:
        v = val.lower()
        if v in ('y', 'yes', 'true', '1'):
            return True
        elif v in ('n', 'no', 'false', '0'):
            return False
        raise ValueError()

    @classmethod
    def _represents_int(cls, s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    def _get_fargs(self):
        argspec = inspect.getfullargspec(self.func)
        args = []
        for arg in argspec.args:
            if arg in argspec.annotations:
                args.append((arg, argspec.annotations[arg]))
                continue
            args.append((arg, ''))
        return args

    def _verify_str(self, _type: AllowedType) -> str:
        return next((key for key, value in self.types.items() if _type == value), '')

    def _ask_list(self, arg_info: dict, _tuple: bool = False) -> tuple[AllowedType] | list[AllowedType]:
        print(f'#{arg_info[2]} {arg_info[0]} [{arg_info[1]}] : ')
        list_values = []
        i = 0
        value_type = 'str'
        while 1:
            try:
                i += 1
                list_value = input(f"    #{i} [{value_type}] : ")
                if list_value == '--exit': exit()
                if list_value == '--exit-list': break
                if list_value.startswith('--type') and list_value[7:] in self.types.keys():
                    value_type = list_value[7:]
                    i -= 1
                    continue
                if value_type == 'bool': list_value = self._str_to_bool(list_value)
                list_values.append(self.types[value_type](list_value))
            except ValueError:
                print(f'\nInvalid type, \'{value_type}\' required.')
                continue
        return tuple(list_values) if _tuple else list_values

    def _ask_types(self, i, arg_name, arg_type) -> None:
        running = True
        while running:
            try:
                if arg_type in ['list', 'tuple']:
                    # Break if the [default] argument type is 'list' or 'tuple'
                    running = False
                    continue 
                value = input(f'#{i} {arg_name} [{arg_type}] : ')
                if value.startswith('--exit'): exit()
                if arg_type == '' and value.startswith('--type') and value[7:] in self.types.keys():
                    arg_type = value[7:]
                    if arg_type in ['list', 'tuple']: 
                        # Break if the [choosen] argument type is 'list' or 'tuple'
                        return value, arg_type
                    value = input(f'#{i} {arg_name} [{arg_type}] : ')
                if arg_type == 'int': value = int(value)
                if arg_type == 'bool': value = bool(self._str_to_bool(value))
                if arg_type == 'float': value = float(value)
                return value, arg_type
            except ValueError:
                print(f'\nInvalid type, \'{arg_type}\' required.')
                continue

    def run(self) -> None:
        print("\nType '--type <type>' to change the type of an argument whose type is not specified.")
        print("Type '--exit-list' to leave a list.")
        print("Type '--exit' to exit the VisualTest.\n")
        fargs = self._get_fargs()
        i = 0
        values = []
        for farg in fargs:
            i += 1
            arg_name = farg[0]
            arg_type = self._verify_str(farg[1])
            value, arg_type = self._ask_types(i, arg_name, arg_type)
            if arg_type in ['list', 'tuple']: 
                arg_info = (arg_name, arg_type, i)
            if arg_type == 'list': value = self._ask_list(arg_info = arg_info)
            if arg_type == 'tuple': value = self._ask_list(arg_info = arg_info, _tuple = True)
            values.append(value)
            continue
        print()
        if results := self.func(*values):
            print(f"Returns: \n---------\n{results}\n---------")
        print()

    @classmethod
    def run_choice_between(cls, l: ListOfFunctions) -> None:
        n = len(l)
        list_as_text = '\n'.join(f' ({i + 1}) - {f.__name__}' for i, f in enumerate(l))
        input_text = f"Choose the function to execute : \n {list_as_text}\n\n -> "

        raw_choice = input(input_text)

        while 1:
            if not cls._represents_int(raw_choice):
                print(f'The choice should be an integer ranging between 1 and {n}')
                raw_choice = input(input_text)
                continue
            elif not (1 <= int(raw_choice) <= n):
                print(f'The choice should be ranging between 1 and {n}')
                raw_choice = input(input_text)
                continue

            break

        index_choice = int(raw_choice) - 1
        f_choice = l[index_choice]

        vt = cls(f_choice)
        vt.run()

if __name__ == '__main__':
    # vt = VisualTest(testing)
    # vt.run()

    VisualTest.run_choice_between([testing])