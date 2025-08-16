from django.shortcuts import render, redirect, get_object_or_404
from shopsales.forms import ProductForm, StockForm ,ShelfForm
from shopsales.models import Product , Shelf 
from django.http import JsonResponse
from collections import defaultdict

def sales_dashboard(request):
    return render(request, 'sales_dashboard.html')

def product_management(request):
    products = Product.objects.all()
    product_id = request.GET.get('product_id')  # ดึง product_id จาก query string
    if request.method == 'POST':
        if product_id:  # ถ้ามี product_id แสดงว่าเป็นการแก้ไข
            product = Product.objects.get(id=product_id)
            form = ProductForm(request.POST, instance=product)  # ส่งข้อมูลของสินค้าไปยังฟอร์ม
            if form.is_valid():
                # เก็บค่าจากฟอร์ม
                updated_product = form.save(commit=False)
                # ทำการบันทึกเฉพาะข้อมูลที่มีการเปลี่ยนแปลง
                updated_product.save()
                return redirect('product_management')  # Redirect หลังบันทึกสำเร็จ
        else:
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('product_management')  # Redirect หลังบันทึกสำเร็จ
    else:
        if product_id:
            product = Product.objects.get(id=product_id)  # ดึงสินค้าจากฐานข้อมูลที่มี id ตรงกับ product_id
            form = ProductForm(instance=product)  # ส่งข้อมูลของสินค้าผ่าน instance
        else:
            form = ProductForm()  # ฟอร์มใหม่สำหรับการเพิ่มสินค้า

    return render(request, 'product_management.html', {'form': form, 'products': products})

# ลบสินค้า
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_management')

def add_stock(request):
    form = StockForm()
    product = None  # เตรียมตัวแปรสำหรับเก็บสินค้า

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            # ค้นหาสินค้าตามรหัสสินค้า
            try:
                product = Product.objects.get(product_code=form.cleaned_data['product_code'])
            except Product.DoesNotExist:
                form.add_error('product_code', 'ไม่พบสินค้าด้วยรหัสนี้')

            # ตรวจสอบว่าปุ่มไหนถูกกด
            action = request.POST.get('action')  # รับค่าจากปุ่ม
            if action == 'add_stock':
                # เพิ่มจำนวนสินค้าที่รับเข้ามา
                product.stock += form.cleaned_data['received_quantity']
                message = 'เพิ่มสต็อกสินค้าเสร็จสิ้น'
            elif action == 'remove_stock':
                # ลดจำนวนสินค้า
                if product.stock >= form.cleaned_data['received_quantity']:
                    product.stock -= form.cleaned_data['received_quantity']
                    message = 'ลดสต็อกสินค้าเสร็จสิ้น'
                else:
                    message = 'สต็อกไม่เพียงพอที่จะลบ'

            product.save()

            # รีเซ็ตฟอร์มหลังจากบันทึกสำเร็จ
            form = StockForm()  # สร้างฟอร์มใหม่เพื่อให้ช่องกรอกกลับมาว่าง

            return render(request, 'add_stock.html', {'form': form, 'product': product, 'message': message})

    # ถ้าไม่ได้ส่งค่า POST จะเป็นการโหลดหน้าแรก (ฟอร์มว่างๆ)
    return render(request, 'add_stock.html', {'form': form, 'product': product})

def move_to_shelf(request):
    form = ShelfForm()
    shelves = Shelf.objects.all()  # ดึงข้อมูลสินค้าบนชั้นวางทั้งหมด
    message = ""  # กำหนดค่าเริ่มต้นให้กับ message

    if request.method == 'POST':
        form = ShelfForm(request.POST)
        if form.is_valid():
            product_code = form.cleaned_data['product_code']
            shelf_quantity = form.cleaned_data['shelf_quantity']

            # ค้นหาสินค้าจากรหัสสินค้า
            product = get_object_or_404(Product, product_code=product_code)

            action = request.POST.get('action')  # ตรวจสอบว่าปุ่มไหนถูกกด

            if action == 'move_to_shelf':  # ถ้ากดปุ่ม "ขึ้นชั้นวาง"
                if product.stock and product.stock >= shelf_quantity:
                    # ลดสต็อกสินค้า
                    product.stock -= shelf_quantity
                    product.save()

                    # ตรวจสอบว่าใน Shelf มีสินค้าชนิดนี้อยู่แล้วหรือไม่
                    shelf_entry = Shelf.objects.filter(product=product).first()

                    if shelf_entry:
                        # ถ้ามีสินค้าชนิดนี้ใน Shelf แล้ว ให้รวม shelf_quantity
                        shelf_entry.shelf_quantity += shelf_quantity
                        shelf_entry.save()
                    else:
                        # ถ้าไม่มีสินค้าใน Shelf ให้สร้างแถวใหม่
                        Shelf.objects.create(product=product, shelf_quantity=shelf_quantity)

                    message = 'ขึ้นชั้นวางสำเร็จ'
                else:
                    form.add_error('shelf_quantity', 'สินค้าในสต็อกไม่เพียงพอ')
                    message = 'สินค้าในสต็อกไม่เพียงพอ'

            elif action == 'move_to_stock':  # ถ้ากดปุ่ม "ย้ายไป Stock"
                try:
                    # หาสินค้าที่มีอยู่ใน Shelf
                    shelf_entry = Shelf.objects.get(product=product)

                    if shelf_entry.shelf_quantity >= shelf_quantity:
                        # เพิ่มจำนวนสินค้าในสต็อก
                        product.stock += shelf_quantity
                        product.save()

                        # ลดจำนวนสินค้าใน Shelf
                        shelf_entry.shelf_quantity -= shelf_quantity
                        shelf_entry.save()

                        # ถ้าจำนวนสินค้าใน Shelf เหลือน้อยกว่า 1 ชิ้น ให้ลบออกจาก Shelf
                        if shelf_entry.shelf_quantity <= 0:
                            shelf_entry.delete()

                        message = "ย้ายไป Stock สำเร็จ"
                    else:
                        message = "จำนวนสินค้าในชั้นวางไม่เพียงพอที่จะย้าย"

                except Shelf.DoesNotExist:
                    message = "ไม่มีสินค้านี้ในชั้นวาง"

    return render(request, 'move_to_shelf.html', {
        'form': ShelfForm(),
        'shelves': Shelf.objects.all(),
        'message': message  # ส่งค่าข้อความที่มีให้กับ template
    })
