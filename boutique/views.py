from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import BoutiqueForm, ProductForm, UserForm
from .models import Boutique, Product

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_boutique(request):
    if not request.user.is_authenticated():
        return render(request, 'boutique/login.html')
    else:
        form = BoutiqueForm(request.POST or None)
        if form.is_valid():
            boutique= form.save(commit=False)
            boutique.user = request.user
            context = {
                    'boutique': boutique,
                    'form': form,
                }

          
            boutique.save()
            return render(request, 'boutique/detail.html', {'boutique': boutique})
        context = {
            "form": form,
        }
        return render(request, 'boutique/create_boutique.html', context)


def create_product(request, boutique_id):
    form = ProductForm(request.POST or None, request.FILES or None)
    boutique = get_object_or_404(Boutique, pk=boutique_id)
    if form.is_valid():
        boutique_products = boutique.product_set.all()
        for s in boutique_products:
            if s.product_name == form.cleaned_data.get("product_name"):
                context = {
                    'boutique': boutique,
                    'form': form,
                    'error_message': 'Vous avez ajouté ce produit',
                }
                return render(request, 'boutique/create_product.html', context)
        product = form.save(commit=False)
        product.boutique = boutique
        product.product_img = request.FILES['product_img']
        file_type = product.product_img.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'boutique': boutique,
                'form': form,
                'error_message': 'Le format est incompatible Choisissez une image',
            }
            return render(request, 'boutique/create_product.html', context)

        product.save()
        return render(request, 'boutique/detail.html', {'boutique': boutique})
    context = {
        'boutique': boutique,
        'form': form,
    }
    return render(request, 'boutique/create_product.html', context)






def detail(request, boutique_id):
    if not request.user.is_authenticated():
        return render(request, 'boutique/login.html')
    else:
        user = request.user
        boutique= get_object_or_404(Boutique, pk=boutique_id)
        return render(request, 'boutique/detail.html', {'boutique': boutique, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'boutique/login.html')
    else:
     boutiques = Boutique.objects.filter(user=request.user)
     return render(request, 'boutique/index.html', {'boutiques': boutiques})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'boutique/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                boutiques = Boutique.objects.filter(user=request.user)
                return render(request, 'boutique/index.html', {'boutiques': boutiques})
            else:
                return render(request, 'boutique/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'boutique/login.html', {'error_message': 'Invalid login'})
    return render(request, 'boutique/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                boutiques =Boutique.objects.filter(user=request.user)
                return render(request, 'boutique/index.html', {'boutiques': boutiques})
    context = {
        "form": form,
    }
    return render(request, 'boutique/register.html', context)


def products(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'boutique/login.html')
    else:
        try:
            product_ids = []
            for boutique in Boutique.objects.filter(user=request.user):
                for product in boutique.product_set.all():
                    product_ids.append(product.pk)
            users_products= Product.objects.filter(pk__in=product_ids)
          
        except Boutique.DoesNotExist:
            users_products = []
        return render(request, 'boutique/products.html', {
            'product_list': users_products,
            'filter_by': filter_by,
        })
