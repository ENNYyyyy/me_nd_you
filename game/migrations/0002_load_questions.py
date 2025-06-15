from django.db import migrations


def load_questions(apps, schema_editor):
    from django.core.management import call_command

    try:
        call_command("loaddata", "questions.json")
    except Exception:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_questions),
    ]
