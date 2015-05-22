import sys
import karaoke


def print_usage():
	print 'usage:'
	print '    python main.py song.kara'


def main(argv):
	if len(argv) == 1:
		print_usage()
		return

	config = karaoke.Config(argv[1])
	html = karaoke.HtmlGenerator(config)
	css = karaoke.CssGenerator(config)
	html.generate()
	css.generate()


if __name__ == '__main__':
	main(sys.argv)
