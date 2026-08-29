from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, Roles


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        return (
            FilmWork.objects
            .annotate(
                genre_names=ArrayAgg(
                    'genres__name',
                    distinct=True,
                ),
                actors=ArrayAgg(
                    'personfilmwork__person__full_name',
                    filter=Q(personfilmwork__role=Roles.ACTOR),
                    distinct=True,
                ),
                directors=ArrayAgg(
                    'personfilmwork__person__full_name',
                    filter=Q(personfilmwork__role=Roles.DIRECTOR),
                    distinct=True,
                ),
                writers=ArrayAgg(
                    'personfilmwork__person__full_name',
                    filter=Q(personfilmwork__role=Roles.WRITER),
                    distinct=True,
                ),
            )
            .values(
                'id',
                'title',
                'description',
                'creation_date',
                'rating',
                'type',
                'genre_names',
                'actors',
                'directors',
                'writers',
            )
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = FilmWork
    http_method_names = ['get']
    paginate_by = 50


    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by,
        )
        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': [
                {
                    **data,
                    'genres': data.pop('genre_names'),
                }
                for data in queryset
            ],
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    pk_url_kwarg='id'

    def get_context_data(self, **kwargs):
        return {
            **self.object,
            'genres': self.object.pop('genre_names'),
        }
