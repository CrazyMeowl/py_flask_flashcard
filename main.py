from flask import Flask, request, jsonify, render_template_string
import json
import random
app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
	return render_template_string("""
		<!DOCTYPE html>
		<html>
		  <body>
			<h1>Flask Dictionary</h1>
			<p><a href="/add-word/vocab">Add vocabulary</a></p>
			<p><a href="/add-word/phrasal">Add phrasal verbs </a></p>
			<p><a href="/add-word/patterns">Add word patterns</a></p>
			<p><a href="/study/vocab">Study vocabulary</a></p>
			<p><a href="/study/phrasal">Study phrasal verbs</a></p>
			<p><a href="/study/patterns">Study word patterns</a></p>

		  </body>
		</html>
	""")

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

	return render_template_string("""
		<!DOCTYPE html>
		<html>
		  <body>
			<h1 class="title">Flask Dictionary</h1 />
			<form method="post" action="/add-word/{{ type }}">
			  Word: <input type="text" name="word"><br />
			  Translation: <input type="text" name="translation"><br />
			  <input type="submit" value="Submit">
			  <p><a href="/">Quay về trang chủ</a></p>
			</form />
		  </body>
		</html>
	""", type=type)

@app.route('/study/<word_type>', methods=['GET'])
def study(word_type):
	
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
	# return jsonify({'message': word})
	return render_template_string("""
		<!DOCTYPE html>
		<html>
		  <body>
			<h1 style="display: none;">Flask Dictionary</h1>
			<h3 style="display: none;">Study</h3>
				<h4>{{ word["word"] }}</h4>
				<div id="translation" style="display: none;">
					Translation: {{ word["translation"] }}
				</div>

			<button onclick="location.href='/';">Quay về trang chủ</button>
			<button onclick="window.location.reload();">Tiếp Tục</button>
			<button onclick="trigger_answer()">Show nghĩa</button>
<script>
function trigger_answer() {
  var x = document.getElementById("translation");
  if (x.style.display === "none") {
	x.style.display = "block";
  } else {
	x.style.display = "none";
  }
}
</script>
		  </body>
		</html>
	""", types=types,word=word,word_type=word_type)




if __name__ == '__main__':
	app.run(debug=True)
