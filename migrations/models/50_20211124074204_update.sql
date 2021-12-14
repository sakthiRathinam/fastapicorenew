-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-24';
ALTER TABLE "clinic" ADD "mongo_inventory" INT;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-23';
ALTER TABLE "clinic" DROP COLUMN "mongo_inventory";
