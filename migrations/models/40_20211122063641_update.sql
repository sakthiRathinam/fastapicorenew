-- upgrade --
ALTER TABLE "subreports" ADD "status" VARCHAR(15) NOT NULL  DEFAULT 'Pending';
-- downgrade --
ALTER TABLE "subreports" DROP COLUMN "status";
