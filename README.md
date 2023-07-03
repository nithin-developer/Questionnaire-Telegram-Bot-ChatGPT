# Questionnaire Telegram Bot (ChatGPT)

![Questionnaire Telegram Bot](https://github.com/nithin-developer/Questionnaire-Telegram-Bot-ChatGPT/assets/92811211/dac17d84-65cf-43ed-826b-1d78be8ae69c)

The Questionnaire Telegram Bot is a chatbot developed to facilitate the process of conducting questionnaires and providing ratings for user answers. This Telegram bot utilizes the power of ChatGPT, an advanced language model, to generate sample answers and evaluate user responses. The bot supports three types of questions: oral, writing, and letter writing questions.

## Features

- **Question Types**: The bot supports three types of questions:

  - **Oral Questions**: These questions require users to provide oral responses, which can be recorded and evaluated by the bot.

  - **Writing Questions**: These questions require users to enter their answers as text, which are then evaluated by the bot.

  - **Letter Writing Questions**: These questions ask users to write a letter on a specific topic, and the bot can provide sample answers for guidance.

- **Rating System**: The bot uses ChatGPT to evaluate user responses and provide a rating based on various criteria such as relevance, coherence, and fluency. This helps users understand the quality of their answers.

- **Sample Answer Generation**: Users can request the bot to generate sample answers for writing and letter writing questions. This feature provides users with examples and guidance for crafting their own responses.

- **User-Friendly Interface**: The bot provides a user-friendly chat interface in Telegram, making it easy for users to interact and receive feedback on their answers.

## Usage

1\. Search for the Questionnaire Telegram Bot in Telegram and start a chat with the bot.

2\. The bot will present different types of questions (oral, writing, and letter writing) to the user.

3\. Users can choose the desired question type and answer accordingly:

   - For oral questions, users can record their responses and send them to the bot.

   - For writing questions, users can type their answers directly in the chat.

   - For letter writing questions, users can follow the provided prompt and compose their letters.

4\. After receiving the user's response, the bot will utilize ChatGPT to evaluate the answer and provide a rating based on different criteria.

5\. Users can also request the bot to generate sample answers for writing and letter writing questions to gain insights and guidance.

6\. Users can continue the conversation with the bot, answering additional questions and receiving ratings and sample answers as needed.

## Setup and Configuration

To set up and configure the Questionnaire Telegram Bot, follow these steps:

1\. Clone the repository to your local machine:

```bash

git clone https://github.com/nithin-developer/Questionnaire-Telegram-Bot.git

```

2\. Set up a Telegram Bot:

   - Create a new bot using the BotFather on Telegram to obtain the bot token.

   - Set the bot token in the configuration file.

3\. Install the required dependencies using pip:

```bash

cd Questionnaire-Telegram-Bot

pip install telebot openai

```

4\. Configure the bot's settings in the configuration file:

   - Specify the criteria for rating user responses.

   - Set the desired options for generating sample answers.

5\. Start the bot by running the main script:

```bash

python bot.py

```

The Questionnaire Telegram Bot is now running and ready to be used.

## Contributing

Contributions to the Questionnaire Telegram Bot are welcome! If you have any suggestions, bug reports, or feature requests, feel free to submit them as issues or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code in accordance with the terms of the license.

## Acknowledgements

The Questionnaire Telegram Bot utilizes ChatGPT, an advanced language model developed by Open

AI, to provide sample answers and evaluate user responses.

Special thanks to the developers of ChatGPT and the Telegram Bot API for their contributions.
