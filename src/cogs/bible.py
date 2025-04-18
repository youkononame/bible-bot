import discord
import requests
from discord.ext import commands
from discord import app_commands
from json import JSONDecodeError

TRANSLATION = "BSB"
INVALID_VERSE_RANGE = "Invalid verse range! Must be number-number (ex. 1-4)."


class PurgeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_books(self):
        return requests.get(
            f"https://bible.helloao.org/api/{TRANSLATION}/books.json"
        ).json()["books"]

    def get_verse(
        self, book, chapter, verse_start: int, verse_end: int
    ) -> tuple[str, bool]:
        try:
            response = requests.get(
                f"https://bible.helloao.org/api/{TRANSLATION}/{book.upper() if len(book) == 3 else book.capitalize()}/{chapter}.json"
            ).json()
        except JSONDecodeError as e:
            return (
                "Invalid book ID or chapter.",
                True,
            )

        verse_str = (
            verse_start
            if verse_end == verse_start
            else str(verse_start) + "-" + str(verse_end)
        )
        message = f"**{response["book"]["name"]}** {chapter}:{verse_str}"

        total_verse_count = response["numberOfVerses"]
        used_verse_count = 0
        started = False
        last_heading = ""

        if verse_end <= total_verse_count:
            for item in response["chapter"]["content"]:
                item_type = item["type"]

                if item_type == "line_break" and started:
                    message += "\n"
                elif item_type == "heading":
                    last_heading = f"\n\n**{"".join(value for value in item["content"])}**{"\n" if not started else ""}"
                    message += last_heading if started else ""

                if item_type != "verse":
                    continue

                if not verse_start <= item["number"] <= verse_end:
                    continue

                if not started:
                    started = True
                    message += last_heading if started else ""

                message += (
                    " ".join(
                        [
                            (
                                value
                                if type(value) == str
                                else (
                                    value["text"]
                                    if type(value) == dict and "text" in value
                                    else ""
                                )
                            )
                            for value in item["content"]
                        ]
                    )
                    + " "
                )
                used_verse_count += 1

                if used_verse_count > verse_end - verse_start:
                    return message, False

        return (
            f"Invalid verse. Verse {verse_str} was requested but {response["book"]["name"]} chapter {chapter} only has {total_verse_count} verses.",
            True,
        )

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
        self, interaction: discord.Interaction, book: str, chapter: int, verse: str
    ) -> None:
        """
        Arguments:
            verse: A singular verse (ex. 19) or a range (ex. 1-4)
        """
        if verse.isnumeric():
            verse_start = int(verse)
            verse_end = verse_start
        else:
            verse = verse.split("-")
            if len(verse) != 2 or "" in verse:
                await interaction.response.send_message(
                    INVALID_VERSE_RANGE, ephemeral=True
                )
                return

            try:
                verse_start = int(verse[0])
                verse_end = int(verse[1])
            except TypeError as e:
                await interaction.response.send_message(
                    INVALID_VERSE_RANGE, ephemeral=True
                )
                return

            if verse_end < verse_start:
                temp = verse_start
                verse_start = verse_end
                verse_end = temp

        verse, ephemeral = self.get_verse(book, chapter, verse_start, verse_end)
        try:
            await interaction.response.send_message(verse, ephemeral=ephemeral)
        except discord.HTTPException as e:
            await interaction.response.send_message(
                "The requested citation is too long. Please quote fewer verses and try again!",
                ephemeral=True,
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PurgeCog(bot))
