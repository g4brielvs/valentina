from faker import Factory


def create_nickname():
    """Creates a female nickname"""

    faker = Factory.create('pt-BR')

    nickname = faker.first_name_female()

    suffix = 'a'
    exceptions = ('Valentina', 'Lucca')

    while not nickname.endswith(suffix) or nickname in exceptions:
        nickname = faker.first_name_female()

    return nickname
