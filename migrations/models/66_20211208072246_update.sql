-- upgrade --
ALTER TABLE "cart" ADD "total_price" INT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "cart" DROP COLUMN "total_price";
