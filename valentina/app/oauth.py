from valentina.app.models import Profile

FB_GENDER = {'feminino': Profile.FEMALE, 'masculino': Profile.MALE}


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = Profile.objects.get(user=user)
        if profile is None:
            profile = Profile(user=user)
        profile.gender = FB_GENDER.get(response.get('gender'), Profile.OTHER)
        profile.timezone = response.get('timezone', '')
        profile.access_token = response.get('access_token', '')
        profile.save()
