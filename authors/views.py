from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegisterForm


# Create your views here.
def register_view(request):
    # Understanding the session number
    # request.session['number'] = request.session.get('number') or 1
    # request.session['number'] += 1

    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    # if the form is valid then save this form
    if form.is_valid():
        # salve just in the variable called user
        user = form.save(commit=False)
        user.set_password(user.password)  # treating the user password
        form.save()  # now, it salves in the database
        messages.success(request, 'Your user is created, please log in.')

        del (request.session['register_form_data'])

    return redirect('authors:register')
