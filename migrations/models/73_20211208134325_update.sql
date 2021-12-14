-- upgrade --
ALTER TABLE "cart" ADD "medicine_name" VARCHAR(1200);
ALTER TABLE "cart" ALTER COLUMN "order_status" TYPE VARCHAR(16) USING "order_status"::VARCHAR(16);
-- downgrade --
ALTER TABLE "cart" DROP COLUMN "medicine_name";
ALTER TABLE "cart" ALTER COLUMN "order_status" TYPE VARCHAR(9) USING "order_status"::VARCHAR(9);
