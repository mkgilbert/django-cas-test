import re
import requests
#import pamela
from django.conf import settings
from django.contrib.auth.models import User
from django_cas_ng.backends import CASBackend

from main.models import CVTUser

NAU_CAS = "https://cas.nau.edu/cas/"

class NAUCASBackend(CASBackend):
    """
    authenticate against NAU CAS server
    """
    def user_can_authenticate(self, user):
        try:
            # if no exception is raised, the user exists in PAM LDAP on this system
            #pamela.check_account(user.username)
            user.username == 'mkg52'
        except Exception:
            user.delete()
            return False
        return True

