import flask    
from flask import request,jsonify,make_response

app=flask.Flask(__name__)
app.config["DEBUG"]=True

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error":"not found"}),404)

@app.route('/',methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/users/all',methods=['GET'])
def get_user():
    return jsonify(books)

@app.route('/users/',methods=['GET'])
def get_user_by_id():
    if 'id' in request.args:
        id=request.args.get('id')
    else:
        return "Id not found."
    for data in books:
        if data["id"]==int(id):
            return jsonify(data)
    else:
        return "no data found."

@app.route('/users/<int:id>',methods=['GET'])
def get_user_byid(id):
    for data in books:
        if id==data["id"]:
            return jsonify(data)
    else:
        return "no data found"

@app.route('/users/',methods=['POST'])
def create_user():
    print(request.json)
    if not request.json and not 'title' in request.json and not 'author' in request.json:
        return jsonify({"error": "please provide correct data."})
    else:
        book={
            "id":len(books)-1,
            "title":request.json.get("title"),
            "author":request.json.get("author"),
            "first_sentence":"",
            "published":request.json.get("published",None)
        }
        books.append(book)
    return jsonify(books)

@app.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    if not request.json:
        return jsonify({"error":"please provide correct data."})
    else:
        for data in books:
            if data["id"]==id:
                data["title"]=request.json.get("title") if request.json.get("title") is not None else data["title"]
                data["author"]=request.json.get("author") if request.json.get("author") is not None else data["author"]
                data["first_sentence"]=request.json.get("first_sentence") if request.json.get("first_sentence") is not None else data["first_sentence"]
                data["published"]=request.json.get("published") if request.json.get("published") is not None else data["published"]
                return jsonify(data)
        else:
            return jsonify({"error":"please provide correct data."})
app.run()


