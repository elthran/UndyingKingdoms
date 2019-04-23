from flask import url_for


def vue_safe_nbsp(s):
    """Returns a string with all spaces non-breaking.

    This string will render safely in vue.js
    """
    return '\u00a0'.join(s.split())


def vue_safe_metadata_mod(mod, county, is_percent=True):
    """Simplify a metatdata object to race and background.

    All values are assumed to be percents.
    """
    vue_safe_mod = {}
    race_mod = mod.get(county.race)
    background_mod = mod.get(county.background)
    if race_mod:
        value = int(race_mod[1] * 100) if is_percent else race_mod[1]
        vue_safe_mod['race'] = dict(
            name=vue_safe_nbsp(race_mod[0]),
            value=value
        )
    if background_mod:
        value = int(background_mod[1] * 100) if is_percent else background_mod[1]
        vue_safe_mod['background'] = dict(
            name=vue_safe_nbsp(background_mod[0]),
            value=value
        )

    return vue_safe_mod

def vue_safe_array(value):
    """Convert all tuples to lists.

    This also marks the value as safe to prevent escaping.
    I may need to make this more complex over time.
    """

    new = []
    if value is not None:
        for item in value:
            if isinstance(item, tuple):
                new.append(list(item))
            else:
                new.append(item)
        return new
    return None


def vue_safe_form(form):
    """A simplified form object suitable for vue.

    I might need to check type to accommodate other forms.
    """

    vs_form = {}

    for field in form:
        key = field.name
        if key != 'csrf_token':
            try:
                vs_form[key] = dict(
                        choices = vue_safe_array(field.choices),
                        id=key
                    )
            except AttributeError:
                vs_form[key] = dict(
                    id=key,
                    html=field()
                )
        else:
            vs_form[key] = dict(
                value=field.current_token,
                id=key,
                html=field()
            )
    return vs_form


def vue_safe_news(news):
    """Convert a list of news objects in a JSON serializable form."""

    for event in news:
        yield dict(
            day=event.day,
            title=event.title,
            content=event.content
        )


def vue_safe_message(message):
    # return "({time}) {leader}: {content}".format(time=self.get_pretty_timestamp(), leader=self.get_county_leader_name(), content=self.content)
    return dict(
        time=message.time_created,
        leader=message.get_county_leader_name(),
        content=message.content,
        room="global" if message.is_global else "kingdom",
        id=message.id,
        leaderUrl=url_for('enemy_overview', county_id=message.county_id)
    )


def vue_safe_reply(post):
    county = post.author.county
    return dict(
        timeCreated=post.time_created,
        author=post.get_author(),
        leaderUrl=url_for('enemy_overview', county_id=county.id),
    )

def vue_safe_post(post):
    most_recent_reply = post.get_most_recent_reply()
    return dict(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.get_author(),
        url=url_for('forum', thread_id=post.thread_id, post_id=post.id),
        mostRecentReply=vue_safe_reply(most_recent_reply) if most_recent_reply else None,
        votes=post.get_votes(),
        replyCount=post.get_reply_count(),
    )


def vue_safe_thread(thread):
    post = thread.get_most_recent_post()
    return dict(
        id=thread.id,
        title=thread.title,
        author=thread.get_author(),
        mostRecentPost=vue_safe_reply(post) if post else None,
        postCount=thread.get_post_count(),
        url=url_for('forum', thread_id=thread.id, post_id=0),
        votes=thread.get_votes(),
        # views=thread.get_views()
    )
