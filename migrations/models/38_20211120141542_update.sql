-- upgrade --
ALTER TABLE "labreports" ADD "active" BOOL NOT NULL  DEFAULT True;
-- downgrade --
ALTER TABLE "labreports" DROP COLUMN "active";
