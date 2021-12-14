-- upgrade --
ALTER TABLE "cart" DROP COLUMN "medicine_name";
ALTER TABLE "cartsubs" ADD "medicine_name" VARCHAR(1200);
-- downgrade --
ALTER TABLE "cart" ADD "medicine_name" VARCHAR(1200);
ALTER TABLE "cartsubs" DROP COLUMN "medicine_name";
