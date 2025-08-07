import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    # Correction BUG 1 "email"
    email = request.form.get('email')
    club = next((club for club in clubs if club['email'] == email), None)
    
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    # Trouver la compétition et le club
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    competition_places = int(competition['numberOfPlaces'])
    club_points = int(club['points'])

    # Correction BUG 4: Limite de 12 places par club 
    if placesRequired > 12:
        flash("Error: You cannot book more than 12 places per competition.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # Correction BUG 5  : Vérification des points du club
    if placesRequired > club_points:
        flash("Your club doesn't have enough points.")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    
    # Correction BUG 3: Mise à jour des points du club
    competition['numberOfPlaces'] = competition_places - placesRequired
    club['points'] = club_points - placesRequired

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# Correction BUG 2: Tableau d'affichage des points
@app.route('/pointsDisplay')
def pointsDisplay():
    return render_template('points_display.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))