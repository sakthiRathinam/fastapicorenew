-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-11';
ALTER TABLE "appointmentslots" ALTER COLUMN "doctor_id" DROP NOT NULL;
ALTER TABLE "appointments" ALTER COLUMN "doctor_id" DROP NOT NULL;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-10';
ALTER TABLE "appointments" ALTER COLUMN "doctor_id" SET NOT NULL;
ALTER TABLE "appointmentslots" ALTER COLUMN "doctor_id" SET NOT NULL;
