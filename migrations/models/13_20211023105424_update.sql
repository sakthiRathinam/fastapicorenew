-- upgrade --
ALTER TABLE "user" ADD "sex" VARCHAR(11) NOT NULL  DEFAULT 'Male';
ALTER TABLE "medicalaccepted" ALTER COLUMN "status" TYPE VARCHAR(16) USING "status"::VARCHAR(16);
-- downgrade --
ALTER TABLE "user" DROP COLUMN "sex";
ALTER TABLE "medicalaccepted" ALTER COLUMN "status" TYPE VARCHAR(16) USING "status"::VARCHAR(16);
