-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-10';
ALTER TABLE "cart" ADD "pincode" VARCHAR(20);
ALTER TABLE "cart" ADD "address" TEXT;
ALTER TABLE "cart" ADD "landmark" VARCHAR(1100);
-- downgrade --
ALTER TABLE "cart" DROP COLUMN "pincode";
ALTER TABLE "cart" DROP COLUMN "address";
ALTER TABLE "cart" DROP COLUMN "landmark";
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-09';
