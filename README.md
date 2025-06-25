

1.
python manage.py createsuperuser





2.
python manage.py shell


from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.get(username='your_superuser_username')
user.role = 'owner'  # หรือ 'admin' หรือค่า role ที่ระบบยอมรับ
user.save()

3.
