-- upgrade --
CREATE TABLE IF NOT EXISTS "infractions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "user_id" BIGINT NOT NULL,
    "active" BOOL NOT NULL
);
COMMENT ON COLUMN "infractions"."active" IS 'Whether the infraction is active or not.';
COMMENT ON TABLE "infractions" IS 'Database model for an infraction.';
CREATE TABLE IF NOT EXISTS "users" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "user_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL,
    "discriminator" SMALLINT NOT NULL
);
COMMENT ON COLUMN "users"."user_id" IS 'The ID of this user from Discord.';
COMMENT ON COLUMN "users"."name" IS 'The username of this user from Discord.';
COMMENT ON COLUMN "users"."discriminator" IS 'The discriminator of the user from Discord.';
COMMENT ON TABLE "users" IS 'Database model for a Discord User.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
