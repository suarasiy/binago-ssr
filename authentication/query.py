from .models import User


def count_verified_users() -> int:
    return User.objects.filter(is_verified=True).count()
