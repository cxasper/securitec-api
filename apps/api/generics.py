from django.db.models.query import QuerySet
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class CustomAPIView(APIView):
    """
    Base class for all CRUD with parent, searching and pagination.
    """

    # You'll need to either set these attributes,
    # `model` represents the instance model in which it will work (it is required).
    model = None
    # `serializer_class` represents the serializer use for this view
    # (it is required, except in DELETE & POST).
    serializer_class = None
    # `parent_model` use this attribute when define deep urls,
    # e.g r'clients/(?P<client>\d+)/documents', in this case Client is
    # `parent_model`
    parent_model = None
    # `parent_model` is name for FK, e.g r'clients/(?P<client>\d+)/documents',
    # in this case 'client' is parent_field.
    parent_field = None
    parent = None
    filter_parent = None
    # If you want to use object lookups other than pk, set 'lookup_field'.
    # For more complex lookup requirements override `get_object()`.
    lookup_field = 'pk'
    lookup_url_kwarg = None
    # `search_class` The searching backend classes to use for queryset filtering
    search_class = None
    # The style to use for queryset pagination.
    pagination_class = None


    def set_parent(self):
        self.parent_field = next(iter(self.kwargs))
        parent_args = {
            'pk': self.kwargs.get(self.parent_field),
        }
        self.parent = get_object_or_404(self.parent_model, **parent_args)


    def get_queryset(self):
        assert self.model is not None, (
            "'%s' should either include a `model` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        if self.parent_model:
            self.set_parent()
            filter_args = {
                self.filter_parent or self.parent_field: self.parent
            }
            queryset = self.model.objects.filter(
                **filter_args
            )
        else:
            queryset = self.model.objects.all()

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_object(self):
        queryset = self.get_queryset()

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        instance = get_object_or_404(queryset, **filter_kwargs)

        return instance

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {'request': self.request}
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.serializer_class

    def search_queryset(self, queryset):
        if self.search_class:
            return self.search_class().filter_queryset(self.request, queryset, self)
        return queryset


class ListAPIView(CustomAPIView):
    """
    List a queryset with paginated and searching.
    """

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        return self.paginator.get_paginated_response(data)

    def get(self, request, *args, **kwargs):
        queryset = self.search_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator


class CreateAPIView(CustomAPIView):
    """
    Create a model instance.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveAPIView(CustomAPIView):
    """
    Get a model instance.
    """
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DestroyAPIView(CustomAPIView):
    """
    Delete a model instance.
    """
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateAPIView(CustomAPIView):
    """
    Partial update or update (PATCH or PUT) a model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
