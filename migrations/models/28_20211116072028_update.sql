-- upgrade --
ALTER TABLE "presmedicines" RENAME COLUMN "type" TO "medicine_type";
-- downgrade --
ALTER TABLE "presmedicines" RENAME COLUMN "medicine_type" TO "type";
