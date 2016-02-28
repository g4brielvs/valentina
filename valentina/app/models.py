from django.conf import settings
from django.db import models
from faker import Factory


class Profile(models.Model):

    FEMALE = 'F'
    MALE = 'M'
    OTHER = 'O'
    GENDERS = ((FEMALE, 'Feminino'), (MALE, 'Masculino'), (OTHER, 'Outro'))

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='Usuário')
    gender = models.CharField('gênero', max_length=1, choices=GENDERS)
    timezone = models.CharField('fuso-horário', max_length=255)
    nickname = models.CharField('apelido', max_length=255)
    first_access = models.BooleanField('primeiro acesso', default=True)

    def __str__(self):
        return self.nickname if self.nickname else self.user.get_full_name()

    @staticmethod
    def create_nickname():
        faker = Factory.create(settings.LANGUAGE_CODE)
        suffix = 'a'
        exceptions = ('Valentina', 'Lucca')
        nickname = faker.first_name_female()
        while not nickname.endswith(suffix) or nickname in exceptions:
            nickname = faker.first_name_female()
        return nickname

    class Meta:
        ordering = ['nickname']
        verbose_name = 'usuária'
        verbose_name_plural = 'usuárias'
