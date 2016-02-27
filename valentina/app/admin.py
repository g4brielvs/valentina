from django.contrib import admin
from valentina.app.models import Profile


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'gender', 'email', 'last_login',
                    'date_joined')
    search_fields = ('nickname', 'name', 'email')

    def email(self, obj):
        return obj.user.email

    email.short_description = 'e-mail'

    def last_login(self, obj):
        return obj.user.last_login

    last_login.short_description = 'último login'

    def date_joined(self, obj):
        return obj.user.date_joined

    date_joined.short_description = 'criado em'


admin.site.register(Profile, ProfileModelAdmin)
