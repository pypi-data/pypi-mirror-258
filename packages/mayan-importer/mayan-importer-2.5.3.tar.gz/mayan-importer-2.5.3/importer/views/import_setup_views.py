import logging

from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    FormView, SingleObjectDeleteView, SingleObjectDynamicFormCreateView,
    SingleObjectDynamicFormEditView, SingleObjectListView
)
from mayan.apps.views.view_mixins import ExternalObjectViewMixin

from ..classes import ImportSetupBackend
from ..forms import (
    ImportSetupBackendSelectionForm, ImportSetupBackendDynamicForm
)
from ..icons import (
    icon_import_setup_backend_selection, icon_import_setup_delete,
    icon_import_setup_edit, icon_import_setup_list,
    icon_import_setup_log_list
)
from ..links import link_import_setup_backend_selection
from ..models import ImportSetup
from ..permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_view
)

logger = logging.getLogger(name=__name__)


class ImportSetupBackendSelectionView(FormView):
    extra_context = {
        'title': _('New import backend selection')
    }
    form_class = ImportSetupBackendSelectionForm
    view_icon = icon_import_setup_backend_selection
    view_permission = permission_import_setup_create

    def form_valid(self, form):
        backend_class = form.cleaned_data['backend']
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='importer:import_setup_create', kwargs={
                    'class_path': backend_class
                }
            )
        )


class ImportSetupCreateView(SingleObjectDynamicFormCreateView):
    form_class = ImportSetupBackendDynamicForm
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )
    view_icon = icon_import_setup_backend_selection
    view_permission = permission_import_setup_create

    def get_backend(self):
        try:
            return ImportSetupBackend.get(
                name=self.kwargs['class_path']
            )
        except KeyError:
            raise Http404(
                '{} class not found'.format(
                    self.kwargs['class_path']
                )
            )

    def get_extra_context(self):
        backend_class = self.get_backend_class()
        return {
            'title': _(
                'Create a "%s" import setup'
            ) % backend_class.label
        }

    def get_form_schema(self):
        backend_class = self.get_backend_class()
        result = {
            'fields': backend_class.fields,
            'widgets': getattr(
                backend_class, 'widgets', {}
            )
        }
        if hasattr(backend_class, 'field_order'):
            result['field_order'] = backend_class.field_order

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'backend_path': self.kwargs['class_path']
        }


class ImportSetupDeleteView(SingleObjectDeleteView):
    model = ImportSetup
    object_permission = permission_import_setup_delete
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(viewname='importer:import_setup_list')
    view_icon = icon_import_setup_delete

    def get_extra_context(self):
        return {
            'import_setup': None,
            'object': self.object,
            'title': _('Delete the import setup: %s?') % self.object
        }


class ImportSetupEditView(SingleObjectDynamicFormEditView):
    form_class = ImportSetupBackendDynamicForm
    model = ImportSetup
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_id'
    view_icon = icon_import_setup_edit

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit import setup: %s') % self.object
        }

    def get_form_schema(self):
        backend_class = self.object.get_backend_class()
        result = {
            'fields': backend_class.fields,
            'widgets': getattr(
                backend_class, 'widgets', {}
            )
        }
        if hasattr(backend_class, 'field_order'):
            result['field_order'] = backend_class.field_order

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class ImportSetupListView(SingleObjectListView):
    model = ImportSetup
    object_permission = permission_import_setup_view
    view_icon = icon_import_setup_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_import_setup_list,
            'no_results_main_link': link_import_setup_backend_selection.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Import setups are configuration units that will retrieve '
                'files for external locations and create documents from '
                'them.'
            ),
            'no_results_title': _('No import setups available'),
            'title': _('Import setups')
        }


class ImportSetupLogListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_class = ImportSetup
    external_object_permission = permission_import_setup_view
    external_object_pk_url_kwarg = 'import_setup_id'
    view_icon = icon_import_setup_log_list

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_import_setup_log_list,
            'no_results_text': _(
                'This view displays the error log for import setups. '
                'An empty list is a good thing.'
            ),
            'no_results_title': _(
                'There are no error log entries'
            ),
            'object': self.external_object,
            'title': _(
                'Log entries for import setup: %s'
            ) % self.external_object
        }

    def get_source_queryset(self):
        return self.external_object.logs.all()
