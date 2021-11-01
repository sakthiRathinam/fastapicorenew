-- upgrade --
ALTER TABLE "user" ADD "pincode" VARCHAR(800)   DEFAULT '';
-- downgrade --
ALTER TABLE "user" DROP COLUMN "pincode";
