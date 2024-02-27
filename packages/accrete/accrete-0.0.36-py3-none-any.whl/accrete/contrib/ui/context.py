import logging
from typing import TypedDict
from dataclasses import dataclass, field
from django.utils.translation import gettext_lazy as _
from django.shortcuts import resolve_url
from django.db.models import Model, QuerySet
from django.core.paginator import Paginator
from django.core import paginator
from django.forms import Form, ModelForm
from .elements import ClientAction, BreadCrumb, TableField
from .filter import Filter

_logger = logging.getLogger(__name__)

DEFAULT_PAGINATE_BY = 40


class DetailPagination(TypedDict):
    previous_object_url: str
    next_object_url: str
    current_object_idx: int
    total_objects: int


class TableContext(TypedDict, total=False):

    title: str
    object_label: str
    object_param_str: str
    fields: list[TableField]
    breadcrumbs: list[BreadCrumb]
    actions: list[ClientAction]
    list_page: paginator.Page
    pagination_param_str: str
    endless_scroll: bool
    filter: Filter


class ListContext(TypedDict):

    title: str
    object_label: str
    object_param_str: str
    breadcrumbs: list[BreadCrumb]
    actions: list[ClientAction]
    list_page: paginator.Page
    pagination_param_str: str
    endless_scroll: bool
    filter: Filter


class DetailContext(TypedDict, total=False):

    title: str
    object: Model
    breadcrumbs: list[BreadCrumb]
    detail_page: DetailPagination
    pagination_param_str: str
    actions: list[ClientAction]


class FormContext(TypedDict):

    title: str
    breadcrumbs: list[BreadCrumb]
    form: Form | ModelForm
    form_id: str
    actions: list[ClientAction]


# @dataclass
# class ListContext:
#
#     title: str
#     actions: list[ClientAction] = field(default_factory=list)
#     object_label: str = ''
#     fields: list[TableField] = field(default_factory=list)
#     page: paginator.Page = None
#     list_pagination: bool = True
#     endless_scroll: bool = True
#     params: dict = field(default_factory=dict)
#     filter: Filter = None
#
#     def dict(self):
#         return {
#             "title": self.title,
#             "actions": self.actions,
#             "object_label": self.object_label,
#             "fields": self.fields,
#             "page": self.page,
#             "list_pagination": self.list_pagination,
#             "endless_scroll": self.endless_scroll,
#             "params": self.params,
#             "filter": self.filter
#         }


class GenericContent:

    def __init__(self, *args, **kwargs):
        self.page: Page | None = None

    def dict(self):
        return {}


class ListContent:

    def __init__(
            self, queryset: QuerySet, paginate_by: int = DEFAULT_PAGINATE_BY,
            page_number: int = 1, filter_obj: Filter = None,
            endless_scroll: bool = True, fields: list[TableField] = None,
            object_label: str = None, object_url_params: dict = None
    ):
        self.queryset = queryset
        self.paginate_by = paginate_by or DEFAULT_PAGINATE_BY
        self.page_number = page_number
        self.filter = filter_obj
        self.endless_scroll = endless_scroll
        self.fields = fields or []
        self.object_label = object_label or _('Name')
        self.object_url_params = object_url_params or {}
        self.page: Page | None = None

    def get_page_number(self, paginator):
        if self.page_number < 1:
            return 1
        if self.page_number > paginator.num_pages:
            return paginator.num_pages
        return self.page_number

    def dict(self):
        paginator = Paginator(self.queryset, self.paginate_by)
        page = paginator.page(self.get_page_number(paginator))
        context = {
            'page': page,
            'object_label': self.object_label,
            'object_url_params': url_param_str(prepare_url_params(self.object_url_params)),
            'fields': self.fields,
            'list_pagination': True if self.paginate_by > 0 else False,
            'filter': self.filter,
            'endless_scroll': self.endless_scroll
        }
        return context


class DetailContent:

    def __init__(
            self, obj: Model | type[Model], queryset: QuerySet = None,
    ):
        self.obj = obj
        self.queryset = queryset
        self.page: Page | None = None

    def get_detail_pagination(self):
        return detail_pagination(self.queryset, self.obj)

    def dict(self):
        ctx = {
            'object': self.obj,
            'detail_pagination': False,
        }
        if self.queryset:
            ctx.update(self.get_detail_pagination())
        return ctx


