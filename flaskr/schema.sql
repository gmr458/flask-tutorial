DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `post`;

CREATE TABLE IF NOT EXISTS `user` (
    `id`       int          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` varchar(30)  NOT NULL UNIQUE,
    `password` varchar(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS `post` (
    `id`        int          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `author_id` int          NOT NULL,
    `title`     varchar(30)  NOT NULL,
    `body`      varchar(300) NOT NULL,
    `created`   timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY `author_id` (`author_id`)
);
