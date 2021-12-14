-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-08';
ALTER TABLE "clinic" ADD "instore_pickup" BOOL NOT NULL  DEFAULT False;
ALTER TABLE "clinic" ADD "instore_pickup_kms" INT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-07';
ALTER TABLE "clinic" DROP COLUMN "instore_pickup";
ALTER TABLE "clinic" DROP COLUMN "instore_pickup_kms";
