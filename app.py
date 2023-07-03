import telebot
import openai
import json
from telebot import types
import random

# Set up your Telegram bot token
bot_token = 'YOUR_BOT_TOKEN'

# Set up your OpenAI API credentials
openai.api_key = 'YOUR_API_KEY'

bot = telebot.TeleBot(bot_token)

with open('questions.json', 'r') as f:
    questions_data = json.load(f)

oral_questions = questions_data['oral']
writing_questions = questions_data['writing']
letter_questions = questions_data['letter']

CALLBACK_ORAL = 'callback_oral'
CALLBACK_WRITING = 'callback_writing'
CALLBACK_LETTER = 'callback_letter'
CALLBACK_SAMPLE_ANSWER = 'callback_sample_answer'
CALLBACK_SKIP = 'callback_skip'
CALLBACK_MAIN_MENU = 'callback_main_menu'
CALLBACK_VOCABULARY = 'callback_vocabulary'

user_states = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_states[user_id] = 'main_menu'
    send_main_menu(user_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.message.chat.id
    callback_data = call.data

    if callback_data == CALLBACK_MAIN_MENU:
        user_states[user_id] = 'main_menu'
        send_main_menu(user_id)

    elif callback_data == CALLBACK_ORAL:
        user_states[user_id] = 'oral_question'
        send_question(user_id, oral_questions)

    elif callback_data == CALLBACK_WRITING:
        user_states[user_id] = 'writing_question'
        send_question(user_id, writing_questions)

    elif callback_data == CALLBACK_LETTER:
        user_states[user_id] = 'letter_question'
        send_question(user_id, letter_questions)

    elif callback_data.startswith(CALLBACK_SAMPLE_ANSWER):
        _, question = callback_data.split(':')
        print(question)
        send_sample_answer(user_id, question)

    elif callback_data.startswith(CALLBACK_WRITING):
        print(callback_data)
        _, type = callback_data.split(':')
        print(type)
        send_writing_section_question(user_id, call, type)

    elif callback_data.startswith(CALLBACK_LETTER):
        print(callback_data)
        _, type, section, question = callback_data.split(':')
        print(type)
        verify_letter_answer(user_id, call, question)

    elif callback_data.startswith(CALLBACK_SKIP):
        _, question = callback_data.split(':')
        question_list = user_states[user_id]
        data = get_question_list_by_type(question_list)
        send_question(user_id, data)

    elif callback_data == CALLBACK_VOCABULARY:
        bot.send_message(
            user_id, "Please enter the text for vocabulary generation:")
        bot.register_next_step_handler(call.message, generate_vocabulary)


def send_writing_section_question(user_id, call, section):
    print(section)
    # print(question)
    if section == 'intro':
        bot.send_message(
            user_id, "Your current writing type is Introduction.\n\nDo not write more than 60-70 words for introduction.")
    elif section == 'body':
        bot.send_message(
            user_id, "Your current writing type is Body Paragraph.\n\nNot more than 120-150 words for body paragraphs.")
    elif section == 'conclusion':
        bot.send_message(user_id, "Your current writing type is Conclusion.\n\nDo not write more than 60-70 words for conclusion.")
    elif section == 'full':
        bot.send_message(user_id, "Your current writing type is Full Essay.\n\nWrite between 200-300 words.")

    bot.send_message(user_id, "Please enter your answer:")
    user_states[user_id] = f'writing_question:{section}'
    bot.register_next_step_handler(call.message, verify_writing_answer)


def verify_writing_answer(message):
    user_id = message.chat.id
    section_data = user_states[user_id].split(':')
    print(section_data)
    section = section_data[1]
    # question = section_data[2]
    answer = message.text.strip()

    if section == 'intro':
        words_count = len(answer.split())
        if words_count > 60 and words_count <= 70:
            test = bot.send_message(user_id, "wait, we are analysing your score 💯").message_id
            rating = get_value_intro_of_rating(answer, user_id)
            response = "Congrat`s, Here is Our rating for this answer \n\n" + rating
            bot.delete_message(user_id, test)
            bot.send_message(user_id, response)
        else:
            bot.send_message(
                user_id, "Error: Wrong answer. Please provide an answer with 60-70 words.")
            bot.send_message(user_id, "Please provide the answer again:")
            bot.register_next_step_handler(message, verify_writing_answer)  # Call the function again
            return
    elif section == 'body':
        words_count = len(answer.split())
        if words_count > 120 and words_count <= 150:
            test = bot.send_message(user_id, "wait, we are analysing your score 💯").message_id
            rating = get_value_body_of_rating(answer, user_id)
            response = "Congrat`s, Here is Our rating for this answer \n\n" + rating
            bot.delete_message(user_id, test)
            bot.send_message(user_id, response)
        else:
            bot.send_message(
                user_id, "Error: Wrong answer. Please provide an answer with 120-150 words.")
            bot.send_message(user_id, "Please provide the answer again:")
            bot.register_next_step_handler(message, verify_writing_answer)  # Call the function again
            return
        
    elif section == 'conclusion':
        words_count = len(answer.split())
        if words_count > 60 and words_count <= 70:
            test = bot.send_message(user_id, "wait, we are analysing your score 💯").message_id
            rating = get_value_conclusion_of_rating(answer, user_id)
            response = "Congrat`s, Here is Our rating for this answer \n\n" + rating
            bot.delete_message(user_id, test)
            bot.send_message(user_id, response)
        else:
            bot.send_message(
                user_id, "Error: Wrong answer. Please provide an answer with 60-70 words.")
            bot.send_message(user_id, "Please provide the answer again:")
            bot.register_next_step_handler(message, verify_writing_answer)  # Call the function again
            return
        
    elif section == 'full':
        words_count = len(answer.split())
        if words_count > 200 and words_count <= 300:
            test = bot.send_message(user_id, "wait, we are analysing your score 💯").message_id
            rating = get_value_full_of_rating(answer, user_id)
            response = "Congrat`s, Here is Our rating for this answer \n\n" + rating
            bot.delete_message(user_id, test)
            bot.send_message(user_id, response)
        else:
            bot.send_message(
                user_id, "Error: Wrong answer. Please provide an answer with 200-300 words.")
            bot.send_message(user_id, "Please provide the answer again:")
            bot.register_next_step_handler(message, verify_writing_answer)  # Call the function again
            return
    else:
        # Add similar verification logic for other sections (body, conclusion, full essay) here
        bot.send_message(
            user_id, "Verification logic for this section is not implemented yet.")

    # Update user state to writing_question
    user_states[user_id] = 'writing_question'
    send_question(user_id, writing_questions)


def send_main_menu(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    oral_button = types.InlineKeyboardButton(
        '1. Oral Questions', callback_data=CALLBACK_ORAL)
    writing_button = types.InlineKeyboardButton(
        '2. Writing Questions', callback_data=CALLBACK_WRITING)
    letter_button = types.InlineKeyboardButton(
        '3. Letter Writing Questions', callback_data=CALLBACK_LETTER)

    # Add another button here

    vocabulary_button = types.InlineKeyboardButton(
        '4. Vocabulary Generation', callback_data=CALLBACK_VOCABULARY)
    keyboard.add(oral_button, writing_button, letter_button, vocabulary_button)
    bot.send_message(
        user_id, "🎉 Welcome aboard the EEC IELTS Amazing Robot! 🤖 Ready to smash those IELTS goals! 🚀 \n\nPlease choose an option:", reply_markup=keyboard)


def send_question(user_id, question_list):
    question_type = user_states.get(user_id)
    question = user_states.get(str(user_id) + '_question')
    # print(question_list)
    print(user_states)
    print(question_type)
    print(question_list)
    if not question_list:
        bot.send_message(user_id, "No questions available.")
        return

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    sample_answer_button = types.InlineKeyboardButton(
        'Sample Answer 🧠', callback_data=f'{CALLBACK_SAMPLE_ANSWER}:{question}')
    skip_button = types.InlineKeyboardButton(
        'Skip Question ⏩', callback_data=f'{CALLBACK_SKIP}:{question}')
    main_menu_button = types.InlineKeyboardButton(
        'Main Menu ✨', callback_data=CALLBACK_MAIN_MENU)
    keyboard.add(sample_answer_button, skip_button)
    # Add the button as a new row with full width
    keyboard.row(main_menu_button)

    if question_type == 'oral_question':
        question = "📝 Question: \n\n" + get_random_question(question_list)
        user_states['user_' + str(user_id) + '_question'] = question
        bot.send_message(user_id, question, reply_markup=keyboard)
        user_states[user_id] = 'oral_question'

    elif question_type == 'writing_question':
        print("\n-----------------------in writing_question-----------------------\n")
        question = "📝 Question: \n\n" + get_random_question(question_list)
        user_states['user_' + str(user_id) + '_question'] = str(question)
        user_states[user_id] = 'writing_question'
        intro = 'intro'
        body = 'body'
        conclusion = 'conclusion'
        full = 'full'

        intro_button = types.InlineKeyboardButton(
            'Introduction 🎬', callback_data=f'{CALLBACK_WRITING}:{intro}')
        body_button = types.InlineKeyboardButton(
            'Body Paragraph 🗨️', callback_data=f'{CALLBACK_WRITING}:{body}')
        conclusion_button = types.InlineKeyboardButton(
            'Conclusion ⚖️', callback_data=f'{CALLBACK_WRITING}:{conclusion}')
        full_essay_button = types.InlineKeyboardButton(
            'Full Essay 💯', callback_data=f'{CALLBACK_WRITING}:{full}')
        keyboard.add(intro_button, body_button,
                     conclusion_button, full_essay_button)
        
        bot.send_message(user_id, question, reply_markup=keyboard)
        print("\n-----------------------Sent-----------------------\n")

    elif question_type == 'letter_question' or question_type == 'letter_question_answer':
        question = "📝 Question: \n\n" + get_random_question(question_list)
        user_states['user_' + str(user_id) + '_question'] = question
        bot.send_message(user_id, question, reply_markup=keyboard)
        bot.send_message(user_id,"Please enter your answer:")
        user_states[user_id] = 'letter_question_answer'  # Update user state to 'letter_question_answer'


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'letter_question_answer')
def handle_letter_question_answer(message):
    user_id = message.chat.id
    answer = message.text.strip()
    verify_letter_answer(message)


def verify_letter_answer(message):
    user_id = message.chat.id
    answer = message.text.strip()
    words_count = len(answer.split())
    print(answer)
    print(words_count)
    if words_count > 100:
        test = bot.send_message(user_id, "wait, we are analysing your score 💯").message_id
        rating = get_value_of_rating(answer, user_id)
        response = "Congrat`s, Here is Our rating for this answer \n\n" + rating
        bot.delete_message(user_id, test)
        bot.send_message(user_id, response)
    else:
        bot.send_message(
            user_id, "Error: Wrong answer. Please provide an answer with 200-300 words.")
        bot.send_message(user_id, "Please provide the answer again:")
        bot.register_next_step_handler(message, verify_letter_answer)  # Call the function again
        return

def send_sample_answer(user_id, question):
    mes_id = bot.send_message(
        user_id, "We are generating a sample answer... Please wait... ⏳").message_id
    questions = user_states.get("user_" + str(user_id) + "_question")
    answer = generate_sample_answer(questions)
    bot.delete_message(user_id, mes_id)
    bot.send_message(user_id, answer)


def get_random_question(question_list):
    return random.choice(question_list)


def get_question_list_by_type(question_type):
    if question_type == 'oral_question':
        return oral_questions
    elif question_type == 'writing_question':
        return writing_questions
    elif question_type == 'letter_question' or question_type == 'letter_question_answer':
        return letter_questions
    else:
        return []

def get_value_intro_of_rating(question, user_id):
    sent_quest = user_states['user_' + str(user_id) + '_question']
    main_question = "check the given ielts introduction according to the IDP ielts checking criteria and give bands according to idp band descriptors and also check the answer for this question based on that give rating \n\n question is " + str(sent_quest) + "\n if the answer is right then give bands rating individually in given format 1)COHERENCE AND COHESION: 2)LEXICAL RESOURCE: 3)GRAMMATICAL RANGE: 4)TASK ACHIEVEMENT:, without any description need only rating \n\n Here is the answer " + str(question) 
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": str(main_question)})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    reply = chat.choices[0].message.content
    return reply

def get_value_body_of_rating(question, user_id):
    sent_quest = user_states['user_' + str(user_id) + '_question']
    main_question = "check the given ielts body paragraph according to the IDP ielts checking criteria and give bands according to idp band descriptors and also check the answer for this question based on that give rating \n\n question is " + str(sent_quest) + "\n if the answer is right then give bands rating individually in given format 1)COHERENCE AND COHESION: 2)LEXICAL RESOURCE: 3)GRAMMATICAL RANGE: 4)TASK ACHIEVEMENT:, without any description need only rating \n\n Here is the answer " + str(question) 
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": str(main_question)})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    reply = chat.choices[0].message.content
    return reply

def get_value_conclusion_of_rating(question, user_id):
    sent_quest = user_states['user_' + str(user_id) + '_question']
    main_question = "check the given ielts conclusion according to the IDP ielts checking criteria and give bands according to idp band descriptors and also check the answer for this question based on that give rating \n\n question is " + str(sent_quest) + "\n if the answer is right then give bands rating individually in given format 1)COHERENCE AND COHESION: 2)LEXICAL RESOURCE: 3)GRAMMATICAL RANGE: 4)TASK ACHIEVEMENT:, without any description need only rating \n\n Here is the answer " + str(question) 
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": str(main_question)})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    reply = chat.choices[0].message.content
    return reply

def get_value_full_of_rating(question, user_id):
    sent_quest = user_states['user_' + str(user_id) + '_question']
    main_question = "check the given ielts essay according to the IDP ielts checking criteria and give bands according to idp band descriptors and also check the answer for this question based on that give rating \n\n question is " + str(sent_quest) + "\n if the answer is right then give bands rating individually in given format 1)COHERENCE AND COHESION: 2)LEXICAL RESOURCE: 3)GRAMMATICAL RANGE: 4)TASK ACHIEVEMENT:, without any description need only rating \n\n Here is the answer " + str(question) 
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": str(main_question)})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    reply = chat.choices[0].message.content
    return reply

def get_value_of_rating(question, user_id):
    sent_quest = user_states['user_' + str(user_id) + '_question']
    main_question = "check the given ielts latter according to the IDP ielts checking criteria and give bands according to idp band descriptors and also check the answer for this question based on that give rating \n\n question is " + str(sent_quest) + "\n if the answer is right then give bands rating individually in given format 1)COHERENCE AND COHESION: 2)LEXICAL RESOURCE: 3)GRAMMATICAL RANGE: 4)TASK ACHIEVEMENT:, without any description need only rating \n\n Here is the answer " + str(question) 

    messages = [
        {"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": str(main_question)})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    reply = chat.choices[0].message.content
    return reply


def generate_sample_answer(question):
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": str(question)})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    reply = chat.choices[0].message.content
    return reply

# Copy this and Change as per your needs.


def generate_vocabulary(message):
    mes_id = bot.send_message(
        message.chat.id, "We are generating vocabulary... Please wait... ⏳").message_id
    text = "Give me the 10 Vocabulary of " + message.text
    print(text)
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    vocabulary = response.choices[0].message.content.split("\n")
    bot.delete_message(message.chat.id, mes_id)
    reply = "Generated vocabulary:\n\n" + "\n".join(vocabulary)
    bot.send_message(message.chat.id, reply)


# Start the bot
bot.polling()
