#!/usr/bin/python3
""" Console Module """
import ast
import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.rfind(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].strip().strip('"\'')

                # if arguments exist beyond __id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    _args = pline

            line = ' '.join([_cmd, _cls, _id, _args]).strip()

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    @staticmethod
    def cast_value(value):
        """ Casts a param value to a string, a float or an integer

        A string starts with a double quote, its underscores are replaced
        by spaces and escaped double quotes are unescaped. A value that
        contains a dot is a float, anything else is an integer.
        Values that cannot be cast return None.
        """
        try:
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('_', ' ')
                return value.replace('\\"', '"')
            if '.' in value:
                return float(value)
            return int(value)
        except (ValueError, TypeError):
            return None

    def do_create(self, args):
        """ Create an object of any class

        Usage: create <class name> [<key name>=<value> ...]
        """
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split(' ')
        if arg_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.classes[arg_list[0]]()
        for param in arg_list[1:]:
            if '=' not in param:
                continue
            key, value = param.split('=', 1)
            if not key or not value:
                continue
            value = HBNBCommand.cast_value(value)
            if value is None:
                continue
            setattr(new_instance, key, value)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className> [<key name>=<value> ...]\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
        else:
            print(obj)

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
        else:
            storage.delete(obj)
            storage.save()

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            objects = storage.all(HBNBCommand.classes[args])
        else:
            objects = storage.all()

        for obj in objects.values():
            print_list.append(str(obj))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for key in storage.all().keys():
            if args and args == key.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    @staticmethod
    def parse_arguments(arguments):
        """ Splits arguments into quoted or space/comma separated tokens"""
        tokens = []
        index = 0
        length = len(arguments)
        while index < length:
            char = arguments[index]
            if char in ' ,':
                index += 1
            elif char in '"\'':
                end = arguments.find(char, index + 1)
                if end == -1:
                    tokens.append(arguments[index + 1:])
                    break
                tokens.append(arguments[index + 1:end])
                index = end + 1
            else:
                end = index
                while end < length and arguments[end] not in ' ,':
                    end += 1
                tokens.append(arguments[index:end])
                index = end
        return tokens

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        new_dict = objects[key]

        # first determine if kwargs or args
        rest = args[2].strip()
        if rest.startswith('{') and rest.endswith('}'):
            try:
                kwargs = ast.literal_eval(rest)
            except (SyntaxError, ValueError):
                kwargs = None
            if isinstance(kwargs, dict):
                for att_name, att_val in kwargs.items():
                    if att_name in HBNBCommand.types:
                        att_val = HBNBCommand.types[att_name](att_val)
                    setattr(new_dict, att_name, att_val)
                new_dict.save()
                return

        tokens = HBNBCommand.parse_arguments(rest)
        if not tokens or not tokens[0]:  # check for att_name
            print("** attribute name missing **")
            return
        if len(tokens) < 2:  # check for att_value
            print("** value missing **")
            return

        att_name = tokens[0]
        att_val = tokens[1]

        # type cast as necessary
        if att_name in HBNBCommand.types:
            att_val = HBNBCommand.types[att_name](att_val)

        # update attribute with name, value pair
        setattr(new_dict, att_name, att_val)
        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
