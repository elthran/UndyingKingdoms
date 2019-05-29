# To generate passwords use:
# $ python3
# >>> import os
# >>> os.urandom(24)
# >>> '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

DB_PASSWORD = "db_passwd"

# Secret key for signing cookies
SECRET_KEY = 'complex_pass'
CLOCK_KEY = 'complex_pass2'
# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_SESSION_KEY = 'complex_pass3'
SENDGRID_API_KEY = "api key you can't have"
SERVER_DATABASE_URI = "database uri you don't need"
