from datetime import datetime
from distutils.util import strtobool
from importlib import import_module

from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

get_models = lambda: import_module('app.models.exports')
get_forms = lambda: import_module('app.models.forms.message')


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        forms = get_forms()
        models = get_models()
        preferences = current_user.preferences

        form = forms.MessageForm()

        last_message_id = request.args.get('last_message_id', 0)
        # return all messages, filter in frontend
        messages = preferences.all_messages_query().filter(
            models.Chatroom.id > last_message_id
        ).all()
        preferences.last_checked_townhall = datetime.utcnow()  # Update that user has looked at town hall
        return jsonify(
            debugMessage=f"You called on {__name__}",
            maxLength=form.CONTENT_SIZE,
            CSRFToken=form.csrf_token.current_token,
            messages=messages,  # serialization is now auto-magic
            globalChatOn=preferences.global_chat_on,
        ), 200

    @login_required
    def post(self):
        forms = get_forms()
        models = get_models()
        county = current_user.county
        preferences = current_user.preferences
        form = forms.MessageForm()

        preferences.last_checked_townhall = datetime.utcnow()  # Update that user has looked at town hall

        is_global = strtobool(request.form['global_chat_on'])
        preferences.global_chat_on = is_global

        if form.validate_on_submit():
            forms = models.Chatroom(county.kingdom_id, county.id, form.content.data, is_global=is_global)
            forms.save()
            return jsonify(
                debugMessage='Your message was saved.',
            ), 201
        elif form.content.data == '':
            return jsonify(
                debugMessage='Update chat room selection',
            ), 303
        else:
            return jsonify(
                debugMessage='Failed form validation.'
            ), 400
