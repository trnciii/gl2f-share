class Gl2f_Share:
	@staticmethod
	def add_to():
		return 'gl2f', 'share'

	@staticmethod
	def add_args(parser):
		parser.set_defaults(handler = lambda _:print(f'share installed'))

registrars = [Gl2f_Share]
