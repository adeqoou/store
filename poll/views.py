from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    View,
    ListView)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import *
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'poll/index.html'


class ProductView(TemplateView):
    template_name = 'poll/products.html'

    def get(self, request, *args, **kwargs):
        context = {
            'products': Product.objects.all(),
            'categories': ProductCategory.objects.all(),
        }
        return render(request, self.template_name, context)


class BasketView(LoginRequiredMixin, View):
    template_name = 'poll/profile.html'
    login_url = 'login_pg'

    def get(self, request, product_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        baskets = Basket.objects.filter(user=request.user, product_id=product_id)
        total_price = sum([basket.product.price * basket.quantity for basket in baskets])

        context = {
            'baskets': baskets,
            'total_price': total_price,
            'product': product,
        }
        return render(request, self.template_name, context)

    def post(self, request, product_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        baskets = Basket.objects.filter(user=request.user, product=product)

        if not baskets.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
        return redirect('index')


class RemoveBasketView(View):
        def get(self, request, basket_id):
            basket = Basket.objects.get(id=basket_id)
            basket.delete()
            message = messages.success(self.request, 'Product deleted')
            return message


class ProductListAndPaginateView(ListView):
    model = Product
    template_name = 'poll/product_list.html'
    paginate_by = 4
    context_object_name = 'products'

    def get(self, request, category_id=None, *args, **kwargs):
        products = Product.objects.filter(product_id=category_id) if category_id else Product.objects.all()
        context = {
            'product': products
        }
        return render(request, self.template_name, context)


    # def post(self, request, *args, **kwargs):
    #     product_id = request.POST.get('product_id')

    #     quantity = int(request.POST.get('quantity', 1))
    #     product = Product.objects.get(id=product_id)
    #
    #     basket, created = Basket.objects.get_or_create(user=request.user, product=product)
    #     basket.quantity += quantity
    #     basket.save()
    #     return redirect('basket')



