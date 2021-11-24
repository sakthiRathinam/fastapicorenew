-- upgrade --
ALTER TABLE "subreports" ADD "price" INT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "subreports" DROP COLUMN "price";
