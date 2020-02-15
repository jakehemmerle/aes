def pad_message(message: bytearray):
    if type(message) is bytes:
        message = bytearray(message)
    return message + b'\x00' * (16 - (len(message) % 16))  # need message to be divisible into 128 blocks


def unpad_message(message: bytearray):
    count = 0
    for byte in reversed(message):
        if byte == 0:
            count += 1
    return message[:-count]


with open('../data/encrypt_me.txt', 'rb') as message_file:
    plaintext = bytearray(message_file.read())
padded = pad_message(plaintext)
test2 = b"The super secret password is 'password123'.\n\nThis is the third line.\n"


