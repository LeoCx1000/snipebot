
-- in current implementation this holds prefix disable status.
-- not sure if this will be needed at all.
CREATE TABLE IF NOT EXISTS guilds (
    guild_id                BIGINT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS users (
    user_id                 BIGINT PRIMARY KEY,
    opted_out               BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS delete_snipe (
    id                      BIGSERIAL PRIMARY KEY,
    user_id                 BIGINT NOT NULL,
    channel_id              BIGINT NOT NULL,
    guild_id                BIGINT NOT NULL,
    content                 TEXT NOT NULL DEFAULT '',
    timestamp               TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    referenced_message_id   BIGINT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS deleted_message_attachments (
    id                      BIGSERIAL PRIMARY KEY,
    delete_snipe_id         BIGINT REFERENCES delete_snipe(id) ON DELETE CASCADE,
    filename                TEXT NOT NULL,
    proxy_url               TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS deleted_message_stickers (
    id                      BIGSERIAL PRIMARY KEY,
    delete_snipe_id         BIGINT REFERENCES delete_snipe(id) ON DELETE CASCADE,
    name                    TEXT NOT NULL,
    url                     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS edit_snipe (
    id                      BIGSERIAL PRIMARY KEY,
    user_id                 BIGINT NOT NULL,
    message_id              BIGINT NOT NULL,
    channel_id              BIGINT NOT NULL,
    guild_id                BIGINT NOT NULL,
    before_content          TEXT NOT NULL DEFAULT '',
    after_content           TEXT NOT NULL DEFAULT '',
    timestamp               TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS edited_message_attachment (
    id                      BIGSERIAL PRIMARY KEY,
    delete_snipe_id         BIGINT REFERENCES delete_snipe(id) ON DELETE CASCADE,
    filename                TEXT NOT NULL,
    proxy_url               TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reaction_snipe (
    id                      BIGSERIAL PRIMARY KEY,
    user_id                 BIGINT NOT NULL,
    message_id              BIGINT NOT NULL,
    channel_id              BIGINT NOT NULL,
    guild_id                BIGINT NOT NULL,
    is_custom_emoji         BOOLEAN NOT NULL,
    custom_emoji_name       TEXT DEFAULT NULL,
    emoji                   TEXT NOT NULL, -- either the name of the emoji, or the url to a custom emoji.
    timestamp               TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS error_log (
    id                      BIGSERIAL PRIMARY KEY,
    item                    TEXT NOT NULL DEFAULT '',
    traceback               TEXT NOT NULL,
    timestamp               TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
