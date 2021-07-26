import inspect
import distutils
import distutils.util

class VisualTest(object):

    def __init__(self, func: callable): 
        self.func = func
        self.types = {
            int.__name__: int,
            str.__name__: str,
            list.__name__: list,
            tuple.__name__: tuple,
            bool.__name__: bool,
            float.__name__: float
        }

    def _get_fargs(self):
        argspec = inspect.getfullargspec(self.func)
        args = []
        for arg in argspec.args:
            if arg in argspec.annotations:
                args.append((arg, argspec.annotations[arg]))
                continue
            args.append((arg, ''))
        return args

    def _str_type(self, _type):
        for key, value in self.types.items():
            if _type == value: return key
            continue
        return ''

    def _ask_list(self, arg_info: dict, _tuple: bool = False):
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
                if value_type == 'bool': list_value = distutils.util.strtobool(list_value)
                list_values.append(self.types[value_type](list_value))
            except ValueError:
                print(f'\nInvalid type, \'{value_type}\' required.')
                continue
        if _tuple:
            return tuple(list_values)
        return list_values

    def run(self):
        print("\nType '--type <type>' to change the type of an argument whose type is not specified.")
        print("Type '--exit-list' to leave a list.")
        print("Type '--exit' to exit the VisualTest.\n")
        fargs = self._get_fargs()
        i = 0
        values = []
        for farg in fargs:
            i += 1
            arg_name = farg[0]
            arg_type = self._str_type(farg[1])
            while 1:
                try:
                    if arg_type == 'list' or arg_type == 'tuple': break # Break if the [default] argument type is 'list' or 'tuple'
                    value = input(f'#{i} {arg_name} [{arg_type}] : ')
                    if value.startswith('--exit'): exit()
                    if arg_type == '' and value.startswith('--type') and value[7:] in self.types.keys():
                        arg_type = value[7:]
                        if arg_type == 'list' or arg_type == 'tuple': break # Break if the [choosen] argument type is 'list' or 'tuple'
                        value = input(f'#{i} {arg_name} [{arg_type}] : ')
                    if arg_type == 'int': value = int(value)
                    if arg_type == 'bool': value = bool(distutils.util.strtobool(value))
                    if arg_type == 'float': value = float(value)
                    break
                except ValueError:
                    print(f'\nInvalid type, \'{arg_type}\' required.')
                    continue
            if arg_type == 'list' or arg_type == 'tuple': 
                arg_info = (arg_name, arg_type, i)
                if arg_type == 'list': value = self._ask_list(arg_info = arg_info)
                if arg_type == 'tuple': value = self._ask_list(arg_info = arg_info, _tuple = True)
            values.append(value)
            continue
        results = self.func(*values)
        if results:
            print(f"\nReturns: \n---------\n{results}\n---------")