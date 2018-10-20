def get_form_errors(form):
    if getattr(form, '_errors', None):
        return {field: str(values[0]) for field, values in form._errors.items()}
    return {}
