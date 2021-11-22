-- upgrade --
ALTER TABLE "user" ADD "doctor_fees" INT NOT NULL  DEFAULT 0;
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-19';
-- downgrade --
ALTER TABLE "user" DROP COLUMN "doctor_fees";
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-17';
