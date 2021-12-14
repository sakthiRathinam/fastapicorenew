-- upgrade --
ALTER TABLE "cart" ADD "user_id" INT NOT NULL;
ALTER TABLE "cart" DROP COLUMN "order_id";
ALTER TABLE "cart" DROP COLUMN "task_id";
ALTER TABLE "cartmedicines" ADD "cart_id" INT NOT NULL;
ALTER TABLE "cart" ADD CONSTRAINT "fk_cart_user_a79aa2ff" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;
ALTER TABLE "cartmedicines" ADD CONSTRAINT "fk_cartmedi_cart_98daa7c7" FOREIGN KEY ("cart_id") REFERENCES "cart" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "cartmedicines" DROP CONSTRAINT "fk_cartmedi_cart_98daa7c7";
ALTER TABLE "cart" DROP CONSTRAINT "fk_cart_user_a79aa2ff";
ALTER TABLE "cart" ADD "order_id" VARCHAR(300);
ALTER TABLE "cart" ADD "task_id" VARCHAR(300);
ALTER TABLE "cart" DROP COLUMN "user_id";
ALTER TABLE "cartmedicines" DROP COLUMN "cart_id";
