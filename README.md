1. เข้า Command Promt
2. พิมพ์ gh repo clone Supakorn4623/65114540620
3. แล้วเปิดใน VSCODE

การสร้างฐานข้อมูล
สร้าง database ใน command promt 
1.  mysql -u root -p
2.  CREATE DATABASE ชื่อฐานข้อมูล;
สร้างเสร็จแล้วเข้า VSCODE แล้วเข้าไปใน myproject แล้วกดเข้าไปแก้ไขไฟล์ใน
setting.py แล้วแก้ไขตรง database ให้ตรงกับข้อมูลที่เราสร้าง
3. เสร็จแล้วพิมพใน terminal   python manage.py migrate
4. python manage.py runserver แล้วเข้าลิงค์นี้ http://127.0.0.1:8000/accounts/owner/login/

การสร้างชื่อผู้ใช้งาน
1. พิมพ์ python manage.py createsuperuser แล้วกรอกข้อมูลชื่อผู้ใช้
2. แล้วเปลี่ยนโรล user เป็น owner พิมพ์  python manage.py shell

3. พิมพ์ตามนี้
   
from django.contrib.auth import get_user_model

User = get_user_model()

user = User.objects.get(username='ชื่อผู้ใช้')
user.role = 'owner'
user.save()

print(f"Role of {user.username} changed to {user.role}")








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
