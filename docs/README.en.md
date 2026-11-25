# **Telegram HTML Formatter Bot**

The Telegram bot allows you to quickly and easily convert HTML markup into readable, properly formatted text.

- How It Works
- Installation Guide
- How to Obtain a Bot Token
- User Guide

The Telegram bot runs locally on your PC. Simply install the application, enter your bot token, and click the **Start** button. The bot will then be ready to receive messages and format HTML text!

1. Navigate to the **Releases** section.
2. Download the latest installation package.
3. Run the installer.
4. Specify the installation directory.
5. Enter your Telegram bot token (see the instructions below for details on how to obtain one).

A **bot token** is a unique string of characters that connects your application to the Telegram Bot API. Your token is **secret**.

**Never share your bot token with third parties!** Anyone who obtains your token can gain control of your bot and perform actions on its behalf.

To obtain a bot token:

1. Start a conversation with [@BotFather](https://t.me/BotFather?utm_source=chatgpt.com) on Telegram — the official bot for creating and managing Telegram bots.
2. Send the `/newbot` command.
3. Follow the instructions to specify a name and username for your new bot.
4. Send the `/token` command.
5. Copy the token, which looks like this: ```1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789```

The application window consists of two main sections:

1. **Bot Control Panel**
2. **Event Log**

The **Bot Control Panel** allows you to manage the bot's operating state and **replace its token** if the current one is no longer valid.

The **Event Log** displays timestamps and actions performed by the bot, as well as any errors and exceptions detected by the application.

**The bot will not operate while it is stopped!**

Once the bot is running, open Telegram, start a conversation with the bot you created, and follow the instructions.

When you send HTML-formatted text to the bot, it will return a message in which each supported HTML tag is converted into its corresponding Telegram entity.

The **list of HTML tags supported by Telegram** remains up to date and **is independent of the installed application version**.

_Enjoy using the bot!_