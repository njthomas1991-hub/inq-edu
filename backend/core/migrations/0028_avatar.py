# Generated migration for Avatar model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_remove_avatar_arm_color_remove_avatar_arm_style_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_type', models.CharField(choices=[('round_blue', 'Round Blue'), ('round_pink', 'Round Pink'), ('round_green', 'Round Green'), ('round_yellow', 'Round Yellow'), ('square_purple', 'Square Purple'), ('square_orange', 'Square Orange')], default='round_blue', max_length=20)),
                ('eye_type', models.CharField(choices=[('big_happy', 'Big Happy'), ('big_sleepy', 'Big Sleepy'), ('small_angry', 'Small Angry'), ('round_confused', 'Round Confused'), ('star_sparkly', 'Star Sparkly')], default='big_happy', max_length=20)),
                ('mouth_type', models.CharField(choices=[('smile', 'Smile'), ('grin', 'Big Grin'), ('open', 'Open'), ('neutral', 'Neutral'), ('tongue', 'Tongue Out')], default='smile', max_length=20)),
                ('accessory', models.CharField(choices=[('none', 'None'), ('cap', 'Cap'), ('hat', 'Hat'), ('crown', 'Crown'), ('glasses', 'Glasses'), ('bow', 'Bow')], default='none', max_length=20)),
                ('primary_color', models.CharField(default='#FF6B9D', help_text='Hex color', max_length=7)),
                ('accent_color', models.CharField(default='#FFB347', help_text='Hex color', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Avatar',
                'verbose_name_plural': 'User Avatars',
            },
        ),
    ]
