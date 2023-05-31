from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None
        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', context={
            'form': form
        })

    def get(self, request, id=None):
        print('Entro CBV new!!!')
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,  # for files of images
            instance=recipe
        )

        if form.is_valid():
            # form is valid
            # it grants that the form is salved in recipes
            # but doesn´t send to database
            # that is done to conclude the form with values valid
            # and it performes the
            # validation
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            # now, the form is salved in the database
            recipe.save()
            messages.success(
                request, 'Your recipe has been successfully saved!')
            return redirect(reverse('authors:dashboard_recipe_edit',
                                    args=(recipe.id,)))

        return self.render_recipe(form)
