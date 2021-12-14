-- upgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-12-01';
ALTER TABLE "monthlyplans" ADD "number_of_months" INT NOT NULL  DEFAULT 1;
ALTER TABLE "monthlyplans" DROP COLUMN "main_subscription";
ALTER TABLE "razorpayment" ADD "number_of_months" INT NOT NULL  DEFAULT 1;
ALTER TABLE "razorpayment" DROP COLUMN "status";
ALTER TABLE "razorpayment" DROP COLUMN "subscription";
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "date_of_birth" SET DEFAULT '2021-11-25';
ALTER TABLE "monthlyplans" ADD "main_subscription" VARCHAR(9) NOT NULL  DEFAULT 'Monthly';
ALTER TABLE "monthlyplans" DROP COLUMN "number_of_months";
ALTER TABLE "razorpayment" ADD "status" VARCHAR(8) NOT NULL  DEFAULT 'Pending';
ALTER TABLE "razorpayment" ADD "subscription" VARCHAR(9) NOT NULL  DEFAULT 'Monthly';
ALTER TABLE "razorpayment" DROP COLUMN "number_of_months";
