-- upgrade --
ALTER TABLE "useraddress" ADD "landmark" VARCHAR(1200);
ALTER TABLE "useraddress" DROP COLUMN "apartment";
-- downgrade --
ALTER TABLE "useraddress" ADD "apartment" VARCHAR(400);
ALTER TABLE "useraddress" DROP COLUMN "landmark";
