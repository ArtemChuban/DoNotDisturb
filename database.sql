CREATE TABLE `Users`
(
    `id` Utf8 NOT NULL,
    `password` Utf8,
    `username` Utf8,
    PRIMARY KEY (`id`)
);

CREATE TABLE `Teams`
(
    `id` String NOT NULL,
    `name` Utf8,
    PRIMARY KEY (`id`)
);

CREATE TABLE `Sessions`
(
    `user_id` Utf8 NOT NULL,
    `session` Utf8 NOT NULL,
    PRIMARY KEY (`user_id`, `session`)
);

CREATE TABLE `Membership`
(
    `user_id` Utf8 NOT NULL,
    `team_id` Utf8 NOT NULL,
    `is_admin` Bool,
    `tokens` Uint64,
    PRIMARY KEY (`user_id`, `team_id`)
);

CREATE TABLE `Invites`
(
    `user_id` Utf8 NOT NULL,
    `team_id` Utf8 NOT NULL,
    PRIMARY KEY (`user_id`, `team_id`)
);
