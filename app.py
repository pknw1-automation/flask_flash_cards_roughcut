from flask import Flask, request, render_template
import pygsheets
import random
import json
import urllib
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/quiz", methods = ['POST','GET'])
def quiz():
    data = []
    data.append({
	"source_name": "Open Trivia DB",
	"info": "",
	"www": "https://opentdb.com/",
	"docs": "",
	"logo": "https://opentdb.com/images/logo-banner.png",
	"api": "https://opentdb.com/api.php?",
	"params": {
		"amount": {
			"required": "true",
			"paramater": "amount=",
			"info": "The number of questions to return from API",
			"min_value": "1",
			"max_value": "50",
			"default": "25"
		},
		"difficulty": {
			"required": "false",
			"paramater": "difficulty=",
			"info": "The difficulty of the question returned",
			"valid_entries": ["easy", "medium", "hard"],
			"default": "unset - so returns mixed"
		},
		"type": {
			"required": "false",
			"paramater": "type=",
			"info": "return only one type of format ",
			"a_value": "multiple",
			"b_value": "boolean",
			"default": "both types"
		},
		"misc": {
			"required": "",
			"paramater": "misc=",
			"info": "",
			"min_value": "",
			"max_value": "",
			"default": ""
		}
	}
})


    if request.method == "POST":

        questions = request.form.get('myQuestions')
        difficulty= request.form.get('difficulty')
        category = request.form.get('trivia')

        if questions == None:
            questions="amount=10"

        print(difficulty)
        #print("Number of Questions : "+questions)
        #print("Question Difficulty : "+difficulty)
        #print("Selected Category : "+category)
        if difficulty == 'mixed':
            source = "https://opentdb.com/api.php?"+questions
        else:
            source = "https://opentdb.com/api.php?"+questions+difficulty
        data = []
        with urllib.request.urlopen(source) as url:
            d = json.load(url)
            question_set = d['results']
            count = 1

        for item in question_set:
            shuffled_answers = []
            incorrect_answers = []
            shuffled_answers.append(item["correct_answer"].replace('&quot;','"').replace('&amp;','&').replace('&#039;','`').replace('&rsquo;','`'))
            for wrong_answer in item["incorrect_answers"]:
                shuffled_answers.append(wrong_answer.replace('&quot;','"').replace('&amp;','&').replace('&#039;','`').replace('&rsquo;','`'))
                incorrect_answers.append(wrong_answer.replace('&quot;','"').replace('&amp;','&').replace('&#039;','`').replace('&rsquo;','`'))
            data.append({
                'question_number': count,
                'question': item["question"].replace('&quot;','"').replace('&amp;','&').replace('&#039;','`').replace('&rsquo;','`'),
                'difficulty': item["difficulty"],
                'category': item["category"],
                'correct_answer': item["correct_answer"].replace('&quot;','"').replace('&amp;','&').replace('&#039;','`').replace('&rsquo;','`'),
                'incorrect_answers': incorrect_answers,
                'shuffled_answers' : shuffled_answers
            })
            count=(count+1)

    else:
        print("whoops")

    return render_template("quiz.html", data=data)




@app.route("/google/<Category>")
def fetch_data_from_sheets(Category="terraform"):
    gc = pygsheets.authorize(service_file='config/auth.json')
    sh = gc.open_by_key('1ciI0PV5hMJ-qEk9J5gznf0zfeeClxJ8n67nYOn1H2VM')
    worksheet = sh.worksheet('title',Category)

    rows = worksheet.get_all_records()

    data = []
    count = 1
    for row in rows:
        question  = row['Question']
        reference = row['Reference']
        correct_answer = row['Correct'].split(',') if row['Correct'] else []
        incorrect_answers = row['Incorrect'].split(',') if row['Incorrect'] else []

        shuffled_answers = correct_answer + incorrect_answers
        random.shuffle(shuffled_answers)
        data.append({
            'count': count,
            'question': question,
            'reference': reference,
            'difficulty': row['Difficulty'],
            'category': row['Category'],
            'correct_answer': correct_answer,
            'incorrect_answers': incorrect_answers,
            'shuffled_answers': shuffled_answers
            })
        count=(count+1)
    print(data)
    return render_template('google.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
