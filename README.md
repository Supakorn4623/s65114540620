

1.
python manage.py createsuperuser





2.
python manage.py shell


from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.get(username='test')
user.role = 'owner' 
user.save()

3.
