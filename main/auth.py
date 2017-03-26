import re
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.shortcuts import HttpResponseRedirect

from main.models import CVTUser

NAU_CAS = "https://cas.nau.edu/cas/"

class NAUCASBackend(object):
    """
    authenticate against NAU CAS server
    """
    def authenticate(self, request, user=None):
        if user is not None:
            try:
                cvt_user = CVTUser.objects.get(user=user)
                if cvt_user.is_logged_in:
                    return cvt_user
                else:
                    return None
            except Exception:
                return None
        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return CVTUser.objects.get(user=user)
        except Exception:
            return None

