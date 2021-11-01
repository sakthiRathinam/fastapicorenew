-- upgrade --
ALTER TABLE "medicalaccepted" ADD "status" VARCHAR(16) NOT NULL  DEFAULT 'WAITING';
-- downgrade --
ALTER TABLE "medicalaccepted" DROP COLUMN "status";
