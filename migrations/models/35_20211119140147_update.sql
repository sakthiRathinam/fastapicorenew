-- upgrade --
CREATE INDEX "idx_user_mobile_319e6a" ON "user" ("mobile");
-- downgrade --
DROP INDEX "idx_user_mobile_319e6a";
