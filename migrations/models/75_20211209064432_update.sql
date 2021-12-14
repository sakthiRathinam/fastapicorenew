-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-09';
ALTER TABLE "cartsubs" ADD "medicine_type" VARCHAR(13) NOT NULL  DEFAULT 'Capsules';
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-08';
ALTER TABLE "cartsubs" DROP COLUMN "medicine_type";
