-- upgrade --
ALTER TABLE "prescriptiontemplates" DROP COLUMN "doctor_id";
-- downgrade --
ALTER TABLE "prescriptiontemplates" ADD "doctor_id" INT;
ALTER TABLE "prescriptiontemplates" ADD CONSTRAINT "fk_prescrip_user_37e094ce" FOREIGN KEY ("doctor_id") REFERENCES "user" ("id") ON DELETE CASCADE;
