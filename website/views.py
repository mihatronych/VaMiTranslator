from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Translate
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')#Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
            db.session.add(new_note) #adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/translate', methods=['GET', 'POST'])
@login_required
def index():
    pass
    if request.method == 'POST':
        source = request.form.get('tr_request')#Gets the note from the HTML
        model_name = request.form.get('model_name')  # Gets the note from the HTML

        if len(source) < 1:
            flash('Note is too short!', category='error')
        else: # ВОТ ЗДЕСЬ БУДЕТ МАГИЯ ТРАНСЛЕЙТА
            new_note = Translate(source=source, translate=source, model_name=model_name, user_id=current_user.id)  #providing the schema for the translate
            db.session.add(new_note) #adding the note to the database
            db.session.commit()
            flash('Translated!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})