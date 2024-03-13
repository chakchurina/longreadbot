# Longread Bot

This project features a Telegram bot designed to assist users in creating Instagram posts, when their content exceeds the platform's text limit for a single post. If the text for a proposed Instagram post is too lengthy and doesn't fit into a post's text block, this bot automatically generates images to be used in a carousel.

## Features

- **Text to Image Conversion:** For Instagram posts longer than 2200 characters, the bot converts the overflow text into images, allowing for carousel posts.
- **Automated Line Breaks:** For shorter texts, the bot intelligently adds line breaks to enhance readability.
- **Language Support:** Initially supporting English and Russian, the bot interacts with users, offering them to choose their preferred language for communication.

## How It Works

1. **Starting a Conversation:** Users initiate interaction by sending a command to the bot within Telegram.
2. **Language Selection:** Users select their preferred language (Russian or English) for the bot's responses.
3. **Submitting Text:** Users send their intended Instagram post text to the bot.
4. **Processing:** The bot processes the text, automatically determining whether to add line breaks or convert the text into one or more images.
5. **Delivery:** The bot then sends the processed text or images back to the user, ready for Instagram posting.

## Getting Started

This project is built with Python, leveraging Telegram's Bot API for interaction and custom rendering scripts for generating images from text.

### Prerequisites

- Python 3.6 or newer.
- A Telegram bot token, obtained through BotFather on Telegram.

### Installation and Setup

1. Clone the repository to your local machine.
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory.
   ```bash
   cd longread-instagram-bot
   ```
3. Install the required dependencies.
   ```bash
   pip install -r requirements.txt
   ```
4. Set the `TELEGRAM_TOKEN` environment variable to your Telegram bot token.
5. Run the bot.
   ```bash
   python run_longread_bot.py
   ```
   
I hope this bot helps you manage your long Instagram posts! Enjoy creating and sharing your content.
