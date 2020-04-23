from flask import Flask, render_template, url_for



app = Flask(__name__)

posts = [
    {
        'author': 'Andre Williams',
        'title': 'Meal Plan 1',
        'content': 'First Post Content',
        'date_posted': 'April 20, 2020'
    },
        {
        'author': 'Lauren Williams',
        'title': 'Meal Plan 2',
        'content': 'Second Post Content',
        'date_posted': 'April 22, 2020'
    }
]

@app.route('/')
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)