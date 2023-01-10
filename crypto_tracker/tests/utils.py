import random
import string


def random_lower_string(length: int) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"{random_lower_string(10)}@gmail.com"

