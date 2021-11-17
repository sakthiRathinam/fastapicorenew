-- upgrade --
ALTER TABLE "user" ADD "health_issues" varchar(3000)[];
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-12';
-- downgrade --
ALTER TABLE "user" DROP COLUMN "health_issues";
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-11';
