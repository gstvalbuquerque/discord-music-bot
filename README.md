## Discord Music Bot

This is a simple Discord music bot written in Python using the discord.py library. The bot can join a voice channel, play music from YouTube, stop the music, and skip to the next song. It utilizes the `yt_dlp` library to download the audio from YouTube videos.

### Prerequisites

Before running the bot, make sure you have the following prerequisites:

- Python 3.7 or higher
- discord.py library (`pip install discord.py`)
- yt_dlp library (`pip install yt_dlp`)

### Getting Started

1. Clone the repository or download the source code files.

2. Install the required libraries by running the following command:

   ```shell
   pip install -r requirements.txt
   ```

3. Create a new Discord bot and obtain the bot token. You can follow the Discord Developer Portal documentation on how to create a bot and obtain the token.

4. Set the Discord token as an environment variable with the name `DISCORD_TOKEN`. You can either set it in your system environment variables or create a `.env` file in the project directory and add the following line:

   ```
   DISCORD_TOKEN=your_token_here
   ```

5. Run the bot script using the following command:

   ```shell
   python bot.py
   ```

### Usage

The bot responds to the following commands:

- `!join`: The bot joins the voice channel the user is currently connected to.

- `!play <song_name_or_url>`: The bot plays the specified song from YouTube. You can provide either the name of the song or the YouTube URL.

- `!stop`: The bot stops the currently playing music and disconnects from the voice channel.

- `!skip`: The bot skips the currently playing song and moves to the next song in the queue.

### Contributing

Contributions to the project are welcome. If you find any issues or want to add new features, feel free to open a pull request.

### License

This project is licensed under the [MIT License](LICENSE).
