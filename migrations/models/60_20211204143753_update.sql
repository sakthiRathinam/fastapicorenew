-- upgrade --
CREATE TABLE IF NOT EXISTS "cart" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_received" BOOL NOT NULL  DEFAULT False,
    "task_id" VARCHAR(300),
    "order_id" VARCHAR(300),
    "medical_store_id" INT REFERENCES "clinic" ("id") ON DELETE CASCADE
);;
DROP TABLE IF EXISTS "cartmedicines";
-- downgrade --
DROP TABLE IF EXISTS "cart";
