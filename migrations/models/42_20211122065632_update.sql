-- upgrade --
ALTER TABLE "clinicreports" ADD "clinic_id" INT;
ALTER TABLE "clinicreports" ADD CONSTRAINT "fk_clinicre_clinic_a69de4dc" FOREIGN KEY ("clinic_id") REFERENCES "clinic" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "clinicreports" DROP CONSTRAINT "fk_clinicre_clinic_a69de4dc";
ALTER TABLE "clinicreports" DROP COLUMN "clinic_id";
