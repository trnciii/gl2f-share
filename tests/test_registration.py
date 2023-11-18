from gl2f import command_builder
import gl2f_share

def test_registration():
	_, tree = command_builder.build(command_builder.builtin)
	for r in gl2f_share.registrars:
		parent, _ = r.add_to()
		assert parent in tree.keys()

	parser, tree = command_builder.build(command_builder.builtin + gl2f_share.registrars)

	for r in gl2f_share.registrars:
		p, n = r.add_to()
		command = p.split('.')[1:]
		command.append(n)
		args = parser.parse_args(command)
		assert hasattr(args, 'handler')
