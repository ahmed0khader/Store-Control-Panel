from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.
@login_required(login_url='login')
# @admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    # 
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {
        'title': 'Home',
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request ,'accounts/dashboard.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def products(request):
    context = {
        'title': 'Products',
    }
    return render(request ,'accounts/products.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    # filter
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {
        'title': 'Customer',
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter,
    }
    return render(request ,'accounts/customer.html', context)

# order
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status', 'note'), extra=3)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

# order Update
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    orderform = OrderForm(instance=order)
    if request.method == 'POST':
        orderform = OrderForm(request.POST, instance=order)
        if orderform.is_valid():
            orderform.save()
            return redirect('/')
    context = {
        'title': 'Update Order',
        'form': orderform,

    }
    return render(request ,'accounts/order_form.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'title': 'Delete Order',
        'order': order,
    }   
    return render(request ,'accounts/delete.html', context)



# creae Customer
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def create_customer(request):
    ordercustomer = CustomerForm()
    if request.method == 'POST':
        ordercustomer = CustomerForm(request.POST)
        if ordercustomer.is_valid():
            ordercustomer.save()
            return redirect('/')
    context = {
            'title': 'Create Customer',
            'ordercustomer': ordercustomer,
        }
    return render(request ,'accounts/create_customer.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    ordercustomer = CustomerForm(instance=customer)
    if request.method == 'POST':
        ordercustomer = CustomerForm(request.POST, instance=customer)
        if ordercustomer.is_valid():
            ordercustomer.save()
            return redirect('/')
        
    context = {
        'title': 'Update Customer',
        'ordercustomer': ordercustomer,
    }
    return render(request ,'accounts/create_customer.html', context)


# @allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/user.html', context)

#profile
@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
    
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)


# user********************
@unauthenticated_user
def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
            messages.success(request, f'Account was created for {username}')
    else:
        form = RegisterForm()

    context = {
        'title': 'Register',
        'form': form,

    }
    return render(request, 'accounts/register.html', context)


from django.contrib.auth import authenticate, login, logout

@unauthenticated_user
def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:   
            messages.success(request, 'username or password is incorrect ')
            
    context = {
        'title': 'Login',
    }
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')