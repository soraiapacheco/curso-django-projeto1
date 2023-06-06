# from utils.recipes.factory import make_recipe
import os

from django.db.models import F, Q  # para consultas que use Or
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))  # Qty of recipes by page

# print(PER_PAGE, type(PER_PAGE))


def theory(request, *args, **kwargs):
    recipes = Recipe.objects \
        .filter(id=F('author__id')
                ).order_by('id', '-title')  # ordenando crescente
    #    .order_by('-id') # ordenando decrescente
    #    .first()
    # .last()

    # print(recipes[1])
    # print(recipes[2:3])
    # recipes = recipes.filter(title__icontains='Teste')

    # if you transform the queryset in list, the Django take all recipes
    # list(recipes)
    context = {'recipes': recipes}

    return render(request,
                  'recipes/pages/theory.html',
                  context=context)


class RecipeListViewBase(ListView):

    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )

        # you can use prefetch_related when you have a relation of many to many
        # qs = qs.prefetch_related('author', 'category')
        # In this our case, we keep the select_related because our relation is of one to many
        qs = qs.select_related('author', 'category')

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )

        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )

        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']

        recipes_list = recipes.object_list.values()

        # one way to debug using the print command
        # print(recipes.object_list)

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update(
            {
                'title': f'{ctx.get("recipes")[0].category.name} - Category |',

            }
        )

        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update(
            {
                'page_title': f'Search for "{search_term}" |',
                'search_term': search_term,
                'additional_url_query': f'&q={search_term}',
            }
        )

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        if not qs:
            raise Http404()

        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
