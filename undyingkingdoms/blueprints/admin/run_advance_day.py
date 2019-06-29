from flask import jsonify, current_app

from undyingkingdoms.models.worlds import World


def run_advance_day():
    try:
        world = World.query.first()
        world.advance_day()
        return jsonify(
            status='success',
            message='You successfully advanced the game world one day.'
        )
    except Exception as ex:
        if current_app.config['ENV'] != 'production':
            raise ex
        return jsonify(
            status='fail',
            message=f'Advance day failed due to: {ex}'
        )
