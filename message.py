from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC8d9cd796662e71009515af66742adac0'
auth_token = '959724443bbd2ab2ffaf4edcb774dcbf'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+918360581227',
                              body='body',
                              to='+919888151400'
                          )

print(message.sid)
