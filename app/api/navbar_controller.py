from flask import url_for
from flask_login import current_user, login_required

from lib.base_controller import CRUDMethodView


class NavbarController(CRUDMethodView):
    @login_required
    def read(self):
        county = current_user.county
        kingdom = current_user.county.kingdom
        preferences = current_user.preferences

        user = dict(
            is_admin=current_user.is_admin,
            has_mail=preferences.has_mail(),
            has_chat_message=preferences.has_new_townhall_message(),
            is_king=kingdom.leader != 0,
            has_clan=current_user.clan is not None,
        )

        # the url names on the left here must match the ones
        # inside the Navbar.vue component.
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
            royal_court=url_for('royal_court'),
            achievements=url_for('achievements'),
            forum=url_for('forum', thread_id=0, post_id=0),
            guide=url_for('guide'),
            leaderboard=url_for('leaderboard'),
            profile=url_for('profile', tab='basic'),
            admin_home_api=url_for('admin.home_api'),
            clan=url_for('generic_clan'),
            logout=url_for('logout'),
        )

        return dict(
            debug_message="You called on the navbar api.",
            user=user,
            url_for=urls,
        ), 200
