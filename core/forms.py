from django import forms


FIELD_CLASS = "form-input"
CHECKBOX_CLASS = "form-checkbox"
SELECT_CLASS = "form-input"


class StyledFormMixin:
    placeholders = {}
    autocomplete = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widget_styles()

    def apply_widget_styles(self):
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", CHECKBOX_CLASS)
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", SELECT_CLASS)
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", f"{FIELD_CLASS} min-h-28")
                widget.attrs.setdefault("rows", 4)
            elif not isinstance(widget, forms.HiddenInput):
                widget.attrs.setdefault("class", FIELD_CLASS)
            if name in self.placeholders:
                widget.attrs.setdefault("placeholder", self.placeholders[name])
            if name in self.autocomplete:
                widget.attrs.setdefault("autocomplete", self.autocomplete[name])
