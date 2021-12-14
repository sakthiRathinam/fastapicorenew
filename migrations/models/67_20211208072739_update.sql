-- upgrade --
ALTER TABLE "cartmedicines" ADD "lat" DOUBLE PRECISION NOT NULL  DEFAULT 0;
ALTER TABLE "cartmedicines" ADD "lang" DOUBLE PRECISION NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "cartmedicines" DROP COLUMN "lat";
ALTER TABLE "cartmedicines" DROP COLUMN "lang";
