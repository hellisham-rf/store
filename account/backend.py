from django.contrib.auth import backends
from .models import User
from django.db.models import Q
class Emialbackend(backends.ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        try:
            q = Q(username__iexact=username) | Q(email__iexact=username)
            user = User.objects.get(q)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            pass

        return super().authenticate(request, username, password, **kwargs)