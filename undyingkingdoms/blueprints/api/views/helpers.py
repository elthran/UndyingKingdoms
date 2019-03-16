from undyingkingdoms.models import Message


def patch_has_mail(target):
    def has_mail(self):
        return Message.query.filter_by(county_id=self.county.id, unread=True).first() is not None
    target.has_mail = has_mail.__get__(target, target.__class__)


def patch_has_chat_message(target):
    def has_chat_message(self):
        return None
    target.has_chat_message = has_chat_message.__get__(target, target.__class__)


def to_class_name(name):
    return ''.join(name.title().split('_'))
