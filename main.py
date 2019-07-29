import encryption_tools as crypt
import telebot

TOKEN = '928164897:AAFs_L9eArxE_BdkGJdUw1NdhsTJaf8mlLQ'
data = {}
hide_keyboard = hide_modeboard = telebot.types.ReplyKeyboardRemove()
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('YES', 'NO')
modeboard = telebot.types.ReplyKeyboardMarkup(True, True)
modeboard.row('ENCRYPT', 'DECRYPT')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def bot_start(message):
    data[message.chat.id] = [None, 'encrypt', None, message.from_user.first_name,
                             message.from_user.last_name, '@' + message.from_user.username]
    bot.send_message(
        message.chat.id, "Hello! I can encode any text by a given key. \nSee everything I can do by pressing /commands.")
    bot.send_message(
        message.chat.id, "To start encoding we need to set a key. Use command /set_key. \nAfter you've set the key, you can send me any text to encode.")


@bot.message_handler(commands=['commands'])
def bot_commands(message):
    bot.send_message(message.chat.id, "/start - launch @SecretCipherBot \n/commands - show list of supported commands \n/help - show reference information \n/set_key - set a new key to encode messages \n/show_key - show current key \n/set_mode - sets one of the cryption modes: encoding or decoding \n/show_mode - show current cryption mode: encoding or decoding \n/encode - encode the following message by the current key \n/decode - decode the following message by the current key \n/send - encode and send the following message to any user")


@bot.message_handler(commands=['set_key'])
def bot_set_key(message):
    bot.send_message(message.chat.id, "Please input your new key.")
    data[message.chat.id][1] = 'set_key'


@bot.message_handler(commands=['show_key'])
def bot_show_key(message):
    KEY = data[message.chat.id][0]
    if KEY is None:
        bot.send_message(
            message.chat.id, "There is no key. Please use /set_key")
    else:
        bot.send_message(message.chat.id, f"Current key: {KEY}")


@bot.message_handler(commands=['set_mode'])
def bot_set_mode(message):
    bot.send_message(message.chat.id, "Please choose the mode:",
                     reply_markup=modeboard)
    data[message.chat.id][1] = 'cipher_mode'


@bot.message_handler(commands=['show_mode'])
def bot_show_mode(message):
    if data[message.chat.id][1] == 'encrypt':
        mode = 'Encryption'
    elif data[message.chat.id][1] == 'decrypt':
        mode = 'Decryption'
    bot.send_message(message.chat.id, f"{mode} mode is on now.")


@bot.message_handler(commands=['encode'])
def bot_encode(message):
    bot.send_message(
        message.chat.id, "I will encrypt all the following texts from you until you switch into decryption mode.")
    data[message.chat.id][1] = 'encrypt'


@bot.message_handler(commands=['decode'])
def bot_decode(message):
    bot.send_message(
        message.chat.id, "I will decrypt all the following texts from you until you switch into encryption mode.")
    data[message.chat.id][1] = 'decrypt'


@bot.message_handler(commands=['send'])
def bot_send(message):
    bot.send_message(
        message.chat.id, "Write me a message I should encode and send another user")
    data[message.chat.id][1] = 'send'


@bot.message_handler(commands=['i_wanna_see'])
def bot_get_dataset(message):
    bot.send_message(message.chat.id, f"{data}")


@bot.message_handler(commands=['i_wanna_forget'])
def bot_delete_dataset(message):
    data.clear()


