-- upgrade --
ALTER TABLE "presmedicines" ADD "medicine_name" VARCHAR(300);
-- downgrade --
ALTER TABLE "presmedicines" DROP COLUMN "medicine_name";
