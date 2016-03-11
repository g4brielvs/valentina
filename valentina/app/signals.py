from ipware.ip import get_real_ip, get_ip
from valentina.app.models import Ip


def save_user_ip(sender, user, request, **kwargs):
    address = get_real_ip(request)
    if address is None:
        address = get_ip(request)
    Ip.objects.create(user=user, address=address)
