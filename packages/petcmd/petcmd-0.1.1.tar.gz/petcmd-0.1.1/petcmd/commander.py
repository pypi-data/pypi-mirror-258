
import traceback

class Commander:

	def __init__(self):
		self.commands = []
		self.help("help - Show help")(self.command("help")(self.help_command))

	def command(self, cmd, args=None, put_all_args=False):
		def dec(func):
			self.commands.append({
				"func": func,
				"cmd": cmd,
				"args": args or [],
				"put_all_args": put_all_args
			})
			return func

		return dec

	def help(self, description):
		def dec(func):
			for info in self.commands:
				if func == info["func"]:
					info["help"] = description
					return func
			raise Exception("You should use @command first")

		return dec

	def find_command(self, cmd):
		for info in self.commands:
			if cmd == info["cmd"] or cmd in info["cmd"]:
				return info
		return self.find_command("help")

	def process(self, argv):
		try:
			info = self.find_command(argv[1] if len(argv) > 1 else "help")
			args = argv[2:]
			if info["put_all_args"] and len(args) >= len(info["args"]):
				info["func"](**dict(zip(info["args"], args[:len(info["args"])])), args=args[len(info["args"]):])
			elif len(args) == len(info["args"]):
				info["func"](**dict(zip(info["args"], args)))
			else:
				print(info["help"])
		except Exception:
			print(traceback.format_exc())
			with open("petcmdlog.txt", "w") as file:
				file.write(traceback.format_exc())

	def help_command(self):
		print("Help:\n\n" + "\n".join(info["help"] for info in self.commands))
