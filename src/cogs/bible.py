import discord
import requests
from discord.ext import commands
from discord import app_commands
from json import JSONDecodeError

TRANSLATION = "BSB"


class PurgeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_books(self):
        return requests.get(
            f"https://bible.helloao.org/api/{TRANSLATION}/books.json"
        ).json()["books"]

    def get_verse(self, book, chapter, verse) -> tuple[str, bool]:
        try:
            response = requests.get(
                f"https://bible.helloao.org/api/{TRANSLATION}/{book.upper() if len(book) == 3 else book.capitalize()}/{chapter}.json"
            ).json()
        except JSONDecodeError as e:
            return (
                "Invalid citation! Ensure you are using a valid book ID, and that the chapter/verse you are searching for exists.",
                True,
            )

        message = f"**{response["book"]["name"]}** {chapter}:{verse}\n"

        for item in response["chapter"]["content"]:
            if item["type"] != "verse":
                continue

            if item["number"] != verse:
                continue

            for value in item["content"]:
                if type(value) == str:
                    message += value + " "

            return message, False

    @app_commands.command(name="books", description="List the available books")
    async def books(
        self,
        interaction: discord.Interaction,
    ) -> None:
        message = "**Table of Contents**\n"

        for book in self.get_books():
            message += f"- {book["name"]} (*ID: **{book["id"]}***)\n"

        await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(
        name="citation",
        description="Read a verse from the specified book",
    )
    async def citation(
        self, interaction: discord.Interaction, book: str, chapter: int, verse: int
    ) -> None:
        verse, ephemeral = self.get_verse(book, chapter, verse)
        await interaction.response.send_message(verse, ephemeral=ephemeral)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PurgeCog(bot))
