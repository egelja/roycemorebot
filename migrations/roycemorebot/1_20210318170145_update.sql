-- upgrade --
ALTER TABLE "users" ADD "in_guild" BOOL NOT NULL  DEFAULT True;
ALTER TABLE "users" ADD "roles" BIGINT[];
-- downgrade --
ALTER TABLE "users" DROP COLUMN "in_guild";
ALTER TABLE "users" DROP COLUMN "roles";
