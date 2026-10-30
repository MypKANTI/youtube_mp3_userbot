from qrcode import QRCode
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


async def authorization_send_code(client: TelegramClient) -> None:
    phone = input("Enter your phone number: ")
    await client.send_code_request(phone)
    code = input("Please enter your code: ")
    try:
        await client.sign_in(code=code, phone=phone)
    except SessionPasswordNeededError:
        f2 = input("Please enter your password: ")
        await client.sign_in(password=f2)


async def authorization_qrcode(client: TelegramClient) -> None:
    qrcode_login = await client.qr_login()

    qr = QRCode()
    qr.add_data(qrcode_login.url)
    qr.print_ascii()

    try:
        await qrcode_login.wait()
    except SessionPasswordNeededError:
        f2 = input("Please enter your password: ")
        await client.sign_in(password=f2)


async def is_user_authorized(client: TelegramClient) -> bool:
    """
    Check if user is authorized.
    """
    #await client.connect()

    if not await client.is_user_authorized():
        return False
    return True


async def authorization() -> None:
    print("""1 = authorization send code\n2 = authorization qrcode\n\n""")
    user_input = input("please type authorization: ")

    if user_input == "1":
        await authorization_send_code()
    elif user_input == "2":
        await authorization_qrcode()
