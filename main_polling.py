from config import TOKEN
import telebot

bot = telebot.TeleBot(TOKEN)

with open('courses.txt') as file:
    courses = [item.split(',') for item in file]

with open('schedule.txt') as file:
    courses_plan = {
        'start': [],
        'pro': [],
        'other': [],
    }
    for item in file:
        if 'start' in item.lower():
            courses_plan['start'].append(item)
        elif 'pro' in item.lower():
            courses_plan['pro'].append(item)
        else:
            courses_plan['other'].append(item)







@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, 'Hello user!')

@bot.message_handler(commands=['help'])
def message_help(message):
    commands = '/courses -\n'\
                '/schedule - '

    bot.reply_to(message, commands)

@bot.message_handler(commands=['courses'])
def list_of_courses(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    for text, url in courses:
        url_button = telebot.types.InlineKeyboardButton(text=text.strip(), url=url.strip(' \n'))
        keyboard.add(url_button)

    bot.send_message(message.chat.id, 'List of courses:', reply_markup = keyboard)


@bot.message_handler(commands=['schedule'])
def list_of_courses(message):
    res = 'Schedule of courses\n\n'

    for category in courses_plan:
        for item in courses_plan[category]:
            title, date = item.split(',')
            res += f'<b>{title}</b>:  <code>{date}</code>'
        res += ' \n'

    bot.send_message(message.chat.id, text = res, parse_mode='HTML' )

@bot.message_handler(func = lambda x: x.text.startswith('info'))
def get_courses_info(message):
    text_from_user = message.json['text']
    if 'python' in text_from_user.lower():
        res=''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'python' in title.lower():
                    res += f'<b>{title}</b>:  <code>{date}</code>'
            res += '\n'
        bot.send_message(message.chat.id, text=res, parse_mode='HTML')
    elif 'java' in text_from_user.lower():
        res=''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'java' in title.lower():
                    res += f'<b>{title}</b>:  <code>{date}</code>'
            res += '\n'
        bot.send_message(message.chat.id, text=res, parse_mode='HTML')



if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
