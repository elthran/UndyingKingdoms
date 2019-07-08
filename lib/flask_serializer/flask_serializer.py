from .commands import serializer_cli
from .encoder_factory import meta_json_encoder_factory

# Convenience import
# noinspection PyUnresolvedReferences
from .base_serializer import Serializer


class FlaskSerializer(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.encoder = self.init_app(app)

    def init_app(self, app):
        app.cli.add_command(serializer_cli)
        encoder = meta_json_encoder_factory(app.name)

        # register extension with app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['serializer'] = encoder

        # override default encoder
        app.json_encoder = encoder
        return encoder
