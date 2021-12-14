-- upgrade --
ALTER TABLE "issueprescription" DROP COLUMN "date";
-- downgrade --
ALTER TABLE "issueprescription" ADD "date" DATE NOT NULL;
