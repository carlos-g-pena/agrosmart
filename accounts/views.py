from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm,ProductForm
from .models import Product
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'accounts/home.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.registered_by = request.user  
            product.save()
            return redirect('home')  
    else:
        form = ProductForm()
    return render(request, 'accounts/add_product.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()  # Obtén todos los productos registrados
    return render(request, 'accounts/product_list.html', {'products': products})

def generate_pdf(request):
     # Crear la respuesta HTTP con contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="product_report.pdf"'

    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Título
    title = "Product Report"
    content = []

    # Agregar título
    
    styles = getSampleStyleSheet()
    content.append(Paragraph(f"<b>{title}</b>", styles['Title']))

    # Obtener los productos
    products = Product.objects.all()

    # Crear datos para la tabla
    table_data = [
        ["ID", "Product Name", "Weight (kg)", "Date Added", "Registered By"]
    ]  # Encabezados
    for product in products:
        table_data.append([
            product.id,
            product.name,
            product.weight,
            product.date_added.strftime("%Y-%m-%d %H:%M"),
            product.registered_by.username,
        ])

    # Estilo para la tabla
    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    # Agregar tabla al contenido
    content.append(table)

    # Generar el PDF
    doc.build(content)

    return response
