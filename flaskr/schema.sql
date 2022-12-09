DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
    `id` INTEGER PRIMARY KEY autoincrement,
    `username` TEXT UNIQUE NOT NULL,
    `password` TEXT NOT NULL
);

CREATE TABLE `post` (
    `id` INTEGER PRIMARY KEY autoincrement,
    `author_id` INTEGER NOT NULL,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `title` TEXT NOT NULL,
    `body` TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES USER (id)
);
