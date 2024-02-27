
import inspect
import traceback
from typing import Type, Any, Callable, Iterable

class CommandException(Exception):
	pass

class Commander:

	def __init__(self, error_handler: Callable[[Exception], None] = None):
		self.__error_handler = error_handler
		self.__commands = []
		self.help("help - Show help")(self.command("help")(self.__help_command))

	def command(self, cmd: str):
		def dec(func):
			for command in self.__commands:
				if command["cmd"] == cmd:
					raise Exception(f"Duplicate command: {cmd}")
			self.__commands.append({"func": func, "cmd": cmd})
			return func
		return dec

	def help(self, description: str):
		def dec(func):
			for info in self.__commands:
				if func == info["func"]:
					info["help"] = description
					return func
			raise Exception("You should use @command first")
		return dec

	def process(self, argv: list[str]):
		info = self.__find_command(argv[1] if len(argv) > 1 else "help")
		try:
			args, kwargs = self.__parse_args(argv[2:], info["func"])
			info["func"](*args, **kwargs)
		except CommandException as e:
			print(e)
			print(info["help"])
		except Exception as e:
			print(traceback.format_exc())
			if isinstance(self.__error_handler, Callable):
				self.__error_handler(e)

	def __parse_value[T](self, arg: str, value: str, typehint: Type[T]) -> T:
		if typehint in (str, None):
			return value
		elif typehint in (int, float):
			try:
				return typehint(value)
			except ValueError:
				raise CommandException(f"{arg}: {value} can't be converted to {typehint}")
		elif typehint == bool:
			if value.lower() in ("1", "true"):
				return True
			elif value.lower() in ("0", "false"):
				return False
			raise CommandException(f"{arg}: {value} can't be converted to {typehint}")
		elif typehint in (list, tuple, set, dict):
			try:
				obj = eval(value)
				if isinstance(obj, typehint):
					return obj
			except Exception:
				pass
			raise CommandException(f"{arg}: {value} can't be converted to {typehint}")
		raise CommandException(f"{arg}: {value} can't be converted to unknown type {typehint}")

	def __parse_args(self, argv: list[str], func: Callable) -> tuple[list, dict]:
		spec = inspect.getfullargspec(func)
		positionals = spec.args if spec.defaults is None else spec.args[:-len(spec.defaults)]
		keyword = spec.kwonlyargs
		if spec.defaults is not None:
			keyword.extend(spec.args[-len(spec.defaults):])
		defaults = spec.kwonlydefaults or {}
		if spec.defaults is not None:
			defaults.update(dict(zip(spec.args[-len(spec.defaults):], spec.defaults)))
		values: dict[str, str] = {}
		free_values: list[str] = []

		# split positional and keyword arguments
		kwargs_indexes: list[int] = []
		for i, item in enumerate(argv):
			if i in kwargs_indexes:
				continue
			if item.startswith("-"):
				kwargs_indexes.append(i)
				typehint = spec.annotations.get(item[1:], None)
				if typehint == bool and (i + 1 >= len(argv) or argv[i + 1].startswith("-")):
					values[item[1:]] = "True"
					continue
				if i + 1 == len(argv) or argv[i + 1].startswith("-"):
					raise CommandException("Invalid usage: missing non bool option value")
				kwargs_indexes.append(i + 1)
				values[item[1:]] = argv[i + 1]
			else:
				free_values.append(item)

		# check all positional arguments are present
		args_by_kwargs = len([arg for arg in positionals if arg in values])
		if len(free_values) + args_by_kwargs < len(positionals):
			raise CommandException("Invalid usage: missing required positional arguments")

		# check positional arguments don't follow keyword arguments
		for i, arg in enumerate(positionals):
			if arg in values:
				for j, arg_ in enumerate(positionals[i + 1:]):
					if arg_ not in values:
						raise CommandException("Invalid usage: positional argument follows keyword argument")
				break

		# check unnecessary positional arguments
		if spec.varargs is None and len(free_values) + args_by_kwargs > len(positionals):
			raise CommandException("Invalid usage: unexpected number of positional arguments")

		# check unnecessary keyword arguments
		if spec.varkw is None and any(arg not in positionals and arg not in keyword for arg in values):
			raise CommandException("Invalid usage: unexpected number of keyword arguments")

		# collect all positional arguments including set as keyword arguments
		args: list[Any] = []
		first_arg_by_kwarg = len(positionals)
		for i, arg in enumerate(positionals):
			if arg in values:
				first_arg_by_kwarg = i
				break
		args.extend(self.__parse_value(
			positionals[i],
			free_values[i],
			spec.annotations.get(positionals[i], None)
		) for i in range(first_arg_by_kwarg))
		args.extend(self.__parse_value(
			positionals[i],
			values[positionals[i]],
			spec.annotations.get(positionals[i], None)
		) for i in range(first_arg_by_kwarg, len(positionals)))
		args.extend(self.__parse_value(
			spec.varargs,
			value,
			spec.annotations.get(spec.varargs, None)
		) for value in free_values[first_arg_by_kwarg:])

		# collect all keyword arguments
		kwargs = {
			arg: self.__parse_value(arg, value, spec.annotations.get(
				arg if arg in keyword else spec.varkw, None))
			for arg, value in values.items() if arg not in positionals
		}

		return args, kwargs

	def __find_command(self, cmd):
		for info in self.__commands:
			if isinstance(info["cmd"], str):
				if cmd == info["cmd"]:
					return info
			if isinstance(info["cmd"], Iterable):
				if cmd in info["cmd"]:
					return info
		return self.__find_command("help")

	def __help_command(self):
		print("Help:\n\n" + "\n".join(info["help"] for info in self.__commands))
