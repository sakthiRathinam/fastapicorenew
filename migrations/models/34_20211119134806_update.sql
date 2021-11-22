-- upgrade --
ALTER TABLE "user" ADD "is_child" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "user" DROP COLUMN "is_child";
