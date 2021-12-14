-- upgrade --
ALTER TABLE "monthlyplans" ADD "title" VARCHAR(500);
-- downgrade --
ALTER TABLE "monthlyplans" DROP COLUMN "title";
