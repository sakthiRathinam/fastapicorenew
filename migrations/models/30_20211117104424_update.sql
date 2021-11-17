-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-17';
ALTER TABLE "presmedicines" ADD "diagonsisName" VARCHAR(1200);
ALTER TABLE "presmedicines" ALTER COLUMN "medicine_name" TYPE VARCHAR(1200) USING "medicine_name"::VARCHAR(1200);
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-16';
ALTER TABLE "presmedicines" DROP COLUMN "diagonsisName";
ALTER TABLE "presmedicines" ALTER COLUMN "medicine_name" TYPE VARCHAR(300) USING "medicine_name"::VARCHAR(300);
