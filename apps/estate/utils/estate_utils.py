from django.db.models import FileField, ImageField
from django.db.models.fields.files import FieldFile
from urllib.parse import urljoin
from inspect import ismethod
from typing import Union, List, Tuple, Dict, Any, Optional


class AdvancedModelFieldExtractor:
    """
    A sophisticated field extractor for Django models that handles:
    - Nested field paths with multiple separator options
    - File/Image field URL resolution
    - Method calls (including get_* methods)
    - Custom display names
    - Absolute URL generation for media files
    """

    def __init__(self, model_instance, context: Optional[dict] = None):
        """
        Initialize with a model instance and optional context.

        Args:
            model_instance: Django model instance to extract fields from
            context: Optional dictionary that may include 'request' and other settings
        """
        self.model_instance = model_instance
        self.context = context or {}
        self.request = self.context.get('request')

    def extract(self, fields_to_extract: Union[List, Tuple]) -> Dict[str, Any]:
        """
        Extract specified fields from the model instance.

        Args:
            fields_to_extract: List/tuple of fields to extract. Can include:
                - Simple field names ('title')
                - Nested paths ('user__profile__image')
                - Method calls ('get_full_name()')
                - Tuples for custom display names: [('field_name', 'display_name')]

        Returns:
            Dictionary with extracted values keyed by field names or display names
        """
        result = {}

        for field in fields_to_extract:
            if isinstance(field, (list, tuple)) and len(field) == 2:
                field_name, display_name = field
                result[display_name] = self._extract_single_field(field_name)
            else:
                result[field] = self._extract_single_field(field)

        return result

    def _extract_single_field(self, field_path: str) -> Any:
        """
        Extract value for a single field path.

        Handles:
        - get_* methods
        - Nested field traversal
        - Method calls
        - File/Image field URL resolution
        """
        # Check for get_* methods first
        get_method_name = f'get_{field_path}'
        if hasattr(self.model_instance, get_method_name):
            method = getattr(self.model_instance, get_method_name)
            return method(self.context) if ismethod(method) else method

        # Split field path using the first found separator
        parts = self._split_field_path(field_path)
        value = self.model_instance

        for part in parts:
            if value is None:
                break

            # Handle method calls
            if part.endswith('()'):
                value = self._call_method(value, part[:-2])
                continue

            # Get attribute value
            value = self._get_attribute_value(value, part)

            # Handle File/Image fields
            value = self._process_file_field(value)

        return value

    def _split_field_path(self, field_path: str) -> List[str]:
        """Split field path using the first found supported separator."""
        separators = ['__', '.', '->']
        for sep in separators:
            if sep in field_path:
                return field_path.split(sep)
        return [field_path]

    def _call_method(self, obj: Any, method_name: str) -> Any:
        """Safely call a method on an object if it exists."""
        if hasattr(obj, method_name):
            method = getattr(obj, method_name)
            return method() if callable(method) else method
        return None

    def _get_attribute_value(self, obj: Any, attr_name: str) -> Any:
        """Get an attribute value from an object, handling callables."""
        try:
            attr = getattr(obj, attr_name)
            if callable(attr) and not isinstance(attr, (FieldFile, type)):
                return attr()
            return attr
        except (AttributeError, ValueError):
            return None

    def _process_file_field(self, value: Any) -> Any:
        """Process FileField/ImageField values to get absolute URLs."""
        if isinstance(value, FieldFile) and self.request and value.name:
            return self._get_absolute_media_url(value.url)
        return value

    def _get_absolute_media_url(self, relative_url: str) -> str:
        """Generate absolute URL for media files using request."""
        if not self.request:
            return relative_url
        return urljoin(self.request.build_absolute_uri('/'), relative_url.lstrip('/'))

    @classmethod
    def extract_fields(
        cls,
        model_instance,
        fields_to_extract: Union[List, Tuple],
        context: Optional[dict] = None
    ) -> Dict[str, Any]:
        """
        Class method for quick usage without instantiation.

        Args:
            model_instance: Django model instance to extract from
            fields_to_extract: List/tuple of fields to extract
            context: Optional context dictionary

        Returns:
            Dictionary of extracted fields
        """
        extractor = cls(model_instance, context)
        return extractor.extract(fields_to_extract)