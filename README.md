# Expense Tracker Telegram Bot

Welcome to the Expense Tracker Telegram Bot repository! This project aims to provide a simple and convenient way to keep track of your expenses, allowing you to classify them by category and subcategory. It also integrates with Google Sheets to provide detailed charts and visualizations of your expenses.

## Table of Contents
- [Introduction](#introduction)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Expense Tracker Telegram Bot helps you manage your personal expenses efficiently. With this bot, you can easily add your expenses, categorize them based on predefined categories and subcategories, and view insightful charts for better expense analysis.

Key features of the Expense Tracker Telegram Bot include:
- **Expense Tracking**: Add and manage your expenses seamlessly within the Telegram app.
- **Categorization**: Classify your expenses by selecting from a predefined set of categories and subcategories.
- **Integration with Google Sheets**: Connect the bot to your Google Sheets account to generate charts and track your expenses over time.

## How It Works

1. **Start the Bot**: Start a conversation with the Expense Tracker Telegram Bot by searching for it in the Telegram app.
2. **Register**: Register your account with the bot to access all its features.
3. **Add Expenses**: Use the bot's commands to add your expenses, providing details such as amount, date, category, and subcategory.
4. **Categorize Expenses**: Choose the appropriate category and subcategory for each expense to facilitate better expense analysis.
5. **View Expense Charts**: Connect your Google Sheets account to the bot to generate charts and visualizations of your expenses.
6. **Analyze and Track**: Analyze your expenses using the charts and track your spending habits over time.

## Getting Started

To use the Expense Tracker Telegram Bot, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine:
   ```
   git clone https://github.com/your-username/expense-tracker-telegram-bot.git
   ```

2. **Set Up Telegram Bot API**: Obtain a Telegram Bot API token by creating a new bot using the [BotFather](https://core.telegram.org/bots#botfather). Make sure to enable the necessary permissions for the bot.

3. **Set Up Google Sheets API**: Set up the Google Sheets API and obtain the required credentials to access your Google Sheets account. Refer to the Google Sheets API documentation for detailed instructions.

4. **Configure the Bot**: Configure the necessary environment variables by creating a `.env` file in the project's root directory. Include the following variables:
   ```
   TELEGRAM_TOKEN=your-telegram-bot-token
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

5. **Install Dependencies**: Install the required dependencies by running the following command:
   ```
   npm install
   ```

6. **Start the Bot**: Start the bot by running the following command:
   ```
   npm start
   ```

7. **Interact with the Bot**: Open the Telegram app and search for your bot. Start a conversation and begin tracking your expenses.

## Contributing

Contributions to the Expense Tracker Telegram Bot project are welcome! If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create your branch from `main`.
2. Make your changes, ensuring that the code adheres to the project's coding standards.
3. Write tests to validate the functionality of your changes.
4. Ensure all tests pass successfully.
5. Submit a pull request detailing your changes, the problem you solved, and any relevant information.

