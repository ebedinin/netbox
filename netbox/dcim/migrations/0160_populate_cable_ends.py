from django.db import migrations


def populate_cable_terminations(apps, schema_editor):
    Cable = apps.get_model('dcim', 'Cable')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    cable_termination_models = (
        apps.get_model('dcim', 'ConsolePort'),
        apps.get_model('dcim', 'ConsoleServerPort'),
        apps.get_model('dcim', 'PowerPort'),
        apps.get_model('dcim', 'PowerOutlet'),
        apps.get_model('dcim', 'Interface'),
        apps.get_model('dcim', 'FrontPort'),
        apps.get_model('dcim', 'RearPort'),
        apps.get_model('dcim', 'PowerFeed'),
        apps.get_model('circuits', 'CircuitTermination'),
    )

    for model in cable_termination_models:
        ct = ContentType.objects.get_for_model(model)
        model.objects.filter(
            id__in=Cable.objects.filter(termination_a_type=ct).values_list('termination_a_id', flat=True)
        ).update(cable_end='A')
        model.objects.filter(
            id__in=Cable.objects.filter(termination_b_type=ct).values_list('termination_b_id', flat=True)
        ).update(cable_end='B')


class Migration(migrations.Migration):

    dependencies = [
        ('circuits', '0037_new_cabling_models'),
        ('dcim', '0159_populate_cable_paths'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_cable_terminations,
            reverse_code=migrations.RunPython.noop
        ),
    ]
