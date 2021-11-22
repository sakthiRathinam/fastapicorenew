-- upgrade --
ALTER TABLE "subreports" DROP COLUMN "report_id";
-- downgrade --
ALTER TABLE "subreports" ADD "report_id" INT NOT NULL;
ALTER TABLE "subreports" ADD CONSTRAINT "fk_subrepor_medicalr_ddd7e6e8" FOREIGN KEY ("report_id") REFERENCES "medicalreports" ("id") ON DELETE CASCADE;
