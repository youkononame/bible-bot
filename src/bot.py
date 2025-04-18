import os
import datetime
from dotenv import load_dotenv, find_dotenv

import discord
from discord.ext import commands
from discord import app_commands


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def load_cogs(self, cogs_directory) -> None:
        if not os.path.isdir(cogs_directory):
            return False

        for filename in os.listdir(cogs_directory):
            if filename.endswith(".py"):
                extension_name = f"cogs.{filename[:-3]}"

                try:
                    await self.load_extension(extension_name)
                except Exception as exception:
                    print(
                        f"Failed to load extension {extension_name}. Error: {exception}"
                    )

        return True

    async def on_ready(self) -> None:
        if not await self.load_cogs("./cogs"):
            print("Cogs directory is missing!")

        try:
            await self.tree.sync()
        except Exception as exception:
            print(f"Failed to sync command tree. Error: {exception}")


bot = Bot(command_prefix="$", intents=discord.Intents.default(), help_command=None)


@bot.tree.error
async def on_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
) -> None:
    match type(error):
        case app_commands.NoPrivateMessage:
            await interaction.response.send_message(
                "This command does not work in private messages.",
                ephemeral=True,
            )
        case app_commands.MissingRole | app_commands.MissingAnyRole:
            await interaction.response.send_message(
                "You are missing the required role(s) to run this command.",
                ephemeral=True,
            )
        case app_commands.MissingPermissions:
            await interaction.response.send_message(
                "You are missing the required permission(s) to run this command.",
                ephemeral=True,
            )
        case app_commands.CommandOnCooldown:
            await interaction.response.send_message(
                f"This command is on cooldown! Try again in {datetime.timedelta(seconds=error.retry_after)}.",
                ephemeral=True,
            )
        case _:
            await interaction.response.send_message(
                "An unknown error occured in the processing of your command.",
                ephemeral=True,
            )

    print(
        f"Error occured in the processing of the command {interaction.command}. Error: {error}"
    )


load_dotenv(find_dotenv())
bot.run(os.getenv("BOT_TOKEN"))
