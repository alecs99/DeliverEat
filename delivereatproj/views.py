from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView

from delivereatproj.models import UserProfile, User, Restaurant, Product, Cart, Order, Feedback
from delivereatproj.forms import UserProfileForm, CheckoutForm, FeedBackForm

from datetime import datetime


def index(request):
    restaurants_list = Restaurant.objects.all()
    return render(request, 'index.html', {'restaurants_list': restaurants_list})


class CartDetail(LoginRequiredMixin, DetailView):
    template_name = 'view_cart.html'
    model = Cart

    def get_context_data(self, **kwargs):
        context = super(CartDetail, self).get_context_data(**kwargs)
        return context


class ProductAddView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        cart = Cart.objects.get(pk=self.request.user.id)
        product = Product.objects.get(pk=self.kwargs['pk_product'])
        if cart.products.count() is not 0:
            for cart_product in cart.products.all():
                if product.restaurant.id is not cart_product.restaurant.id:
                    return redirect(reverse_lazy("cart_detail", kwargs={"pk": self.request.user.id}))
        cart.total_price = cart.total_price + product.price
        cart.products.add(product)
        cart.save()
        return redirect(reverse_lazy("cart_detail", kwargs={"pk": self.request.user.id}))


class ProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        cart = Cart.objects.get(pk=self.request.user.id)
        product = Product.objects.get(pk=self.kwargs['pk_product'])
        cart.total_price = cart.total_price - product.price
        cart.products.remove(product)
        cart.save()
        return redirect(reverse_lazy("cart_detail", kwargs={"pk": self.request.user.id}))


class RestaurantDetail(LoginRequiredMixin, DetailView):
    template_name = 'restaurant_detail.html'
    model = Restaurant

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        current_restaurant = context['restaurant']
        context['products'] = Product.objects.filter(restaurant=current_restaurant)
        context['cart'] = Cart.objects.get(pk=self.request.user.id)
        feedback_list = Feedback.objects.filter(restaurant=current_restaurant)
        context['feedback_list'] = feedback_list

        context['rating'] = 0
        if len(feedback_list):
            rating = 0
            for feedback in feedback_list:
                rating += feedback.stars
            context['rating'] = rating / len(feedback_list)

        return context


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'user_profile.html'
    context_object_name = 'selected_user'

    def get_object(self, **kwargs):
        selected_user = User.objects.get(id=self.request.user.id)
        return selected_user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile_update.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        user = self.object.user
        context['form'].fields['first_name'].initial = user.first_name
        context['form'].fields['last_name'].initial = user.last_name
        context['form'].fields['e_mail'].initial = user.email
        context['form'].fields['phone_number'].initial = user.profile.phone_number
        context['form'].fields['birthday'].initial = user.profile.birthday
        context['form'].fields['address'].initial = user.profile.address
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        self.object.birthday = data['birthday']
        self.object.phone_number = data['phone_number']
        self.object.address = data['address']
        self.request.user.first_name = data['first_name']
        self.request.user.last_name = data['last_name']
        self.request.user.email = data['e_mail']
        self.object.save()
        self.request.user.save()

        if Cart.objects.filter(id=self.request.user.id).count() is 0:
            cart = Cart.objects.create(id=self.request.user.id, customer=self.request.user)


        return redirect(reverse_lazy("user_profile"))


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'])
        UserProfile.objects.create(user=user)
        login(self.request, user)
        return redirect(index)


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self):
        form = AuthenticationForm()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            login(request, user)
            return redirect(reverse_lazy(index))
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy(index))


class OrderView(LoginRequiredMixin, DetailView):
    template_name = "order.html"
    model = Order

    def get_context_data(self, **kwargs):
        return super(OrderView, self).get_context_data(**kwargs)


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = CheckoutForm
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        user = self.request.user
        context['form'].fields['first_name'].initial = user.first_name
        context['form'].fields['last_name'].initial = user.last_name
        context['form'].fields['e_mail'].initial = user.email
        context['form'].fields['phone_number'].initial = user.profile.phone_number
        context['form'].fields['address'].initial = user.profile.address

        return context

    def form_valid(self, form):
        data = form.cleaned_data
        cart = Cart.objects.get(pk=self.request.user.id)

        order = Order.objects.create(restaurant=cart.products.all()[0].restaurant, customer=self.request.user,
                                     order_date=datetime.today(), total_price=cart.total_price)
        order.customer.phone_number = data['phone_number']
        order.customer.address = data['address']
        order.customer.first_name = data['first_name']
        order.customer.last_name = data['last_name']
        order.customer.email = data['e_mail']
        order.payment_method = data['payment_method']
        order.products.add(*cart.products.all())

        order.save()
        cart.products.clear()
        cart.total_price = 0
        cart.save()

        return redirect(reverse_lazy("order", kwargs={"pk": order.id}))


class OrdersListView(LoginRequiredMixin, ListView):
    template_name = "orders.html"
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrdersListView, self).get_context_data(**kwargs)
        orders = Order.objects.all().filter(customer=UserProfile.objects.get(id=self.request.user.id))
        feedback_list = Feedback.objects.all().filter(customer=User.objects.get(id=self.request.user.id))
        context['orders'] = orders
        orders_with_feedback = []
        [orders_with_feedback.append(feedback.order.id) for feedback in feedback_list]
        context['orders_with_feedback'] = orders_with_feedback

        return context


class FeedbackView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'feedback_form.html'
    model = Feedback
    form_class = FeedBackForm

    def get_context_data(self, **kwargs):
        context = super(FeedbackView, self).get_context_data(**kwargs)
        context['order'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        order = Order.objects.get(id=data['order'])

        feedback = Feedback.objects.create(restaurant=order.restaurant, customer=order.customer.user,
                                           stars=data['stars'], details=data['details'], order=order)
        feedback.save()

        return redirect(reverse_lazy('restaurant_detail', kwargs={'pk': order.restaurant.id}))


class FeedbackDetailsView(LoginRequiredMixin, DetailView):
    template_name = "view_feedback.html"
    context_object_name = 'selected_feedback'

    def get_object(self, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk_order'])
        selected_feedback = Feedback.objects.get(order=order)

        return selected_feedback
