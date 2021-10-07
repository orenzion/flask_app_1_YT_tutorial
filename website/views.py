from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required  # makes sure a user cant acceess the homepage unless he is logged in
def home():
    # check if the request is of a POST type
    if request.method == 'POST':
        # get the note from the form
        note = request.form.get('note')

        # check if anything was typed in the note
        if len(note) < 1:
            flash('Note is too short!', category='error')
        # create note and add it to the db
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!', category='success')
    return render_template("home.jinja", user=current_user)


# handle the delete-note request from the client
@views.route('delete-note', methods=['POST'])
def delete_note():
    # this time the data isn't sent through the 'form' so we'll need to get it from the request body - turn it to a python dictionary object
    note = json.loads(request.data)
    # get the node id from the dictionary
    noteId = note['noteId']
    # query the note from the db using the 'get' method - checks the primary key in the schema in the db
    note = Note.query.get(noteId)
    # check if note exists
    if note:
        print('ttt')
        # if the user who is signed in owns this note
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    # return an empty fson object - we have to return something as a response to the request
    return jsonify({})
