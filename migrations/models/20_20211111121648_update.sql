-- upgrade --
ALTER TABLE "user" ALTER COLUMN "roles" TYPE VARCHAR(17) USING "roles"::VARCHAR(17);
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-11';
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "roles" TYPE VARCHAR(13) USING "roles"::VARCHAR(13);
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-10-25';
