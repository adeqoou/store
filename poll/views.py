from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    TemplateView,
    View,
    ListView,
    DeleteView)
from django.urls import reverse_lazy
from .models import *
from users.models import Contact
from .forms import ContactForm
from django.core.mail import send_mail
from .tasks import email_send


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
        context['form'] = ContactForm()
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

    def get(self, request, category_id=None):
        product = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
        context = {
            'products': product
        }
        return render(request, self.template_name, context)


class OrderAddView(CreateView):
    model = Orders

    def post(self, request, *args, **kwargs):
        basket_id = kwargs.get('basket_id')
        user = request.user
        basket = get_object_or_404(Basket, id=basket_id, user=user)

        order = Orders.objects.create(user=user, basket_id=basket_id)
        basket.order = order
        basket.save()

        return redirect('orders')


class OrderListView(ListView):
    model = Orders
    template_name = 'poll/order_add.html'

    def get(self, request):
        baskets = Basket.objects.filter(user=request.user)
        orders = Orders.objects.filter(user=request.user)
        total_sum = sum(basket.product.price * basket.quantity for basket in baskets)

        context = {
            'orders': orders,
            'total_sum': total_sum
        }
        return render(request, self.template_name, context)


class OrderRemoveView(DeleteView):
    model = Orders
    success_url = reverse_lazy('orders')

    def get(self, request, **kwargs):
        order = self.kwargs.get('order')
        order.delete()
        return self.success_url


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    template_name = 'poll/email_send.html'

    def form_valid(self, form):
        user_email = form.cleaned_data.get('email')
        email_send.delay(user_email)

        send_mail(
            'Интернет-магазин',
            f'Почта/ Посетите наш сайт: http://127.0.0.1:8000/',
            'aidarbekovadahan8@gmail.com',
            [user_email],
            fail_silently=False
        )
        form.save()
        return super().form_valid(form)

