# Generated by Django 5.0.1 on 2024-01-22 19:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stela_control', '0002_alter_billingrecipt_option_alter_company_business_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='description',
            new_name='content',
        ),
        migrations.AlterField(
            model_name='billingrecipt',
            name='option',
            field=models.CharField(choices=[('budget_marketing', 'Budget Marketing'), ('budget_development', 'Budget Development'), ('Monthly charge', 'Monthly charge'), ('Others', 'Others'), ('budget_design', 'Budget Design'), ('Billing receipt', 'Billing receipt')], max_length=60, null=True, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='company',
            name='business',
            field=models.CharField(blank=True, choices=[('Logistics and Transportation Services', 'Logistics and Transportation Services'), ('Restaurants and Food Services', 'Restaurants and Food Services'), ('Consulting', 'Consulting'), ('Marketing and Advertising Services', 'Marketing and Advertising Services'), ('IT Development Services', 'IT Development Services'), ('Media Creators', 'Media Creators'), ('E-commerce', 'E-commerce'), ('Education and Training', 'Education and Training'), ('Repair and Maintenance Services', 'Repair and Maintenance Services'), ('Beauty and Personal Care Services', 'Beauty and Personal Care Services'), ('Health and Wellness', 'Health and Wellness')], max_length=100, null=True, verbose_name='Business Type'),
        ),
        migrations.AlterField(
            model_name='content',
            name='card',
            field=models.CharField(blank=True, choices=[('card-light-danger', 'card-light-danger'), ('card-tale', 'card-tale'), ('card-light-blue', 'card-light-blue'), ('card-dark-blue', 'card-dark-blue')], max_length=50, null=True, verbose_name='Color Card'),
        ),
        migrations.AlterField(
            model_name='content',
            name='category',
            field=models.CharField(blank=True, choices=[('Events', 'Events'), ('News', 'News'), ('Stories', 'Stories'), ('Resources', 'Resources'), ('Interviews', 'Interviews'), ('Advices', 'Advices')], default='News', max_length=100),
        ),
        migrations.AlterField(
            model_name='facebookpagecomments',
            name='update_rate',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 16, 38, 12, 303910)),
        ),
        migrations.AlterField(
            model_name='itemdiscount',
            name='field',
            field=models.CharField(choices=[('Promotional Discount', 'Promotional Discount'), ('Initial Payment', 'Initial Payment'), ('Stela Payment Free Suscription', 'Stela Payment Free Suscription'), ('No Selected', 'No Selected')], max_length=60),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('Send', 'Send'), ('Draft', 'Draft')], max_length=20),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='template',
            field=models.CharField(choices=[('Style Template 3', 'Style Template 3'), ('Style Template 4', 'Style Template 4'), ('Style Template 2', 'Style Template 2'), ('Style Template 1', 'Style Template 1')], max_length=60, null=True, verbose_name='Style'),
        ),
        migrations.AlterField(
            model_name='order',
            name='section',
            field=models.CharField(choices=[('Store', 'Store'), ('Cloud Domains', 'Cloud Domains'), ('Cloud Elastic Instance', 'Cloud Elastic Instance'), ('Stela Marketing', 'Stela Marketing'), ('No Selected', 'No Selected'), ('Stela Websites', 'Stela Websites'), ('Stela Design', 'Stela Design')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='pathcontrol',
            name='step',
            field=models.CharField(choices=[('Step 2', 'Step 2'), ('Step 3', 'Step 3'), ('Step 4', 'Step 4')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='sendmoney',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='sitepolicy',
            name='section',
            field=models.CharField(blank=True, choices=[('billing_terms', 'Monthly Billing Terms'), ('monthly_terms', 'Billing Terms'), ('Cookie Policy', 'Cookie Policy'), ('Disclaimer', 'Disclaimer'), ('budget_development_terms', 'Budget Development Terms'), ('Privacy Policy', 'Privacy Policy'), ('Return Policy', 'Return Policy'), ('Terms and Conditions', 'Terms and Conditions'), ('budget_design_terms', 'Budget Design Terms'), ('budget_marketing_terms', 'Budget Marketing Terms')], default='Terms and Conditions', max_length=150),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='social',
            field=models.CharField(choices=[('Github', 'Github'), ('Tiktok', 'Tiktok'), ('X', 'X'), ('Facebook', 'Facebook'), ('Youtube', 'Youtube'), ('Linkedin', 'Linkedin'), ('Wikipedia', 'Wikipedia'), ('Instagram', 'Instagram')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='type',
            field=models.CharField(choices=[('Paypal', 'Paypal'), ('Binance', 'Binance'), ('Zelle', 'Zelle')], max_length=100, verbose_name='Type of Wallet'),
        ),
    ]
