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

def make_blue(s):
	return term.mod(s, term.color('blue', 'fl'))

def add_hash(t):
	return make_blue(f'#{t}')

def delimiter():
	return f'{"-"*20}・ _ ・{"-"*20}'

class Post:
	def __init__(self, text, hashtags, title, urls):
		self.text = text
		self.hashtags = hashtags
		self.title = title
		self.urls = urls

	def preview(self):
		if len(self.urls)>1:
			urls_string = ''.join(map(lambda t:f'\n  - {make_blue(t)}', self.urls))
		elif len(self.urls) == 1:
			urls_string = f' {make_blue(self.urls[0])}'
		else:
			urls_string = ''

		return f'''{delimiter()}
Preview
  text          : {self.text}
  hashtags      : {' '.join(map(add_hash, self.hashtags))}
  article title : {self.title}
  urls          : {urls_string}
{delimiter()}'''

	def build(self):
		return f'{self.text} {self.title} {" ".join(self.urls)} {" ".join(f"#{t}" for t in self.hashtags)}'

def add_title(items):
	return ' '.join(map(lambda i:i['values']['title'], items)) if 'n' != input('add article title? (Y/n)').lower() else ''

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
	if args.pick:
		items = lister.list_contents(args)
		items = [items[i-1] for i in args.pick if 0<i<=len(items)]
		print('Articles to share')
		for i in items:
			fm.print(i)
	else:
		items = term.selected(lister.list_contents(args), fm.format)

	text = input('Compose a post: ')
	hashtags = sorted(set(sum(map(to_hashtags, items), [])))
	title = add_title(items)
	urls = [board.content_url(i) for i in items]

	post = Post(text, hashtags, title, urls)

	print(post.preview())

	if input('edit hashtags? (y/N)').lower() == 'y':
		post.hashtags = term.selected(all_hashtags(), format=add_hash, default=[i in hashtags for i in all_hashtags()])

	return post

def intent_x(post):
	import webbrowser
	webbrowser.register("termux-open '%s'", None)

	text_list = [post.text, post.title] + post.urls if post.text else post.urls

	params = []
	if text_list:
		params.append(f'text={urllib.parse.quote(" ".join(text_list))}')
	if post.hashtags:
		params.append(f'hashtags={urllib.parse.quote(",".join(post.hashtags))}')

	if params:
		intent = f'https://twitter.com/intent/tweet?{"&".join(params)}'
		print('opening:', intent)
		webbrowser.open(intent)
	else:
		print('nothing to post')


def share(args):
	import pyperclip

	post = compose(args)
	print(post.preview())

	todo = term.selected(['copy to clipboard', 'continue on X', 'print'])
	if 'copy to clipboard' in todo:
		pyperclip.copy(post.build())
	if 'continue on X' in todo:
		intent_x(post)
	if 'print' in todo:
		print(post.build())


class Gl2f_Share:
	@staticmethod
	def add_to():
		return 'gl2f', 'share'

	@staticmethod
	def add_args(parser):
		parser.description = 'Compose a post for SNS'

		lister.add_args(parser)
		pretty.add_args(parser)
		parser.add_argument('--target', choices={'x'}, default=None,
			help='where to share')
		parser.add_argument('--pick', type=int, nargs='+',
			help='select articles to show')
		parser.set_defaults(handler = lambda a:share(a))

	@staticmethod
	def set_compreply():
		return '__gl2f_complete_boards'

registrars = [Gl2f_Share]
