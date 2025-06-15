from django.apps import AppConfig
from django.db import connection
from django.core.management import call_command
from django.apps import apps


class GameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "game"

    def ready(self):
        Question = apps.get_model("game", "Question")
        try:
            if connection.introspection.table_names() and Question.objects.count() == 0:
                call_command("loaddata", "questions.json")
        except Exception:
            pass  # Avoid crashing if migrations aren't ready
