-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-25';
ALTER TABLE "medicine" ADD "updated_type_medical" BOOL NOT NULL  DEFAULT True;
ALTER TABLE "medicine" ADD "updated_inventory" VARCHAR(60) NOT NULL  DEFAULT '';
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-24';
ALTER TABLE "medicine" DROP COLUMN "updated_type_medical";
ALTER TABLE "medicine" DROP COLUMN "updated_inventory";
