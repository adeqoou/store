from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    View,
    ListView,
    DeleteView)
from django.urls import reverse_lazy
from .models import *


class IndexView(TemplateView):
    template_name = 'poll/index.html'


class ProductView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'poll/products.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


class BasketAddView(LoginRequiredMixin, View):
    model = Basket
    login_url = 'login_pg'

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        baskets = Basket.objects.filter(user=request.user, product=product)

        if not baskets.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
        return redirect('basket')


class BasketListView(ListView):
    model = Basket
    template_name = 'poll/basket.html'

    def get(self, request, **kwargs):
        baskets = Basket.objects.filter(user=request.user)
        total_sum = sum(basket.product.price * basket.quantity for basket in baskets)

        context = {
            'baskets': baskets,
            'total_sum': total_sum
        }
        return render(request, self.template_name, context)


class RemoveBasketView(DeleteView):
    def get(self, request, basket_id):
        basket = Basket.objects.get(id=basket_id)
        basket.delete()
        return redirect('basket')


class ProductListView(ListView):
    model = Product
    template_name = 'poll/product_list.html'

    def get(self, request, category_id=None, *args, **kwargs):
        product = Product.objects.filter(product_id=category_id) if category_id else Product.objects.all()
        context = {
            'products': product
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




