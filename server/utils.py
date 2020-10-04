from werkzeug.security import check_password_hash, generate_password_hash

from .models import Object, Tag, Terminal, User, database


def create_tables() -> None:  # pragma: no cover
    with database:
        database.create_tables([User, Terminal, Object, Tag])


def createsuperuser(email: str, password: str) -> None:
    if User.select().where(User.email == email):
        raise Exception(f"User `{email}` already exists. Aborting.")
    User.insert(
        email=email, password=generate_password_hash(password), is_admin=True
    ).execute()
