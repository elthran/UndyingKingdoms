from flask import jsonify, url_for
from flask.views import MethodView
from flask_login import current_user, login_required


class SidebarAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county
        kingdom = current_user.county.kingdom
        preferences = current_user.preferences

        user = dict(
            isAdmin=current_user.is_admin,
            hasMail=preferences.has_mail(),
            hasChatMessage=preferences.has_new_townhall_message(),
            isKing=kingdom.leader != 0,
            hasClan=current_user.clan is not None,
        )

        # the url names on the left here must match the ones
        # inside the SideBar.vue component.
        # This probably should just be a list?
        urls = dict(
            overview=url_for('overview'),
            economy=url_for('economy'),
            infrastructure=url_for('infrastructure'),
            military=url_for('military'),
            infiltration=url_for('infiltration'),
            casting=url_for('casting', target_id=county.id),
            research=url_for('research'),
            trading=url_for('trading'),
            messages=url_for('messages'),
            chatroom=url_for('chatroom'),
            kingdom=url_for('kingdom', kingdom_id=kingdom.id),
            royalCourt=url_for('royal_court'),
            achievements=url_for('achievements'),
            forum=url_for('forum', thread_id=0, post_id=0),
            guide=url_for('guide'),
            leaderboard=url_for('leaderboard'),
            profile=url_for('profile', tab='basic'),
            adminHomeAPI=url_for('admin.home_api'),
            clan=url_for('generic_clan'),
            logout=url_for('logout'),
        )

        return jsonify(
            debugMessage="You called on the sidebar api.",
            user=user,
            urlFor=urls
        ), 200
