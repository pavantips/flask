from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

# Create Flask app FIRST
app = Flask(__name__)

# THEN configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your model
class FavoriteTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Your existing API configuration
api_key = 'YOUR_API_KEY'
headers = {'X-Auth-Token': ""}
url = "http://api.football-data.org/v4/matches"

# Function to fetch scores (similar to your previous project)
def fetch_scores():
    """
    Fetch live football match scores from the API.

    Returns:
        list: A list of dictionaries containing match data for the top 5 matches.
              Returns an empty list if no matches are found.
        str: An error message if an exception occurs during the API request.
    """
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        if 'matches' in data and len(data['matches']) > 0:
            matches = data['matches'][:5]  # Display top 5 matches for brevity
            return matches
        else:
            return []  # Return an empty list if no matches
    except Exception as e:
        return f"Error fetching data: {e}"

# STEP 3: YOUR CODE HERE

@app.route('/')


def load_index_page():
    """
    Flask route for the main page.

    Renders the index.html template.

    Returns:
        str: Rendered HTML content of the index page.
    """
    # STEP 4: YOUR CODE HERE
    return render_template('index.html')

# STEP 5: YOUR CODE HERE
@app.route('/scores')
def load_scores_page():
    """
    Flask route for the scores page.

    Renders the scores.html template with the current live scores.

    Returns:
        str: Rendered HTML content of the scores page.
    """
    # Initial score fetch
    live_scores = fetch_scores()

    # STEP 6: YOUR CODE HERE
    return render_template('scores.html', scores=live_scores)

if __name__ == '__main__':

    app.run(debug=True)
