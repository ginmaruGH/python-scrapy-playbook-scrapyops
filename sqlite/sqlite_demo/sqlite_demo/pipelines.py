# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3


class SqliteNoDuplicatesPipeline:

    def __init__(self) -> None:

        # Create/Connect to database
        self.con = sqlite3.connect("demo.db")

        # Create cursor, used to execute commands
        self.cur = self.con.cursor()

        # Create quotes table if none exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS quotes(
                text TEXT,
                tags TEXT,
                author TEXT
            )
        """)

    def process_item(self, item, spider):

        # Check to see if text is already in database
        self.cur.execute(
            "select * from quotes where text = ?",
            (item["text"],)
        )
        result = self.cur.fetchone()

        # If it is in DB, create log message
        if result:
            spider.logger.warn(
                "Item already in database: %s" % item["text"]
            )
        # If text isn't in the DB, insert date
        else:
            # Define insert statement
            self.cur.execute(
                """INSERT INTO quotes (text, tags, author) VALUES (?, ?, ?)""",
                (
                    item["text"],
                    str(item["tags"]),
                    item["author"]
                )
            )
            # Execute insert of data into database
            self.con.commit()

        return item
