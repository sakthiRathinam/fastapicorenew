-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-02';
ALTER TABLE "razorpayment" ADD "status" VARCHAR(8) NOT NULL  DEFAULT 'Pending';
ALTER TABLE "razorpayment" DROP COLUMN "number_of_months";
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-01';
ALTER TABLE "razorpayment" ADD "number_of_months" INT NOT NULL  DEFAULT 1;
ALTER TABLE "razorpayment" DROP COLUMN "status";
