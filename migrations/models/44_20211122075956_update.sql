-- upgrade --
ALTER TABLE "subreports" ADD "report_id" INT;
ALTER TABLE "subreports" ADD CONSTRAINT "fk_subrepor_clinicre_e705be28" FOREIGN KEY ("report_id") REFERENCES "clinicreports" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "subreports" DROP CONSTRAINT "fk_subrepor_clinicre_e705be28";
ALTER TABLE "subreports" DROP COLUMN "report_id";
