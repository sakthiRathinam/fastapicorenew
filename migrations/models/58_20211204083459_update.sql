-- upgrade --
ALTER TABLE "useraddress" ADD "category" VARCHAR(6) NOT NULL  DEFAULT 'Home';
-- downgrade --
ALTER TABLE "useraddress" DROP COLUMN "category";
