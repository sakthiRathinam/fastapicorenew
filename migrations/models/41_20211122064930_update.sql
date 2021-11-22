-- upgrade --
CREATE TABLE IF NOT EXISTS "clinicreports" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(1000) NOT NULL UNIQUE,
    "active" BOOL NOT NULL  DEFAULT True,
    "price" INT NOT NULL  DEFAULT 0,
    "general_report_id" INT NOT NULL REFERENCES "medicalreports" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "clinicreports";
