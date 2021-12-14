-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-04';
ALTER TABLE "clinic" ADD "number_of_persons" INT NOT NULL  DEFAULT 0;
ALTER TABLE "clinic" ADD "number_of_ratings" INT NOT NULL  DEFAULT 0;
CREATE TABLE IF NOT EXISTS "paymentoffers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" TEXT,
    "amount" DOUBLE PRECISION NOT NULL  DEFAULT 0
);;
ALTER TABLE "prescription" ADD "ratings_taken" BOOL NOT NULL  DEFAULT False;
CREATE TABLE IF NOT EXISTS "cartmedicines" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_received" BOOL NOT NULL  DEFAULT False,
    "task_id" VARCHAR(300),
    "order_id" VARCHAR(300),
    "medicine_id" INT REFERENCES "medicine" ("id") ON DELETE CASCADE
);-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-02';
ALTER TABLE "clinic" DROP COLUMN "number_of_persons";
ALTER TABLE "clinic" DROP COLUMN "number_of_ratings";
ALTER TABLE "prescription" DROP COLUMN "ratings_taken";
DROP TABLE IF EXISTS "paymentoffers";
DROP TABLE IF EXISTS "cartmedicines";
