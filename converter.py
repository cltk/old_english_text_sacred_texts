import os, re
import json
import pdb
import collections
from bs4 import BeautifulSoup
from django.utils.text import slugify

sourceLink = 'http://www.sacred-texts.com/neu/ascp/index.htm'
source = 'The Complete Corpus of Anglo-Saxon Poetry'
works = []

def jaggedListToDict(text):
	node = { str(i): t for i, t in enumerate(text) }
	node = collections.OrderedDict(sorted(node.items(), key=lambda k: int(k[0])))
	for child in node:
		if isinstance(node[child], list):
			if len(node[child]) == 1:
				node[child] = node[child][0]
			else:
				node[child] = jaggedListToDict(node[child])
	return node

def main():
	# Build json docs from txt files
	for root, dirs, files in os.walk("."):
		path = root.split('/')
		print((len(path) - 1) * '---', os.path.basename(root))
		for fname in files:
			if 'cltk_json' not in path:
				print((len(path)) * '---', fname)
				if fname.endswith('json'):
					"""

					We don't need to also convert these because we can convert them from the html

					with open(os.path.join(root, fname)) as f:
						data = json.load(f)
					work = {
						'originalTitle': data['title'],
						'englishTitle': data['title'],
						'author': 'Not available',
						'source': source,
						'sourceLink': sourceLink,
						'language': 'old_english',
						'text': {},
					}
					data['text'] = [node.strip() for node in data['text'].split('\n') if len(node.strip())]
					work['text'] = jaggedListToDict(data['text'])
					works.append(work)
					"""
					pass

				elif fname.endswith('html'):
					with open(os.path.join(root, fname), encoding='utf-8') as f:
						soup = BeautifulSoup(f.read(), 'html.parser')


					work = {
						'originalTitle': soup.title.text,
						'englishTitle': soup.title.text,
						'author': 'Not available',
						'source': source,
						'sourceLink': sourceLink,
						'language': 'old_english',
						'text': {},
					}

					stanzas = soup.findAll('dd')
					text = []

					for stanza in stanzas:
						lines = "".join([str(x) for x in stanza.contents]).split("<br>")
						for line in lines:
							line = line.replace("<br>", "").replace("</br>", "").strip()
							if len(line):
								text.append(line)

					work['text'] = jaggedListToDict(text)
					works.append(work)



	for work in works:
		fname = slugify(work['source']) + '__' + slugify(work['englishTitle'][0:100]) + '__' + slugify(work['language']) + '.json'
		fname = fname.replace(" ", "")
		if not os.path.exists('cltk_json'):
			os.makedirs('cltk_json')
		with open('cltk_json/' + fname, 'w') as f:
			json.dump(work, f)

if __name__ == '__main__':
	main()
