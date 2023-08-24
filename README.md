[Getting Started](#getting-started)


Welcome to the documentation for the Telegram Expense Management Bot, a powerful tool designed to help users efficiently manage personal expenses, categorize transactions, and gain insights through visualizations. This document will provide you with an overview of the project's functionality, initialization process, project architecture, and how to use the bot effectively.

## Table of Contents

- [Introduction](#introduction) 
- [Getting Started](#getting-started)  
- [Project Architecture and Class Relationships](#project-architecture-and-class-relationships) 
- [Way of Use](#way-of-use) 
- [Contributing](#contributing) 

## Introduction

The Telegram Expense Management Bot offers the following core functionalities:

- **Expense Tracking:** Users can add and categorize their personal expenses through interactions with the bot.
- **Data Visualization:** The bot generates insightful charts and tables for users to visualize their expenses and spending patterns.
- **Multi-User Support:** The bot efficiently manages interactions with multiple users simultaneously, each identified by their unique `chatID`.

## [Getting Started](getting-started)

To initialize the project, follow these steps:

1. Clone the repository to your local machine.

   ```
   git clone https://github.com/cmd69/teleBot.git
   ```

3. Install the required dependencies using `pip install -r requirements.txt`.
4. Set Up Telegram Bot API: Obtain a Telegram Bot API token by creating a new bot using the [BotFather](https://core.telegram.org/bots#botfather). Make sure to enable the necessary permissions for the bot.
5. Rename the `.env.example` file to `.env` in the root directory.
6. Open the `.env` file and add your Telegram Bot token and other configuration details.
7. Start the bot with `python3 telebot.py`

## Way of Use

1. Start a chat with the Telegram Expense Management Bot with the command `/start`.
2. Follow the menu to add your expenses, categorize them, and provide relevant details.
3. Interact with the bot's menus and commands to view charts and tables showcasing your spending habits.

## Project Architecture and Class Relationships

The project is organized into several key modules:

1. **Managers:** Responsible for managing various aspects of the application, including user management, database operations, and data handling.
2. **Generators:** Responsible for generating interactive components like keyboards and charts for the user interface.
3. **Handlers:** Manage user interactions and implement various functionalities of the bot.
4. **`telebot.py`:** The main entry point that sets up the bot, initializes managers and generators, and starts polling for updates.
5. **`streamlit_app.py`:** Runs the Streamlit application for data visualization using the ChartsGenerator class.
6. **`bot_setup.py`:** Handles loading settings and initializing the bot, dispatcher, managers, and generators.

The components interact as follows:

- The main `telebot.py` initializes the bot and creates unique instances of the `DBManager` for each user.
- `DBManager` orchestrates interactions with the user's data, utilizing `JsonManager` and `SheetsManager`.
- `JsonManager` and `SheetsManager` rely on the `UsersManager` instance to access user-specific data.
- `KeyboardsGenerator` creates interactive keyboards for user interactions.
- `handlers` module handles various user interactions using managers, generators, and other components.
- `streamlit_app.py` retrieves data using the `DBManager` and generates charts through the `ChartsGenerator`.
## Contributing

We welcome contributions from the community! If you're interested in improving the bot, feel free to submit pull requests or open issues.

---

Thank you for using the Telegram Expense Management Bot. If you encounter any issues or have questions, please don't hesitate to contact us or open an issue in the repository.
