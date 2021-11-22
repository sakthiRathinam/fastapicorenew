-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-22';
ALTER TABLE "subreports" ADD "report_name" VARCHAR(1200);
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-20';
ALTER TABLE "subreports" DROP COLUMN "report_name";
