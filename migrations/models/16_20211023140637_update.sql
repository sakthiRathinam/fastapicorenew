-- upgrade --
ALTER TABLE "appointments" ADD "reason" TEXT;
-- downgrade --
ALTER TABLE "appointments" DROP COLUMN "reason";
