# -*- coding: utf-8 -*-


from django.conf import settings
# from core import settings


def conf_to_context(request):
    """
    Function to include certain values of settings in the request context
    to make it available to any view.
    :param request: HTTP request requiring a context
    :return: Dictionary with available values
    """

    return {'ONTASK_HELP_URL': getattr(settings, 'ONTASK_HELP_URL', ''),
            'ONTASK_TIMEOUT': getattr(settings, 'SESSION_COOKIE_AGE', 1800),
            'ONTASK_BASE_URL': getattr(settings, 'BASE_URL', '') + '/'}

