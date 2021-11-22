-- upgrade --
ALTER TABLE "appointments" ALTER COLUMN "status" TYPE VARCHAR(15) USING "status"::VARCHAR(15);
-- downgrade --
ALTER TABLE "appointments" ALTER COLUMN "status" TYPE VARCHAR(15) USING "status"::VARCHAR(15);
