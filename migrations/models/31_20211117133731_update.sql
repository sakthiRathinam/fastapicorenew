-- upgrade --
ALTER TABLE "prescription" ADD "reason" TEXT;
-- downgrade --
ALTER TABLE "prescription" DROP COLUMN "reason";
