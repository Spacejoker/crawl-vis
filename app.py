import urllib2
import os
from flask import Flask, render_template, request, redirect, url_for
from morgueParser import MorgueParser
from werkzeug import secure_filename

UPLOAD_FOLDER = 'C:\\Users\\Jensa\\projects\\python\\crawlvis\\uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world(morgue = None):
	url = 'http://rl.heh.fi/morgue//nago/morgue-nago-20130825-110603.txt'
	url = 'http://dobrazupa.org/morgue/Basil/morgue-Basil-20130826-021512.txt'
	url = 'http://crawl.akrasiac.org/rawdata/olizito/morgue-olizito-20130827-094816.txt'
	response = urllib2.urlopen(url)
	html = unicode(response.read(), 'utf-8')

	for line in open(os.path.join(UPLOAD_FOLDER, morgue)).readlines():
		print line
		try:
			html += unicode(line, 'utf-8') + "\n"
		except:
			pass

	data = MorgueParser().parse(html)
	
	#format some stuff for the web
	level_list = []

	for x in range(2, 28):
		if str(x) in data['level_map']:
			level_list.append({'level' : x, 'turn' : data['level_map'][str(x)]})
	data['level_list'] = level_list

	print data['level_list']

	return render_template('morgue.html', data=data)



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
	if file: #allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	    return hello_world(file.filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)

