import sys

from qrcode import QRCode
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


async def authorization_send_code(client: TelegramClient) -> None:
    """
    Функция авторизации клиента по sms в telegram

    Args:
        client (TelegramClient): Клиет для авторизации
    """
    try:
        phone = input("Enter your phone number: ")
        await client.send_code_request(phone)
        code = input("Please enter your code: ")
        try:
            await client.sign_in(code=code, phone=phone)
        except SessionPasswordNeededError:
            f2 = input("Please enter your password: ")
            await client.sign_in(password=f2)
    except KeyboardInterrupt:
        sys.exit(130) 


async def authorization_qrcode(client: TelegramClient) -> None:
    """
    Функция авторизации клиента по qrcode

    Args:
        client (TelegramClient): Клиет для авторизации
    """
    qrcode_login = await client.qr_login()

    qr = QRCode()
    qr.add_data(qrcode_login.url)
    qr.print_ascii()

    try:
        await qrcode_login.wait()
    except SessionPasswordNeededError:
        try:
            f2 = input("Please enter your password: ")
            await client.sign_in(password=f2)
        except KeyboardInterrupt:
            sys.exit(130) 


async def is_user_authorized(client: TelegramClient) -> bool:
    """
    Функция проверки авторизован ли пользователь

    Args:
        client (TelegramClient): клиент которого проверяем аторизацию

    Returns:
        bool: если клиент авторизован то вернёт True иначе False
    """
    if not await client.is_user_authorized():
        return False
    return True


async def authorization(client: TelegramClient) -> None:
    """
    Функция выбора типа авторизации
    """
    print("""1 = authorization send code\n2 = authorization qrcode\n\n""")
    
    try:
        user_input = input("please type authorization: ")
    except KeyboardInterrupt:
        sys.exit(130) 

    if user_input == "1":
        await authorization_send_code(client)
    elif user_input == "2":
        await authorization_qrcode(client)