class FormContent:

    def __init__(
            self, model: Model | type[Model], form: Form | ModelForm,
            form_id: str = 'form', add_default_actions: bool = True,
            discard_url: str = None
    ):
        self.model = model
        self.form = form
        self.form_id = form_id
        self.add_default_actions = add_default_actions
        self.discard_url = discard_url
        self.page: Page | None = None

    def add_default_form_actions(self):
        actions = [
            ClientAction(
                name=_('Save'),
                submit=True,
                class_list=['is-success'],
                form_id=self.form_id
            )
        ]
        try:
            url = self.discard_url or (self.model.pk and self.model.get_absolute_url())
        except TypeError:
            raise TypeError(
                'Supply the discard_url parameter if Form is called '
                'with a model class instead of an instance.'
            )
        except AttributeError as e:
            _logger.error(
                'Supply the discard_url parameter if Form is '
                'called with a model instance that has the get_absolute_url '
                'method not defined.'
            )
            raise e

        actions.append(
            ClientAction(
                name=_('Discard'),
                url=url,
            )
        )
        if self.page:
            self.page.actions = actions.extend(self.page.actions)

    def get_title(self):
        try:
            int(self.model.pk)
            return _('Edit')
        except TypeError:
            return _('Add')
        except Exception as e:
            _logger.exception(e)
            return ''

    def dict(self):
        ctx = {
            'form': self.form,
            'form_id': self.form_id,
        }
        if self.add_default_actions:
            self.add_default_form_actions()
        if self.page and not self.page.title:
            self.page.title = self.get_title()
        return ctx


class Page:

    def __init__(
            self, *, title: str = None,
            content: GenericContent | ListContent | DetailContent | FormContent = None,
            breadcrumbs: list[BreadCrumb] = None, get_params: dict = None,
            actions: list[ClientAction] = None,
    ):
        self.title = title or ''
        self.content = content
        self.breadcrumbs = breadcrumbs or []
        self.actions = actions or []
        self.get_params = get_params or {}
        if self.content:
            self.content.page = self

    def dict(self):
        url_params = prepare_url_params(self.get_params)
        ctx = {
            'title': self.title,
            'breadcrumbs': self.breadcrumbs,
            'actions': self.actions,
            'url_params': url_params,
            'url_params_str': url_param_str(url_params)
        }
        if self.content:
            ctx.update(self.content.dict())
        return ctx


def cast_param(params: dict, param: str, cast_to: callable, default):
    try:
        return cast_to(params.get(param, default))
    except Exception as e:
        _logger.exception(e)
        return default


def prepare_url_params(get_params: dict) -> dict:
    return {key: f'&{key}={value}' for key, value in get_params.items()}


def url_param_str(params: dict, extract: list[str] = None) -> str:
    """
    Return a URL Querystring from the given parameters
    If extract is supplied, extract the value from the dictionary and prepare
    them, so that each value is formatted eg. {'page': '&page=1'}
    """
    if extract:
        params = prepare_url_params(extract_url_params(params, extract))
    param_str = (
        "".join(str(value) for value in params.values())
        .replace('&&', '&')
        .replace('?&', '?')
        .strip('?&')
    )
    return f'?{param_str}'


def extract_url_params(params: dict, keys: list[str]) -> dict:
    return {key: params[key] for key in keys if key in params}


def exclude_params(params: dict, keys: list[str]) -> dict:
    return {key: val for key, val in params.items() if key not in keys}


def get_list_page(queryset: QuerySet, paginate_by: int, page_number: int) -> paginator.Page:
    pages = Paginator(queryset, per_page=paginate_by)
    return pages.page(page_number <= pages.num_pages and page_number or pages.num_pages)


def get_detail_page(queryset: QuerySet, obj: Model) -> dict:
    if not hasattr(obj, 'get_absolute_url'):
        _logger.warning(
            'Detail pagination disabled for models without the '
            'get_absolute_url attribute. Set paginate_by to 0 to '
            'deactivate pagination.'
        )
        return {}
    idx = (*queryset,).index(obj)
    previous_object_url = (
        queryset[idx - 1] if idx - 1 >= 0 else queryset.last()
    ).get_absolute_url()
    next_object_url = (
        queryset[idx + 1] if idx + 1 <= queryset.count() - 1 else queryset.first()
    ).get_absolute_url()
    return {
        'previous_object_url': previous_object_url,
        'next_object_url': next_object_url,
        'current_object_idx': idx + 1,
        'total_objects': queryset.count()
    }


def default_form_actions(discard_url: str, form_id: str = 'form') -> list[ClientAction]:
    return [
        ClientAction(
            name=_('Save'),
            submit=True,
            class_list=['is-success'],
            form_id=form_id,
        ),
        ClientAction(
            name=_('Discard'),
            url=discard_url
        )
    ]
