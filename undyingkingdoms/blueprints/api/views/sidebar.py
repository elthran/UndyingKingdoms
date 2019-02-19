from flask import jsonify, url_for
from flask.views import MethodView
from flask_login import current_user, login_required

from .helpers import patch_has_mail, patch_has_chat_message


class SideBarAPI(MethodView):
    @login_required
    def get(self):
        kingdom=current_user.county.kingdom

        patch_has_mail(current_user)
        patch_has_chat_message(current_user)

        user = dict(
            isAdmin=current_user.is_admin,
            hasMail=current_user.has_mail(),
            hasChatMessage=current_user.has_chat_message()
        )

        # the url names on the left here must match the ones
        # inside the SideBar.vue component.
        # This probably should just be a list?
        urls = dict(
            overview=url_for('overview', kingdom_id=0, county_id=0),
            economy=url_for('economy'),
            infrastructure=url_for('infrastructure'),
            military=url_for('military'),
            infiltration=url_for('infiltration'),
            diplomacy=url_for('diplomacy'),
            messages=url_for('messages'),
            chatroomAPI=url_for('chatroom_api'),
            kingdom=url_for('kingdom', kingdom_id=kingdom.id),
            achievements=url_for('achievements'),
            forum=url_for('forum', thread_id=0, post_id=0),
            guide=url_for('guide'),
            leaderboard=url_for('leaderboard'),
            versions=url_for('versions'),
            adminHomeAPI=url_for('admin.home_api'),
            logout=url_for('logout'),
        )

        return jsonify(
            user=user,
            urlFor=urls
        )
