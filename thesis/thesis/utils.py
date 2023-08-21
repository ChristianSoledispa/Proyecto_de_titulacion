import pyotp
from datetime import datetime, timedelta


def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session["otp_secret_key"] = totp.secret
    valid_date = datetime.now() + str(valid_date)

    print(f"Your one time password is {otp}")