# bible-bot
> A Discord bot for Bible verses

> [!WARNING]
> This project is still in early development. Features may be broken/missing.

## Commands
- `/books` List the available books
- `/citation [book] [chapter] [verse]` Read a verse from the specified book

By default, the bot uses the [Berean Standard Bible](https://bereanbible.com/) from the [Hello AO Free Use Bible API](https://bible.helloao.org/docs/)
<details>
<summary>Attribution Notice</summary>
<br>
The Holy Bible, Berean Standard Bible, BSB is produced in cooperation with 
<a href="https://biblehub.com/" target="_blank">Bible Hub</a>, 
<a href="https://discoverybible.com/" target="_blank">Discovery Bible</a>, 
<a href="https://openbible.com/" target="_blank">OpenBible.com</a>, 
and the Berean Bible Translation Committee. This text of God's Word has been 
<a href="https://creativecommons.org/publicdomain/zero/1.0/" target="_blank">dedicated to the public domain</a>.
</details>

## Setup
Use [this link](https://discord.com/oauth2/authorize?client_id=1355640740549759127) to add the bot to your server.

### Self-hosting
1. Clone the bot source code and change into the source directory.
```bash
git clone https://github.com/youkononame/bible-bot/
cd bible-bot
```
2. Visit the [Discord Developer Portal](https://discordapp.com/developers/applications/) and create a new application.
3. Visit the **Bot** tab of your application and select **Reset Token**.
4. Copy this token into a .env file like below:
```
BOT_TOKEN="Your token here"
```
5. Visit the **Installation** tab of your application and select the **Guild Install** installation context and the **bot** scope.
6. Enable the **Send Messages** and **Send Messages in Threads** permissions.
7. Use the install link from your application page to add your bot user to your server.
8. Run the commands below to start the bot.
```bash
pip install -r requirements.txt
cd src
python3 bot.py
```

## License
> "...freely you have received; freely give.” - St. Mathew 10:8

This project is licensed under the MIT License.

See the [LICENSE](LICENSE.txt) file for more details.