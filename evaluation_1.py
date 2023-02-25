class UsernameValidator:
    def __init__(self, username):
        self.username = username

    def validate_username(self):
        if len(self.username) < 6:
            raise ValueError(
                "El nombre de usuario debe contener al menos 6 caracteres")
        elif len(self.username) > 12:
            raise ValueError(
                "El nombre de usuario no puede contener más de 12 caracteres")
        elif not self.username.isalnum():
            raise ValueError(
                "El nombre de usuario puede contener solo letras y números")
        else:
            return True


class PasswordValidator:
    def __init__(self, password):
        self.password = password

    def validate_password(self):
        if len(self.password) < 8:
            raise ValueError(
                "La contraseña debe contener al menos 8 caracteres")
        elif not any(char.isupper() for char in self.password):
            raise ValueError(
                "La contraseña debe contener al menos una letra mayúscula")
        elif not any(char.islower() for char in self.password):
            raise ValueError(
                "La contraseña debe contener al menos una letra minúscula")
        elif not any(char.isdigit() for char in self.password):
            raise ValueError("La contraseña debe contener al menos un número")
        elif any(char.isspace() for char in self.password):
            raise ValueError(
                "La contraseña no puede contener espacios en blanco")
        elif self.password.isalnum():
            raise ValueError(
                "La contraseña debe contener al menos un carácter no alfanumérico")
        else:
            return True


def get_valid_credentials():
    while True:
        username = input("Ingrese su nombre de usuario: ")

        try:
            username_validator = UsernameValidator(username)
            username_validator.validate_username()
        except ValueError as ve:
            print(ve)
            continue

        password = input("Ingrese su contraseña: ")

        try:
            password_validator = PasswordValidator(password)
            password_validator.validate_password()
        except ValueError as ve:
            print(ve)
            continue

        print("Credenciales correctas")
        return username, password


if __name__ == "__main__":
    get_valid_credentials()
