import sqlite3
import feedparser


def get_image(entry):
    # Try media_thumbnail
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url")

    # Try media_content
    if hasattr(entry, "media_content") and entry.media_content:
        return entry.media_content[0].get("url")

    # Try enclosures
    if hasattr(entry, "enclosures") and entry.enclosures:
        return entry.enclosures[0].get("href")

    return None


def save_rss():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    feed = feedparser.parse("https://lamleygroup.com/feed/")

    for entry in feed.entries:
        image = get_image(entry)
        if not image:
            image = "https: // shopdiecasttalk.com/products/preorder-kaido-house-x-mini-gt-1-64-honda-nsx-kaido-test-car-spec-v1"
        try:
            cursor.execute("""
                INSERT INTO feed (title, link, source, type, date, image)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entry.title,
                entry.link,
                "Lamley",
                "rss",
                entry.published,
                image
            ))
        except:
            pass

    conn.commit()
    conn.close()
