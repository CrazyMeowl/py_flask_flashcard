from flask import Flask, request, jsonify, render_template_string, render_template
import json
import random
import webbrowser
app = Flask(__name__)

def load_config():
	with open("config.json",'r',encoding='utf-8') as f:
		config = json.load(f)
		return config

app_config = load_config()
@app.route('/', methods=['GET'])
def main():
	# Load collections from JSON
	with open('collections.json','r',encoding='utf-8') as f:
		collections = json.load(f)
	return render_template('index.html',name = app_config['name'],writer = app_config['writer'], collections = collections, reverse = '0')

@app.route('/add-question/', methods=['GET', 'POST'])
def add_question():
	collection = request.args.get('collection')
	# Load collections from JSON
	with open('collections.json','r',encoding='utf-8') as f:
		collections = json.load(f)

	if request.method == 'POST':
		
		question = request.form['question']
		answer = request.form['answer']

		collections[collection].append({'question': question, 'answer': answer})

		# Save collections to JSON
		with open('collections.json', 'w',encoding='utf-8') as f:
			json.dump(collections, f,ensure_ascii=False,indent=4)

		# return jsonify({'message': 'question added successfully'})

	return render_template('add_question.html',name = app_config['name'],writer = app_config['writer'], collection=collection, collections=collections, reverse = '0')

@app.route('/del-question/', methods=['DELETE'])
def del_question():
	collection = request.args.get('collection')
	question = request.args.get('question')
	# Load collections from JSON
	with open('collections.json','r',encoding='utf-8') as f:
		collections = json.load(f)
		collections[collection].pop(question)
		# Save collections to JSON
		with open('collections.json', 'w',encoding='utf-8') as f:
			json.dump(collections, f,ensure_ascii=False,indent=4)
	return "Success", 200
@app.route('/add-collection/', methods=['GET', 'POST'])
def add_collection():
	collection = request.args.get('collection')
	# Load collections from JSON
	with open('collections.json','r',encoding='utf-8') as f:
		collections = json.load(f)

	if request.method == 'POST':

		collection = request.form['collection']

		collections[collection] = []

		# Save collections to JSON
		with open('collections.json', 'w',encoding='utf-8') as f:
			json.dump(collections, f,ensure_ascii=False,indent=4)

		# return jsonify({'message': 'question added successfully'})

	return render_template('add_collection.html',name = app_config['name'],writer = app_config['writer'], collections=collections, reverse = '0')


@app.route('/study', methods=['GET'])
def study():
	collection = request.args.get('collection')
	reverse = request.args.get('reverse')

	# Load collections from JSON
	with open('collections.json','r',encoding='utf-8') as f:
		collections = json.load(f)
	def get_random_question(collection):
		with open('collections.json','r',encoding='utf-8') as f:
			collections = json.load(f)

		if collection not in collections:
			return None

		questions = collections[collection]
		if not questions:
			return None

		question = random.choice(questions)
		return question

	question = get_random_question(collection)
	if question == None:
		return render_template("study.html",name = app_config['name'],writer = app_config['writer'], collections = collections,question="Bộ Sưu Tập này Đang Trống, vui lòng quay lại trang trủ để thêm câu hỏi.", answer = "This collection is empty. You need to back to main page to add questions", collection=collection, reverse = '1')
	# return jsonify({'message': question})
	if reverse == '0':
		return render_template("study.html",name = app_config['name'],writer = app_config['writer'], collections = collections, question=question["question"], answer = question["answer"], collection=collection, reverse = '1')
	else:
		return render_template("study.html",name = app_config['name'],writer = app_config['writer'], collections = collections, question=question["answer"], answer = question["question"], collection=collection, reverse = '0')


if __name__ == '__main__':
	webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=True)
