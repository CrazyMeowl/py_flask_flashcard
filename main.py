from flask import Flask, request, jsonify, render_template_string, render_template
import json
import random
import webbrowser
app = Flask(__name__)

def load_config():
	with open("config.json") as f:
		config = json.load(f)
		return config

app_config = load_config()
@app.route('/', methods=['GET'])
def main():
	return render_template('index.html',name = app_config['name'],writer = app_config['writer'])

@app.route('/add-word/<type>', methods=['GET', 'POST'])
def add_word(type):
	if request.method == 'POST':
		# Load data from JSON
		with open('dictionary.json','r',encoding='utf-8') as f:
			data = json.load(f)

		word = request.form['word']
		translation = request.form['translation']

		data[type].append({'word': word, 'translation': translation})

		# Save data to JSON
		with open('dictionary.json', 'w',encoding='utf-8') as f:
			json.dump(data, f,ensure_ascii=False,indent=4)

		# return jsonify({'message': 'Word added successfully'})

	return render_template('add.html',name = app_config['name'],writer = app_config['writer'], type=type)

@app.route('/study', methods=['GET'])
def study():
	word_type = request.args.get('word_type')
	reverse = request.args.get('reverse')
	types = ['vocabulary', 'phrasal verbs', 'word patterns']

	def get_random_word(word_type):
		with open('dictionary.json','r',encoding='utf-8') as f:
			data = json.load(f)

		if word_type not in data:
			return None

		words = data[word_type]
		if not words:
			return None

		word = random.choice(words)
		return word

	word = get_random_word(word_type)
	if word == None:
		return render_template("study.html",name = app_config['name'],writer = app_config['writer'], types=types,word="Từ Điển của loại từ này hiện đang trống về trang chủ để thêm từ", translation = "The dictionary for this word type is empty go back to the main page to add more word", word_type=word_type, reverse = '1')
	# return jsonify({'message': word})
	if reverse == '0':
		return render_template("study.html",name = app_config['name'],writer = app_config['writer'], types=types, word=word["word"], translation = word["translation"], word_type=word_type, reverse = '1')
	else:
		return render_template("study.html",name = app_config['name'],writer = app_config['writer'], types=types, word=word["translation"], translation = word["word"], word_type=word_type, reverse = '0')


if __name__ == '__main__':
	webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=True)
