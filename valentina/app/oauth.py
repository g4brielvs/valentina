from valentina.app.models import Profile

FB_GENDER = {'feminino': Profile.FEMALE, 'masculino': Profile.MALE}


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile, created = Profile.objects.get_or_create(user=user)
        profile.gender = FB_GENDER.get(response.get('gender'), Profile.OTHER)
        profile.timezone = response.get('timezone', '')
        profile.access_token = response.get('access_token', '')
        profile.save()
