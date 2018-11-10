from django.http import HttpResponse
from django.template import loader
from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import socket


from .models import Product

def index(request):
    productlist = Product.objects.all()
    template = loader.get_template('page/index.html')
    context = {
        'productlist': productlist,
    }
    return HttpResponse(template.render(context, request))

def products(request):
    if request.method == 'GET':
       products = list(Product.objects.values())
       return JsonResponse(dict(products=products))

@csrf_exempt
def product(request, id):
    if request.method == 'DELETE':
       Product.objects.get(pk=id).delete()
       return JsonResponse({'response' : 'Item was deleted'})

    if request.method == 'PUT':
       product = QueryDict(request.body)
       productprice= product.get("newPrice")
       productid = product.get("product")
       myProduct = Product.objects.get(id=productid)
       myProduct.price = productprice
       myProduct.save()
       return JsonResponse({'id': productid,'price':productprice})


@csrf_exempt
def addProduct(request):
    if request.method == 'POST':
       product = QueryDict(request.body)
       productprice= product.get("price")
       productname = product.get("name")
       productDescription = product.get("description")
       newProduct = Product(name=productname,description=productDescription,price=productprice)
       #newProduct.id()
       newProduct.save()
       return JsonResponse({'id': newProduct.id,'price':productprice,'name':productname,'description':productDescription})


def main(request):
   return render_to_response('page/index.html', context_instance=RequestContext(request))
