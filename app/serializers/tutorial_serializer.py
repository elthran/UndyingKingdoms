from flask import url_for

# if installed: from flask_serializer import Serializer
from lib.flask_serializer.flask_serializer import Serializer


class TutorialSerializer(Serializer):
    def __init__(self, obj):
        self.advisor = obj.advisor
        self.is_clickable_step = obj.is_clickable_step()
        self.completed = obj.completed
        self.current_step = obj.current_step
        self.name = obj.name
        self.total_steps = obj.total_steps
        self.step_description = obj.get_step_description()
        self.url = url_for(
            'click_next_tutorial_step',
            tutorial_name=obj.name,
            current_step=obj.current_step
        )
