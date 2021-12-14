-- upgrade --
ALTER TABLE "cart" ADD "order_mode" VARCHAR(10) NOT NULL  DEFAULT 'Dunzo';
-- downgrade --
ALTER TABLE "cart" DROP COLUMN "order_mode";
