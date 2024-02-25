from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Product
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from . import models
from django.db.models import F, Sum


class list_product(ListView):
    model = Product
    template_name = 'core/list_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.all()
        return context


def _empty_cart():
    return {'items': [], 'count': 0}


def _add_item_to_cart(cart, item_dict):
    found_item = None
    for item in cart['items']:
        if item['id'] == item_dict['id']:
            found_item = item
            break
    if found_item:
        found_item['count'] += item_dict['count']
        found_item['name'] = item_dict['name']
        found_item['price'] = item_dict['price']
        found_item['total_price'] = found_item['price']*found_item['count']
    else:
        item_dict['total_price'] = item_dict['price'] * item_dict['count']
        cart['items'].append(item_dict)
    _total_price(cart)

def _total_price(cart):
    for item in cart['items']:
        total = + (item['count']*item['price'])
        cart['total'] = total
        return total


class CartView(View):

    action = None

    def get(self, request, id=None):

        cart = request.session.get('cart', _empty_cart())
        if self.action == 'add':
            obj = get_object_or_404(Product, pk=id)
            item = {'id': id, 'count': 1, 'name': obj.name,
                    'price': obj.price}
            _add_item_to_cart(cart, item)
        elif self.action is None:
            return render(request, 'core/cart_show.html', {'cart': cart})
        else:
            return HttpResponseBadRequest()
        request.session['cart'] = cart
        return HttpResponseRedirect(reverse('store:list_products'))


class CheckoutView(View):
    def get(self, request):
        cart = request.session.get('cart', _empty_cart())
        if not cart:
            return HttpResponseRedirect(reverse('store:list_products'))
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        order = models.Order(user=request.user)
        order.user = request.user
        order.save()
        for item in cart['items']:
            product = models.Product.objects.get(pk=item['id'])
            total_price = product.price * item['count']
            order_item = models.OrderItem(order=order, product=product,
                                          Qty =item['count'], total_price=total_price)
            order_item.save()

        return render(request, 'core/list_product.html', {'order': order,
                                                      'order_item': order_item})

class Up_to_3milView(View):
    def get(self, request):
        total = models.Order.objects.annotate(t_price=Sum(F('items__Qty') * F('items__product__price'))).filter(t_price__gte=3000000)
        return render(request, 'core/3mil.html', {'total': total})

class GetuserView(View):
    def get(self, request, user):
        price =  models.OrderItem.objects.filter(order__user=request.user).values_list('total_price', flat=True)
        count = models.OrderItem.objects.filter(order__user=request.user).values_list('Qty', flat=True)
        product = models.OrderItem.objects.filter(order__user=request.user).values_list('product__name', flat=True)
        return render(request, 'core/get_user.html', {'price': price, 'count': count,'product': product})
