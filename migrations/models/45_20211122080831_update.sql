-- upgrade --
ALTER TABLE "labreports" ADD "total_price" INT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "labreports" DROP COLUMN "total_price";
