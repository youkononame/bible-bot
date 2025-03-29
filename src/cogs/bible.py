import discord
from discord.ext import commands
from discord import app_commands
import requests
from json import JSONDecodeError

TRANSLATION = "BSB"


class PurgeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="books", description="List the available books")
    async def books(
        self,
        interaction: discord.Interaction,
    ):
        message = "**Table of Contents**\n"

        for book in requests.get(
            f"https://bible.helloao.org/api/{TRANSLATION}/books.json"
        ).json()["books"]:
            message += f"- {book["name"]} (*ID: **{book["id"]}***)\n"

        await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(
        name="citation",
        description="Read a verse from the specified book",
    )
    async def citation(
        self, interaction: discord.Interaction, book: str, chapter: int, verse: int
    ):
        try:
            response = requests.get(
                f"https://bible.helloao.org/api/{TRANSLATION}/{book.upper()}/{chapter}.json"
            ).json()
        except JSONDecodeError as e:
            await interaction.response.send_message(
                "Invalid citation! Ensure you are using a valid book ID, and that the chapter/verse you are searching for exists.",
                ephemeral=True,
            )
            return

        message = f"**{response["book"]["name"]}** {chapter}:{verse}\n"

        for item in response["chapter"]["content"]:
            if item["type"] != "verse":
                continue

            if item["number"] != verse:
                continue

            for value in item["content"]:
                if type(value) == str:
                    message += value + " "

            break

        await interaction.response.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(PurgeCog(bot))
