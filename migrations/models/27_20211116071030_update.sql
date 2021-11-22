-- upgrade --
ALTER TABLE "presmedicines" ADD "type" VARCHAR(13) NOT NULL  DEFAULT 'Capsules';
-- downgrade --
ALTER TABLE "presmedicines" DROP COLUMN "type";