@bot.message_handler(content_types=['text'])
def bot_get_text(message):

    def clean_message(text):
        text, unsupported_symbols = list(text), []
        for letter in text:
            if letter not in crypt.alphabet.values():
                text.remove(letter)
                unsupported_symbols.append(letter)
        return ''.join(text), unsupported_symbols
    clean_text, unsupported_symbols = clean_message(message.text)

    if data[message.chat.id][1] == 'set_key':
        data[message.chat.id][0] = message.text
        if not all(letter in crypt.alphabet.values() for letter in data[message.chat.id][0]):
            bot.reply_to(
                message, f"Error! Invalid symbols were found in your key: {unsupported_symbols}. \nTry another key. Will be more correct {clean_text}")
        else:
            bot.reply_to(message, f"Current key: {data[message.chat.id][0]}")
            data[message.chat.id][1] = 'encrypt'
    elif message.text == "ENCRYPT" and data[message.chat.id][1] == 'cipher_mode':
        data[message.chat.id][1] = 'encrypt'
        bot.reply_to(message, "Encryption mode has been set. I will encrypt all the following texts from you until you switch into decryption mode.", reply_markup=hide_modeboard)
    elif message.text == "DECRYPT" and data[message.chat.id][1] == 'cipher_mode':
        data[message.chat.id][1] = 'decrypt'
        bot.reply_to(message, "Decryption mode has been set. I will decrypt all the following texts from you until you switch into encryption mode.", reply_markup=hide_modeboard)
    elif data[message.chat.id][0] is None:
        bot.send_message(
            message.chat.id, "There is no key. Please use /set_key")
    elif message.text == "YES" and data[message.chat.id][1] == 'encrypt':
        bot.reply_to(message, crypt.post_encryption(
            data[message.chat.id][2], data[message.chat.id][0]), reply_markup=hide_keyboard)
    elif message.text == "NO" and data[message.chat.id][1] == 'encrypt':
        bot.reply_to(message, "Then send me another message to encrypt.",
                     reply_markup=hide_keyboard)
    elif data[message.chat.id][1] == 'encrypt':
        if unsupported_symbols:
            data[message.chat.id][2] = clean_text
            bot.send_message(
                message.chat.id, f"Warning! There are unsupported symbols in your message: {unsupported_symbols}. \nI can exclude them and encode the following text: \n{clean_text} \nDo you agree?", reply_markup=keyboard)
        else:
            data[message.chat.id][2] = message.text
            bot.reply_to(message, crypt.post_encryption(
                data[message.chat.id][2], data[message.chat.id][0]))
    elif data[message.chat.id][1] == 'decrypt' and all(letter in crypt.alphabet.values() for letter in message.text):
        bot.reply_to(message, crypt.post_decryption(
            message.text, data[message.chat.id][0]))
    elif message.text == "YES" and data[message.chat.id][1] == 'send':
        data[message.chat.id][1] = 'get_id'
        bot.reply_to(message, "Whom should I send it? Please input any user's id. To find out user's id use @userinfobot. \nThis user should launch @SecretCipherBot first to receive your message.", reply_markup=hide_keyboard)
    elif message.text == "NO" and data[message.chat.id][1] == 'send':
        bot.reply_to(message, "Then send me another message.",
                     reply_markup=hide_keyboard)
    elif data[message.chat.id][1] == 'send':
        if unsupported_symbols:
            data[message.chat.id][2] = clean_text
            bot.send_message(
                message.chat.id, f"Warning! There are unsupported symbols in your message: {unsupported_symbols}. \nI can exclude them and encode the following text: \n{clean_text} \nDo you agree?", reply_markup=keyboard)
        else:
            data[message.chat.id][2] = message.text
            bot.send_message(
                message.chat.id, "Whom should I send it? Please input any user's id. To find out user's id use @userinfobot. \nThis user should launch @SecretCipherBot first to receive your message.")
            data[message.chat.id][1] = 'get_id'
    elif data[message.chat.id][1] == 'get_id':
        user_id = message.text
        if len(user_id) == 9 and user_id.isdigit():
            bot.send_message(
                user_id, '@' + message.from_user.username + ' sent you a secret message:')
            bot.send_message(user_id, crypt.post_encryption(
                data[message.chat.id][2], data[message.chat.id][0]))
            user_info = bot.get_chat_member(user_id, user_id).user
            bot.send_message(
                message.chat.id, f"Your message is encoded and send to user @{user_info.username} successfully.")
        else:
            bot.send_message(message.chat.id, f"Error! User id is incorrect!")
        data[message.chat.id][1] = 'encrypt'

    else:
        bot.reply_to(
            message, "Error! Invalid symbols were found in the message.")


@bot.message_handler(func=lambda message: True, content_types=['photo', 'document', 'audio', 'sticker', 'voice'])
def bot_get_other(message):
    bot.reply_to(
        message, "This command is not recognized! See supported /commands.")


bot.polling()