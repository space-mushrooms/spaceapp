def save_model_trigger(request, form):
    pass


def save_model_trigger_admin(request, form):
    instance = form.save(commit=False)
    if not hasattr(instance, 'created_by'):
        instance.created_by = request.user
    instance.modified_by = request.user
    instance.save()
    form.save_m2m()
    return instance
