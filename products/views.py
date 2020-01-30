from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect

from products.models import Product


# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/home.html', context)


@login_required(login_url='singup')
def create(request):
    error = 'Have Some Error '
    context = {
        'error': error
    }
    if request.method == "POST":
        if request.POST['title'] and request.POST['body'] and request.POST['urls'] and request.FILES['image'] and \
                request.FILES['icon']:
            # create Product Objects
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['urls'].startswith('http://') or request.POST['urls'].startswith('https://'):

                product.url = request.POST['urls']
            else:
                product.url = 'http://' + request.POST['urls']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']

            product.pub_date = timezone.datetime.now()

            product.hunter = request.user
            product.save()
            return redirect("home")
        else:

            return render(request, 'products/create.html', context)
    else:
        return render(request, 'products/create.html')


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/detail.html', context)


@login_required()
def upvote(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()

        return redirect('/' + str(product.id))
