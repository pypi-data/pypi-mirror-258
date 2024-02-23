import json

from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from ..classes import NullBackend

IMPORT_ERROR_EXCLUSION_TEXTS = (
    'doesn\'t look like a module path'
)


class BackendModelMixin(models.Model):
    # TODO: Use common.model_mixins.BackendModelMixin after upgrade to
    # version 4.0.
    backend_path = models.CharField(
        max_length=128,
        help_text=_('The dotted Python path to the backend class.'),
        verbose_name=_('Backend path')
    )
    backend_data = models.TextField(
        blank=True, help_text=_('JSON encoded data for the backend class.'),
        verbose_name=_('Backend data')
    )

    class Meta:
        abstract = True

    def get_backend_class(self):
        """
        Retrieves the backend by importing the module and the class.
        """
        try:
            return import_string(dotted_path=self.backend_path)
        except ImportError as exception:
            for import_error_exclusion_text in IMPORT_ERROR_EXCLUSION_TEXTS:
                if import_error_exclusion_text in str(exception):
                    raise
            return NullBackend

    def get_backend_instance(self):
        return self.get_backend_class()(
            **self.get_backend_data()
        )

    def get_backend_label(self):
        """
        Return the label that the backend itself provides. The backend is
        loaded but not initialized. As such the label returned is a class
        property.
        """
        try:
            return self.get_backend_class().label
        except ImportError:
            return _('Unknown backend')

    get_backend_label.short_description = _('Backend')
    get_backend_label.help_text = _('The backend class for this entry.')

    def get_backend_data(self):
        return json.loads(s=self.backend_data or '{}')

    def set_backend_data(self, obj):
        self.backend_data = json.dumps(obj=obj)
