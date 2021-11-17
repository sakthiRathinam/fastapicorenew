-- upgrade --

ALTER TABLE "prescriptiontemplates" DROP COLUMN "clinic_id";
-- downgrade --
ALTER TABLE "prescriptiontemplates" ADD "clinic_id" INT;
ALTER TABLE "prescriptiontemplates" ADD CONSTRAINT "fk_prescrip_clinic_a159d7dd" FOREIGN KEY ("clinic_id") REFERENCES "clinic" ("id") ON DELETE CASCADE;
