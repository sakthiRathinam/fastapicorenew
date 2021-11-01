-- upgrade --
ALTER TABLE "appointmentslots" ADD "date" DATE;
-- downgrade --
ALTER TABLE "appointmentslots" DROP COLUMN "date";
