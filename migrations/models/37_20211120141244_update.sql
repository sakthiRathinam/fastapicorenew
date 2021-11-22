-- upgrade --
ALTER TABLE "labreports" ADD "expected_result" TIMESTAMPTZ;
CREATE TABLE "labreports_subreports" ("labreports_id" INT NOT NULL REFERENCES "labreports" ("id") ON DELETE CASCADE,"subreports_id" INT NOT NULL REFERENCES "subreports" ("id") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "labreports_subreports";
ALTER TABLE "labreports" DROP COLUMN "expected_result";
