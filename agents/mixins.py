from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, reverse
from django.http import HttpResponse


class OrganizerLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated. or is_organizer"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizer:
            return redirect('/leads')
        return super().dispatch(request, *args, **kwargs)
