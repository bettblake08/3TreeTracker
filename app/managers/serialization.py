""" In this module hosts the Serialization class for validation checks

flask_bcrypt variable is used to hash passwords and check for a match of a password.
It is an instance of the Bcrypt class from module flask_bcrypt.
"""

import re


class Serialization:
    """ Serialization Class
    This class holds all the function required to validate the required inputs
    received from the client such as:
        -   email
        -   password
    """

    @classmethod
    def test_password(cls, password, reg_type):
        """ This function tests the validity of the password by running it through
        a regex expression.
        Args:
            password (string)
            reg_type (int)
                1.  Tests if password contains 1 uppercase, 1 lowercase, 1 digit and
                1 special character [@$#.].
        Returns:
            bool:   Return True if password passes, False if password fails or reg_type
                    is invalid
        """

        pattern = None

        if reg_type == 1:
            pattern = re.compile(
                r"((?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@\$#.!]).{8,16})"
            )

        if not pattern:
            return False
        return bool(pattern.match(password, 0))

    @classmethod
    def test_email(cls, email):
        """ This function test the validity of an email string.
        Args:
            -   email (string)
        Returns:
            bool: Returns True if email passes regex tests, False if password fails
        """

        pattern = re.compile(
            r"(^[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )

        return bool(pattern.match(email, 0))
