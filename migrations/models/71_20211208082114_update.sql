-- upgrade --
ALTER TABLE "cart" ADD "expected_delivery" VARCHAR(500);
-- downgrade --
ALTER TABLE "cart" DROP COLUMN "expected_delivery";
