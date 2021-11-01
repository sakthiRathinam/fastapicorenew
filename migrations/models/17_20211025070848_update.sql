-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-10-25';
ALTER TABLE "appointments" ALTER COLUMN "accepted_slot_id" DROP NOT NULL;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-10-23';
ALTER TABLE "appointments" ALTER COLUMN "accepted_slot_id" SET NOT NULL;
