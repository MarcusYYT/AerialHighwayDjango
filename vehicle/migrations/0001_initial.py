# Generated by Django 4.1 on 2023-05-16 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_frame_cnt', models.IntegerField(null=True)),
                ('departure_frame_cnt', models.IntegerField(null=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.video')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_position', models.IntegerField()),
                ('y_position', models.IntegerField()),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.vehicle')),
                ('video_frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.videoframe')),
            ],
        ),
    ]