-- upgrade --
ALTER TABLE "useraddress" ADD "pincode" VARCHAR(400);
-- downgrade --
ALTER TABLE "useraddress" DROP COLUMN "pincode";
