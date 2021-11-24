-- upgrade --
ALTER TABLE "prescription" ADD "blood_pressure" DOUBLE PRECISION NOT NULL  DEFAULT 0;
ALTER TABLE "prescription" ADD "invalid_till" DATE;
ALTER TABLE "prescription" ADD "blood_sugar" DOUBLE PRECISION NOT NULL  DEFAULT 0;
ALTER TABLE "prescription" ADD "weight" DOUBLE PRECISION NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "prescription" DROP COLUMN "blood_pressure";
ALTER TABLE "prescription" DROP COLUMN "invalid_till";
ALTER TABLE "prescription" DROP COLUMN "blood_sugar";
ALTER TABLE "prescription" DROP COLUMN "weight";
