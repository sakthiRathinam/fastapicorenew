-- upgrade --
ALTER TABLE "cart" ADD "prescription_id" INT;
ALTER TABLE "cartmedicines" ADD "price" INT NOT NULL  DEFAULT 0;
ALTER TABLE "cart" ADD CONSTRAINT "fk_cart_prescrip_de687a09" FOREIGN KEY ("prescription_id") REFERENCES "prescription" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "cart" DROP CONSTRAINT "fk_cart_prescrip_de687a09";
ALTER TABLE "cart" DROP COLUMN "prescription_id";
ALTER TABLE "cartmedicines" DROP COLUMN "price";
