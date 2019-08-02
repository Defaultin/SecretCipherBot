import encryption_tools as crypt
import time


def clean_message(text):
    text, unsupported_symbols = list(text), []
    for letter in text:
        if letter not in crypt.alphabet.values():
            text.remove(letter)
            unsupported_symbols.append(letter)
            print(unsupported_symbols)
    return ''.join(text), unsupported_symbols


def run(text, key):
    encoding_start_time = time.perf_counter()
    message = crypt.post_encryption(text, key)
    encoding_finish_time = time.perf_counter()
    decoding_start_time = time.perf_counter()
    result = crypt.post_decryption(message, key)
    decoding_finish_time = time.perf_counter()
    print(f"\nEncrypted message: \n{message}\n")
    print(f"Decrypted message: \n{result}\n")
    print(f"Text length = {len(text)} symbols")
    print(
        f"Encoding time = {encoding_finish_time - encoding_start_time} seconds")
    print(
        f"Decoding time = {decoding_finish_time - decoding_start_time} seconds")
    print(
        f"Encoding speed = {len(text)/(encoding_finish_time - encoding_start_time)} letter/seconds")
    print(
        f"Decoding speed = {len(text)/(decoding_finish_time - decoding_start_time)} letter/seconds")


def main():
    with open('random_text.txt', 'r') as file:
        text = file.read()
    clean_text, unsupported_symbols = clean_message(text)
    key = str(input("Enter the key: "))
    if unsupported_symbols:
        print(
            f"Warning! There are unsupported symbols in your message: {unsupported_symbols}.")
        choice = str(input("Do you want to encode this text? ")).lower()
        if choice.startwith('y'):
            run(clean_text, key)
        else:
            print("Send me another text.")
    else:
        run(text, key)


if __name__ == "__main__":
    main()
    time.sleep(10)