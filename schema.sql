PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS articles;

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    slug TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS tags;

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT NOT NULL
);

DROP TABLE IF EXISTS articles_tags;

CREATE TABLE articles_tags (
    tag_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    PRIMARY KEY(tag_id, article_id),
    FOREIGN KEY(tag_id) REFERENCES tags(id),
    FOREIGN KEY(article_id) REFERENCES articles(id)
);


