import urllib2
import os
from flask import Flask, render_template, request, redirect, url_for
from morgueParser import MorgueParser
from werkzeug import secure_filename

UPLOAD_FOLDER = 'C:\\Users\\Jensa\\projects\\python\\crawlvis\\uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world(html=None):
	if not html:
		return 'no file'
	
	data = MorgueParser().parse(html)
	
	#format some stuff for the web
	level_list = []

	for x in range(2, 28):
		if str(x) in data['level_map']:
			level_list.append({'level' : x, 'turn' : data['level_map'][str(x)]})
	data['level_list'] = level_list

	print data['level_list']

	return render_template('morgue.html', data=data)


@app.route('/link', methods=['GET', 'POST'])
def link_filk():
	if request.method == 'POST':
		url = request.form['fileurl']
		response = urllib2.urlopen(url)
		html = unicode(response.read(), 'utf-8')
		return hello_world(html)
	return '''
	<!doctype html>
	<title>Provide morgue link</title>
	<h1>Provide morgue link</h1>
	<form action="" method=post enctype=multipart/form-data>
	<p><input type=text name=fileurl>
	 <input type=submit value=Upload>
	</form>
	'''

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file: #allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			html = ""
			for line in open(os.path.join(UPLOAD_FOLDER, filename)).readlines():
				print line
				try:
					html += unicode(line, 'utf-8') + "\n"
				except:
					pass
			return hello_world(html)
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

