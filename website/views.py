from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Translate
from . import db
import json
from .utils import rnn

views = Blueprint('views', __name__)


@views.route('/example', methods=['GET', 'POST'])
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


@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        source = request.form.get('translate') # Gets the note from the HTML
        model_name = request.form.get('model_name')  # Gets the note from the HTML
        print(source)
        print(model_name)
        if len(source) < 1:
            flash('Note is too short!', category='error')
        else: # ВОТ ЗДЕСЬ БУДЕТ МАГИЯ ТРАНСЛЕЙТА
            if model_name == 'rnn':
                tr_res = rnn.decode_sequence_rnn(source)
                new_translate = Translate(source=source, translate=tr_res, model_name=model_name, user_id=current_user.id)  #providing the schema for the translate
                db.session.add(new_translate) #adding the note to the database
                db.session.commit()
                flash('Translated!', category='success')
    return render_template("index.html", user=current_user)

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

@views.route('/delete-translate', methods=['POST'])
def delete_translate():
    translate = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    translateId = translate['translateId']
    print(translateId)
    translate = Translate.query.get(translateId)
    if translate:
        if translate.user_id == current_user.id:
            db.session.delete(translate)
            db.session.commit()

    return jsonify({})