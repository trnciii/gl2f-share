import urllib.parse
from gl2f.core import lister, pretty, member, board
from .ayame import terminal as term

def to_hashtags(item):
	_, v = member.from_id(item.get('categoryId'))
	if v:
		fullname = v['fullname']
		group = board.get('id', item['boardId'])['group']
		if group in {'girls2', 'lucky2'}:
			group = group.capitalize()
		return [fullname, group]
	return []

def add_hash(t):
	return term.mod(f'#{t}', term.color('blue'))

def delimiter():
	return f'{"-"*20}・ _ ・{"-"*20}'

def preview(text, hashtags, urls):
	return f'''{delimiter()}
Preview
  text     : {text}
  hashtags : {' '.join(map(add_hash, hashtags))}
  urls     : {' '.join(map(lambda t:term.mod(t, term.color('blue', 'fl')), urls))}
{delimiter()}'''

def all_hashtags():
	tags = []
	tags.append('Girls2')
	tags += [v['fullname'] for v in member.of_group('girls2').values()]
	tags.append('Lucky2')
	tags += [v['fullname'] for v in member.of_group('lucky2').values()]
	tags.append('lovely2')
	tags += [v['fullname'] for k, v in member.of_group('lovely2').items() if k != 'lovely2staff']
	return tags

def compose(args):
	fm = pretty.from_args(args)
	items = term.selected(lister.list_contents(args), fm.format)

	text = input('Compose a post: ')
	hashtags = sorted(set(sum(map(to_hashtags, items), [])))
	urls = [board.content_url(i) for i in items]

	print(preview(text, hashtags, urls))

	if input('edit hashtags? (y/N)').lower() == 'y':
		hashtags = term.selected(all_hashtags(), format=add_hash, default=[i in hashtags for i in all_hashtags()])

	return text, hashtags, urls

def intent_x(text, hashtags, urls):
	import webbrowser
	webbrowser.register("termux-open '%s'", None)

	text_list = [text] + urls if text else urls

	params = []
	if text_list:
		params.append(f'text={urllib.parse.quote(" ".join(text_list))}')
	if hashtags:
		params.append(f'hashtags={urllib.parse.quote(",".join(hashtags))}')

	if params:
		intent = f'https://twitter.com/intent/tweet?{"&".join(params)}'
		print('opening:', intent)
		webbrowser.open(intent)
	else:
		print('nothing to post')


def share(args):
	import pyperclip

	text, hashtags, urls = compose(args)

	print(preview(text, hashtags, urls))
	todo = term.selected(['copy to clipboard', 'continue on X'])
	if 'copy to clipboard' in todo:
		pyperclip.copy(f'{text} {" ".join(urls)} {" ".join(f"#{t}" for t in hashtags)}')
	if 'continue on X' in todo:
		intent_x(text, hashtags, urls)


class Gl2f_Share:
	@staticmethod
	def add_to():
		return 'gl2f', 'share'

	@staticmethod
	def add_args(parser):
		lister.add_args(parser)
		pretty.add_args(parser)
		parser.add_argument('--target', choices={'x'}, default=None,
			help='where to share')
		parser.set_defaults(handler = lambda a:share(a))

	@staticmethod
	def set_compreply():
		return '__gl2f_complete_boards'

registrars = [Gl2f_Share]
