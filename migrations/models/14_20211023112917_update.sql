-- upgrade --
ALTER TABLE "user" ALTER COLUMN "sex" TYPE VARCHAR(11) USING "sex"::VARCHAR(11);
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "sex" TYPE VARCHAR(11) USING "sex"::VARCHAR(11);
