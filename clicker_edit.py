import base64
import zlib
import json
import argparse
import sys
from functools import reduce
import operator
from collections import defaultdict
import io

def opt_handle(parser, k, v):
	t = type(v)

	if t == type(None):
		pass
	elif t == bool:
		parser.add_argument("--{}".format(k), dest=k, action='store_true', help="Set {}".format(k))
		parser.add_argument("--not-{}".format(k), dest=k, action='store_false', help="Unset {}".format(k))
		tmp = {k: v}
		parser.set_defaults(**tmp)
	elif t == int:
		parser.add_argument("--{}".format(k), default=v, type=int, help="Set {}".format(k))
	elif t == float:
		parser.add_argument("--{}".format(k), default=v, type=float, help="Set {}".format(k))
	elif t == str:
		parser.add_argument("--{}".format(k), default=v, type=str, help="Set {}".format(k))
	elif t == dict:
		# Dicts get... Difficult.
		for k2, v2 in v.items():
			# TODO: Nicer help docs.
			opt_handle(parser, "{}.{}".format(k, k2), v2)
	else:
		# TODO: Currently no lists in the save file.
		# But we should implement handling them all the same.

		# append to list
		# remove index from list
		# remove value from list
		# clear list

		pass

def expand_args(jdata, parser):
	for k, v in sorted(jdata.items()):
		t = type(v)
		opt_handle(parser, k, v)

def load(filename):
	with open(filename, 'rb') as openFile:
		hashed = openFile.read(32)
		bdata = openFile.read()

	zdata = base64.b64decode(bdata)
	o = zlib.decompressobj(wbits=-15)
	jdata = json.loads(o.decompress(zdata))

	return jdata

def loads(source):
	with io.BytesIO(source) as openFile:
		hashed = openFile.read(32)
		bdata = openFile.read()

	zdata = base64.b64decode(bdata)
	o = zlib.decompressobj(wbits=-15)
	jdata = json.loads(o.decompress(zdata))

	return jdata

def compile(data, filename):
	dump = json.dumps(data).encode()
	with open(filename, 'wb+') as openFile:
		openFile.write(b'7e8bb5a89f2842ac4af01b3b7e228592')
		o = zlib.compressobj(wbits=-15)
		r = []
		r.append(o.compress(dump))
		r.append(o.flush())
		openFile.write(base64.b64encode(b''.join(r)))

def compiles(data):
	dump = json.dumps(data).encode()
	with io.BytesIO() as openFile:
		openFile.write(b'7e8bb5a89f2842ac4af01b3b7e228592')
		o = zlib.compressobj(wbits=-15)
		r = []
		r.append(o.compress(dump))
		r.append(o.flush())
		openFile.write(base64.b64encode(b''.join(r)))

		return openFile.getvalue()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		prog='clicker_edit'
	)
	parser.add_argument('filename')

	try:
		filename = sys.argv[1]
	except IndexError:
		parser.print_help()
		sys.exit(1)

	parser.add_argument("--output", "-o",
		help="File to write the output to. Must not be the same as <filename>",
		type=str,
		default="{}.new".format(filename))

	jdata = load(filename)

	# Assemble argparse based on found stuff:
	expand_args(jdata, parser)

	if len(sys.argv) == 2:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()

	# Recursive default dict, that creates a default dict.
	def make_dict():
		return defaultdict(make_dict)

	# Assembly args back into JSON:
	root = make_dict()
	for k in vars(args):
		if k == 'filename':
			continue
		elif k == 'output':
			continue

		v = getattr(args, k)
		if '.' not in k:
			root[k] = v
		else:
			# Magic to write to nested places.
			mapped = k.split('.')
			reduce(operator.getitem, mapped[:-1], root)[mapped[-1]] = v

	# Write the output
	compile(root, args.output)
