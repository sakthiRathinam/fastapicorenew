-- upgrade --
ALTER TABLE "cartmedicines" ADD "received" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "cartmedicines" DROP COLUMN "received";
