-- upgrade --
ALTER TABLE "prescriptiontemplates" ADD "doctor_obj_id" INT;
ALTER TABLE "prescriptiontemplates" ADD CONSTRAINT "fk_prescrip_user_3877e0ec" FOREIGN KEY ("doctor_obj_id") REFERENCES "user" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "prescriptiontemplates" DROP CONSTRAINT "fk_prescrip_user_3877e0ec";
ALTER TABLE "prescriptiontemplates" DROP COLUMN "doctor_obj_id";
