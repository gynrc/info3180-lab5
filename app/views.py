"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from .models import Movie
from .forms import MovieForm

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if a filename has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods='POST')
def movies():
    form = MovieForm()
    if form.validate_on_submit():
        title = form.title.data
        poster = form.poster.data
        description = form.description.data

        # save movie to the database
        movie = Movie(title=title, poster=poster, description=description)
        db.session.add(movie)
        db.session.commit()

        # save the poster file to the uploads folder
        if poster and allowed_file(poster.filename):
            filename = secure_filename(poster.filename)
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # return a success message and the movie data in JSON format
        return jsonify({
            'message': 'Movie successfully added',
            'title': movie.title,
            'poster': movie.poster,
            'description': movie.description,
        })
    else:
        # return a list of form errors in JSON format
        errors = form_errors(form)
        return jsonify({'errors': errors})
    

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404