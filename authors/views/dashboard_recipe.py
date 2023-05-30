from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe


class DashboardRecipe(View):
    def get(self, request, id):
        # print('Estou aqui na CBV!!!')
        recipe = Recipe.objects.filter(
            is_published=False,
            author=request.user,
            pk=id
        ).first()

        if not recipe:
            raise Http404()

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
                                    args=(id,)))

        return render(request, 'authors/pages/dashboard_recipe.html', context={
            'recipe': recipe,
            'form': form
        })
