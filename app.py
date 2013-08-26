import urllib2
from flask import Flask, render_template
from morgueParser import MorgueParser

app = Flask(__name__)

@app.route('/')
def hello_world(morgue=None):
	url = 'http://rl.heh.fi/morgue//nago/morgue-nago-20130825-110603.txt'
	url = 'http://dobrazupa.org/morgue/Basil/morgue-Basil-20130826-021512.txt'
	response = urllib2.urlopen(url)
	html = unicode(response.read(), 'utf-8')

	data = MorgueParser().parse(html)
	
	#format some stuff for the web
	level_list = []

	for x in range(2, 28):
		if str(x) in data['level_map']:
			level_list.append({'level' : x, 'turn' : data['level_map'][str(x)]})
	data['level_list'] = level_list

	print data['level_list']

	return render_template('morgue.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

