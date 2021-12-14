-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-07';
ALTER TABLE "cart" ADD "order_status" VARCHAR(9) NOT NULL  DEFAULT 'Pending';
CREATE TABLE IF NOT EXISTS "cartmedicines" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_received" BOOL NOT NULL  DEFAULT False,
    "quantity" INT NOT NULL  DEFAULT 0,
    "medicine_id" INT NOT NULL REFERENCES "medicine" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "cart"."order_status" IS 'Accepted: Accepted\nDeclined: Declined\nPending: Pending\nDelivered: Delivered';-- downgrade --
ALTER TABLE "cart" DROP COLUMN "order_status";
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-04';
DROP TABLE IF EXISTS "cartmedicines";
