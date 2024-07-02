# jtoh-bot
The jtoh-bot for discord allows a set whitelist of users to post tower completions in a specified channel.

The commands are registered slash commands.

In order to post completions, the completion channel must be specified. There is no default.

Additionally, any users who wish to post completions must be on the whitelist. The only people who can add to the whitelist are:
- Server administrators
- Those with the "jtoh-bot whitelist manager" role (easily renamed with a source modification)

The whitelist must be setup every time the bot is re-hosted.

## Hosting
If you wish to host this bot, you'll need to create a file called `.env` in the source directory that looks like so:
- `DISCORD_TOKEN={TOKEN}`

where `TOKEN` is the token for your bot.

## Commands

### Whitelist
- `!whitelist add {user}`
- `!whitelist remove {user}`
- `!whitelist list`

### Add Completion
- `!addcompletion {user} "{tower}" {difficulty} {time}`

### Set Channel
- `!setchannel {channel}`