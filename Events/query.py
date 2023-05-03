from .models import Events


def count_verified_events() -> int:
    return Events.objects.filter(is_published=True).count()
