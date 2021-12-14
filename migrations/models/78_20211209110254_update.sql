-- upgrade --
ALTER TABLE "cart" ALTER COLUMN "order_status" TYPE VARCHAR(16) USING "order_status"::VARCHAR(16);
-- downgrade --
ALTER TABLE "cart" ALTER COLUMN "order_status" TYPE VARCHAR(16) USING "order_status"::VARCHAR(16);
