-- upgrade --
ALTER TABLE "dunzoorder" DROP CONSTRAINT "fk_dunzoord_createus_b98968ad";
ALTER TABLE "dunzoorder" ADD "medical_order_id" INT;
ALTER TABLE "dunzoorder" DROP COLUMN "medical_store_id";
ALTER TABLE "dunzoorder" DROP COLUMN "main_order_id";
ALTER TABLE "dunzoorder" ADD CONSTRAINT "fk_dunzoord_medicala_335ea06b" FOREIGN KEY ("medical_order_id") REFERENCES "medicalaccepted" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "dunzoorder" DROP CONSTRAINT "fk_dunzoord_medicala_335ea06b";
ALTER TABLE "dunzoorder" ADD "medical_store_id" INT;
ALTER TABLE "dunzoorder" ADD "main_order_id" INT;
ALTER TABLE "dunzoorder" DROP COLUMN "medical_order_id";
ALTER TABLE "dunzoorder" ADD CONSTRAINT "fk_dunzoord_clinic_6942db0d" FOREIGN KEY ("medical_store_id") REFERENCES "clinic" ("id") ON DELETE CASCADE;
ALTER TABLE "dunzoorder" ADD CONSTRAINT "fk_dunzoord_createus_b98968ad" FOREIGN KEY ("main_order_id") REFERENCES "createuserorder" ("id") ON DELETE CASCADE;
