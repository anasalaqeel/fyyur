#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, abort, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
import jinja2
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
env = jinja2.Environment()
env.globals.update(zip=zip)
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.jinja_env.filters['zip'] = zip

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:1234@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    show = db.relationship('Show', backref='venue')
    
    

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    show = db.relationship('Show', backref='artist')


class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  date = db.Column(db.DateTime)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  get=Venue.query.order_by('id')

  data = {
    "cities": [],
    "states": [],
    "venues": get
  }

  for n in get:
    if n.city not in data['cities']:
      data['cities'].append(n.city)
    for n in get:
      if n.state not in data['states']:
        data['states'].append(n.state)


  return render_template('pages/venues.html', zip=zip, areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():

  search_term = request.form.get('search_term', '')
  getResults = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  data = []
  for result in getResults:
    new_result = {
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": len(Show.query.filter_by(id=result.id).all()),
  }
    data.append(new_result)

  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  getVenues=Venue.query.filter_by(id=venue_id).first()
  getShows=Show.query.filter_by(venue_id=venue_id).first()
  getPastShows=Show.query.filter(Show.date <= '2019-12-21T21:30:00.000Z').filter_by(venue_id=venue_id).all()
  getUpcomingShows=Show.query.filter(Show.date > '2019-12-21T21:30:00.000Z').filter_by(venue_id=venue_id).all()

  upcomingShows = []
  pastShows = []


  for show in getUpcomingShows:
    shows={
        "upcoming_shows": [{
          "artist_id": show.artist_id,
          "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
          "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
          "start_time": str(show.date)
        }],
          "upcoming_shows_count": len(getUpcomingShows),
    }
    upcomingShows.append(shows)

  for show in getPastShows:
    shows={
        "past_shows": [{
          "artist_id": show.artist_id,
          "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
          "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
          "start_time": show.date
        }],
          "past_shows_count": len(getPastShows),
    }
    pastShows.append(shows)



  return render_template('pages/show_venue.html', venue=getVenues, upcomingShows=upcomingShows, pastShows=pastShows, delete_id=venue_id)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  error = False
  try:
    name = request.form.get('name', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    address = request.form.get('address', '')
    phone = request.form.get('phone', '')
    genres = request.form.getlist('genres')
    seeking_talent = request.form.get('seeking_talent', '')
    seeking_description = request.form.get('seeking_description', '')
    website = request.form.get('website', '')
    image_link = request.form.get('image_link', '')
    facebook_link = request.form.get('facebook_link', '')
    new_venue = Venue(
      name=name,
      city=city,
      state=state,
      address=address,
      phone=phone,
      genres=genres,
      seeking_talent=bool(seeking_talent),
      seeking_description=seeking_description,
      website=website,
      image_link=image_link,
      facebook_link=facebook_link
      )
    db.session.add(new_venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue'))



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  getArtist= Artist.query.order_by('id').all()
  data=[]


  for artist in getArtist:
    newArtist={
      "id": artist.id,
      "name": artist.name,
    }
    data.append(newArtist)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form.get('search_term', '')
  getResults = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

  data = []
  for result in getResults:
    new_result = {
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": len(Show.query.filter_by(id=result.id).all()),
  }
    data.append(new_result)

  response={
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  getArtist= Artist.query.filter_by(id=artist_id).first()
  getShows=Show.query.filter_by(artist_id=artist_id).first()
  getPastShows=Show.query.filter(Show.date <= '2019-12-21T21:30:00.000Z').filter_by(artist_id=artist_id).all()
  getUpcomingShows=Show.query.filter(Show.date > '2019-12-21T21:30:00.000Z').filter_by(artist_id=artist_id).all()

  pastShows = []
  upcomingShows = []

  for pastShow in getPastShows:
    past_show = {
      "venue_id": pastShow.venue_id,
      "venue_name": Venue.query.filter_by(id=pastShow.venue_id).first().name,
      "venue_image_link": Venue.query.filter_by(id=pastShow.venue_id).first().image_link,
      "start_time": pastShow.date
    }
    pastShows.append(past_show)
  
  for upcomingShow in getUpcomingShows:
    upcoming_show = {
      "venue_id": upcomingShow.venue_id,
      "venue_name": Venue.query.filter_by(id=upcomingShow.venue_id).first().name,
      "venue_image_link": Venue.query.filter_by(id=upcomingShow.venue_id).first().image_link,
      "start_time": upcomingShow.date
    }
    upcomingShows.append(upcoming_show)


  data={
    "id": getArtist.id,
    "name": getArtist.name,
    "genres": getArtist.genres,
    "city": getArtist.city,
    "state": getArtist.state,
    "phone": getArtist.phone,
    "seeking_venue": getArtist.seeking_venue,
    "image_link": getArtist.image_link,
    "website": getArtist.website,
    "facebook_link": getArtist.facebook_link,
    "seeking_description": getArtist.seeking_description,
    "past_shows": pastShows,
    "upcoming_shows": upcomingShows,
    "past_shows_count": len(pastShows),
    "upcoming_shows_count": len(upcomingShows),
  }

  return render_template('pages/show_artist.html', artist=data, delete_id=artist_id)

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist'))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    name = request.form.get('name', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    phone = request.form.get('phone', '')
    seeking_venue = request.form.get('seeking_venue', '')
    seeking_description = request.form.get('seeking_description', '')
    website = request.form.get('website', '')
    image_link = request.form.get('image_link', '')
    genres = request.form.get('genres', '')
    facebook_link = request.form.get('facebook_link', '')
    new_artist = Artist(
      name=name,
      city=city,
      state=state,
      phone=phone,
      seeking_venue=bool(seeking_venue),
      seeking_description=seeking_description,
      website=website,
      image_link=image_link,
      genres=genres,
      facebook_link=facebook_link
      )
    db.session.add(new_artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  getShows=Show.query.order_by('id').all()

  data = []

  for show in getShows:
    single_show = {
    "venue_id": show.venue_id,
    "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
    "artist_id": show.artist_id,
    "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
    "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
    "start_time": str(show.date)
    }
    data.append(single_show)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
    venue_id = request.form.get('venue_id', '')
    artist_id = request.form.get('artist_id', '')
    date = request.form.get('start_time', '')
    new_show = Show(
      venue_id=venue_id,
      artist_id=artist_id,
      date=date
    )
    db.session.add(new_show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
