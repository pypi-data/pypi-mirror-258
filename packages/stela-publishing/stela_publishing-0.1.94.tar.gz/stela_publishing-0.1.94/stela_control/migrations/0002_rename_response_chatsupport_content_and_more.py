# Generated by Django 5.0.1 on 2024-02-07 18:48

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stela_control', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatsupport',
            old_name='response',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='message',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='host',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='ip',
        ),
        migrations.AddField(
            model_name='chatsupport',
            name='superuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_superuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.CharField(default='no phone', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='billingrecipt',
            name='option',
            field=models.CharField(choices=[('Others', 'Others'), ('budget_design', 'Budget Design'), ('budget_development', 'Budget Development'), ('budget_marketing', 'Budget Marketing'), ('Billing receipt', 'Billing receipt'), ('Monthly charge', 'Monthly charge')], max_length=60, null=True, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='chatsupport',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company',
            name='business',
            field=models.CharField(blank=True, choices=[('Marketing and Advertising Services', 'Marketing and Advertising Services'), ('Media Creators', 'Media Creators'), ('Consulting', 'Consulting'), ('IT Development Services', 'IT Development Services'), ('Restaurants and Food Services', 'Restaurants and Food Services'), ('Repair and Maintenance Services', 'Repair and Maintenance Services'), ('E-commerce', 'E-commerce'), ('Logistics and Transportation Services', 'Logistics and Transportation Services'), ('Education and Training', 'Education and Training'), ('Health and Wellness', 'Health and Wellness'), ('Beauty and Personal Care Services', 'Beauty and Personal Care Services')], max_length=100, null=True, verbose_name='Business Type'),
        ),
        migrations.AlterField(
            model_name='content',
            name='card',
            field=models.CharField(blank=True, choices=[('card-light-blue', 'card-light-blue'), ('card-dark-blue', 'card-dark-blue'), ('card-light-danger', 'card-light-danger'), ('card-tale', 'card-tale')], max_length=50, null=True, verbose_name='Color Card'),
        ),
        migrations.AlterField(
            model_name='facebookpagecomments',
            name='update_rate',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 7, 15, 47, 17, 8544)),
        ),
        migrations.AlterField(
            model_name='itemdiscount',
            name='field',
            field=models.CharField(choices=[('Promotional Discount', 'Promotional Discount'), ('Stela Payment Free Suscription', 'Stela Payment Free Suscription'), ('No Selected', 'No Selected'), ('Initial Payment', 'Initial Payment')], max_length=60),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Send', 'Send')], max_length=20),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='template',
            field=models.CharField(choices=[('Style Template 4', 'Style Template 4'), ('Style Template 3', 'Style Template 3'), ('Style Template 2', 'Style Template 2'), ('Style Template 1', 'Style Template 1')], max_length=60, null=True, verbose_name='Style'),
        ),
        migrations.AlterField(
            model_name='order',
            name='section',
            field=models.CharField(choices=[('Store', 'Store'), ('Cloud Domains', 'Cloud Domains'), ('Stela Design', 'Stela Design'), ('Stela Marketing', 'Stela Marketing'), ('No Selected', 'No Selected'), ('Cloud Elastic Instance', 'Cloud Elastic Instance'), ('Stela Websites', 'Stela Websites')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='pathcontrol',
            name='step',
            field=models.CharField(choices=[('Step 2', 'Step 2'), ('Step 4', 'Step 4'), ('Step 3', 'Step 3')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='sendmoney',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='sitepolicy',
            name='section',
            field=models.CharField(blank=True, choices=[('Return Policy', 'Return Policy'), ('Disclaimer', 'Disclaimer'), ('billing_terms', 'Monthly Billing Terms'), ('budget_development_terms', 'Budget Development Terms'), ('Terms and Conditions', 'Terms and Conditions'), ('Privacy Policy', 'Privacy Policy'), ('monthly_terms', 'Billing Terms'), ('Cookie Policy', 'Cookie Policy'), ('budget_marketing_terms', 'Budget Marketing Terms'), ('budget_design_terms', 'Budget Design Terms')], default='Terms and Conditions', max_length=150),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='social',
            field=models.CharField(choices=[('X', 'X'), ('Youtube', 'Youtube'), ('Instagram', 'Instagram'), ('Wikipedia', 'Wikipedia'), ('Facebook', 'Facebook'), ('Tiktok', 'Tiktok'), ('Linkedin', 'Linkedin'), ('Github', 'Github')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='url',
            field=models.URLField(max_length=80),
        ),
        migrations.AlterField(
            model_name='support',
            name='option',
            field=models.CharField(choices=[('Others', 'Others'), ('I have a problem with my subscription', 'I have a problem with my subscription'), ('My delivery has been delayed', 'My delivery has been delayed'), ('My account has an error', 'My account has an error'), ('Payments Issue', 'Payments Issue'), ('I have a problem with my project', 'I have a problem with my project')], max_length=60, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='support',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='type',
            field=models.CharField(choices=[('Binance', 'Binance'), ('Paypal', 'Paypal'), ('Zelle', 'Zelle')], max_length=100, verbose_name='Type of Wallet'),
        ),
    ]
