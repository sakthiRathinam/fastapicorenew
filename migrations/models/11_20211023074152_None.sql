-- upgrade --
CREATE TABLE IF NOT EXISTS "clinicverification" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(700) NOT NULL,
    "email" VARCHAR(800),
    "mobile" VARCHAR(20),
    "verified" BOOL NOT NULL  DEFAULT False
);
CREATE INDEX IF NOT EXISTS "idx_clinicverif_name_6af7e7" ON "clinicverification" ("name");
CREATE TABLE IF NOT EXISTS "inventory" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(400) NOT NULL,
    "types" VARCHAR(12) NOT NULL  DEFAULT 'Clinic'
);
COMMENT ON COLUMN "inventory"."types" IS 'Doctor: Doctor\nMedicalStore: MedicalStore\nClinic: Clinic\nLab: Lab';
CREATE TABLE IF NOT EXISTS "permissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "app_name" VARCHAR(500) NOT NULL UNIQUE,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "permission_level" VARCHAR(14) NOT NULL  DEFAULT 'Admin',
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "permissions"."permission_level" IS 'Admin: Admin\nEmp: Emp\nLowPermissions: LowPermissions';
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "email" VARCHAR(100)  UNIQUE,
    "mobile" VARCHAR(15),
    "roles" VARCHAR(13) NOT NULL  DEFAULT 'Patient',
    "password" VARCHAR(100) NOT NULL,
    "first_name" VARCHAR(100) NOT NULL  DEFAULT '',
    "last_name" VARCHAR(100)   DEFAULT '',
    "city" VARCHAR(800)   DEFAULT '',
    "state" VARCHAR(800)   DEFAULT '',
    "country" VARCHAR(800)   DEFAULT '',
    "date_of_birth" DATE NOT NULL  DEFAULT '2021-10-23',
    "date_join" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "address" TEXT,
    "qualifications" varchar(3000)[],
    "specialization" varchar(3000)[],
    "notificationIds" varchar(3000)[],
    "last_login" TIMESTAMPTZ,
    "experience" INT,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_staff" BOOL NOT NULL  DEFAULT False,
    "currently_active" BOOL NOT NULL  DEFAULT False,
    "display_picture" VARCHAR(2000) NOT NULL  DEFAULT '',
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "avatar" VARCHAR(1000),
    "personal_inventory" BOOL NOT NULL  DEFAULT False,
    "created_subs" BOOL NOT NULL  DEFAULT False,
    "inventory_id" INT REFERENCES "inventory" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "user"."roles" IS 'Doctor: Doctor\nPatient: Patient\nRecoponist: Recoponist\nPharmacyOwner: PharmacyOwner\nLabOwner: LabOwner\nAdmin: Admin';
COMMENT ON TABLE "user" IS 'Model user ';
CREATE TABLE IF NOT EXISTS "verification" (
    "link" UUID NOT NULL  PRIMARY KEY,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "verification" IS 'Модель для подтверждения регистрации пользователя';
CREATE TABLE IF NOT EXISTS "clinictimings" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "day" VARCHAR(9) NOT NULL  DEFAULT 'Monday',
    "timings" varchar(3000)[] NOT NULL
);
COMMENT ON COLUMN "clinictimings"."day" IS 'Monday: Monday\nTuesday: Tuesday\nWednesday: Wednesday\nThursday: Thursday\nFriday: Friday\nSaturday: Saturday\nSunday: Sunday';
CREATE TABLE IF NOT EXISTS "cliniczones" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(1000) NOT NULL UNIQUE,
    "active" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "clinic" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(400) NOT NULL,
    "email" VARCHAR(600),
    "mobile" VARCHAR(20),
    "drug_license" VARCHAR(1000),
    "notificationId" VARCHAR(500),
    "address" TEXT,
    "types" VARCHAR(12) NOT NULL  DEFAULT 'Clinic',
    "sub_types" VARCHAR(16)   DEFAULT 'eye',
    "total_ratings" INT NOT NULL  DEFAULT 0,
    "city" VARCHAR(500),
    "state" VARCHAR(500),
    "lat" VARCHAR(500),
    "lang" VARCHAR(500),
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "display_picture" VARCHAR(2000),
    "pincode" VARCHAR(300),
    "gst_percentage" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "discount_percent" INT NOT NULL  DEFAULT 0,
    "gst_no" VARCHAR(1000),
    "clinic_images" varchar(3000)[],
    "created_subs" BOOL NOT NULL  DEFAULT False,
    "inventoryIncluded" BOOL NOT NULL  DEFAULT False,
    "active" BOOL NOT NULL  DEFAULT True,
    "inventory_id" INT REFERENCES "inventory" ("id") ON DELETE CASCADE,
    "zone_id" INT REFERENCES "cliniczones" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_clinic_name_0425f2" ON "clinic" ("name");
COMMENT ON COLUMN "clinic"."types" IS 'MedicalStore: MedicalStore\nClinic: Clinic\nOthers: Others\nLab: Lab';
COMMENT ON COLUMN "clinic"."sub_types" IS 'eye: eye\ndental: dental\ncardiology: cardiology\ndermatology: dermatology\nthroat: throat\nnose: nose\nnormal: normal\ngastroenterology: gastroenterology\nobstetrics: obstetrics\npodiatry: podiatry\nneurology: neurology\nphysicaltherapy: physicaltherapy\nurology: urology\nophthalmology: ophthalmology\noncology: oncology\northopedics: orthopedics\nhomeo: homeo\nvetnary: vetnary';
CREATE TABLE IF NOT EXISTS "appointmentslots" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "slot_time" VARCHAR(900),
    "max_slots" INT NOT NULL  DEFAULT 0,
    "day" VARCHAR(9) NOT NULL  DEFAULT 'All',
    "active" BOOL NOT NULL  DEFAULT True,
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "doctor_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "appointmentslots"."day" IS 'All: All\nMonday: Monday\nTuesday: Tuesday\nWednesday: Wednesday\nThursday: Thursday\nFriday: Friday\nSaturday: Saturday\nSunday: Sunday';
CREATE TABLE IF NOT EXISTS "appointments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "requested_date" DATE,
    "accepted_date" DATE,
    "status" VARCHAR(15) NOT NULL  DEFAULT 'Pending',
    "accepted_slot_id" INT NOT NULL REFERENCES "appointmentslots" ("id") ON DELETE CASCADE,
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "doctor_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "requested_slot_id" INT NOT NULL REFERENCES "appointmentslots" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "appointments"."status" IS 'Requested: Requested\nAccepted: Accepted\nCancelled: Cancelled\nClinicCancelled: ClinicCancelled\nPending: Pending';
CREATE TABLE IF NOT EXISTS "clinicdoctors" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "personal_inventory" BOOL NOT NULL  DEFAULT False,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL  DEFAULT False,
    "owner_access" BOOL NOT NULL  DEFAULT False,
    "doctor_access" BOOL NOT NULL  DEFAULT True,
    "subs" BOOL NOT NULL  DEFAULT False,
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "clinicreceponists" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "starttime_str" VARCHAR(600),
    "endtime_str" VARCHAR(600),
    "types" VARCHAR(12) NOT NULL  DEFAULT 'Clinic',
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "clinicreceponists"."types" IS 'Doctor: Doctor\nMedicalStore: MedicalStore\nClinic: Clinic\nLab: Lab';
CREATE TABLE IF NOT EXISTS "diagonsis" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(1000) NOT NULL UNIQUE,
    "active" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "labowners" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "starttime_str" VARCHAR(600),
    "endtime_str" VARCHAR(600),
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "medicalreports" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(1000) NOT NULL UNIQUE,
    "active" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "medicine" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "max_retial_price" INT NOT NULL  DEFAULT 0,
    "type" VARCHAR(13) NOT NULL  DEFAULT 'Capsules',
    "title" VARCHAR(1000) NOT NULL UNIQUE,
    "brand" VARCHAR(500),
    "active" BOOL NOT NULL  DEFAULT False
);
COMMENT ON COLUMN "medicine"."type" IS 'Liquid: Liquid\nTablet: Tablet\nCapsules: Capsules\nCream: Cream\nPowder: Powder\nLotion: Lotion\nSoap: Soap\nShampoo: Shampoo\nSuspension: Suspension\nSerum: Serum\nOil: Oil\nInhalers: Inhalers\nInjections: Injections\nSuppositories: Suppositories\nSolution: Solution\nOthers: Others';
CREATE TABLE IF NOT EXISTS "pharmacyowners" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "starttime_str" VARCHAR(600),
    "endtime_str" VARCHAR(600),
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "presmedicines" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "create_template" BOOL NOT NULL  DEFAULT False,
    "morning_count" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "afternoon_count" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "invalid_count" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "night_count" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "qty_per_time" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "total_qty" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "command" TEXT,
    "is_drug" BOOL NOT NULL  DEFAULT False,
    "before_food" BOOL NOT NULL  DEFAULT False,
    "is_given" BOOL NOT NULL  DEFAULT False,
    "fromDate" DATE,
    "toDate" DATE,
    "days" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "diagonsis_id" INT NOT NULL REFERENCES "diagonsis" ("id") ON DELETE CASCADE,
    "medicine_id" INT NOT NULL REFERENCES "medicine" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "prescription" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL  DEFAULT True,
    "create_template" BOOL NOT NULL  DEFAULT False,
    "personal_prescription" BOOL NOT NULL  DEFAULT False,
    "rating_taken" BOOL NOT NULL  DEFAULT False,
    "gst_percentage" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "doctor_fees" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "age" INT NOT NULL  DEFAULT 0,
    "next_visit" DATE,
    "contains_drug" BOOL NOT NULL  DEFAULT False,
    "is_template" BOOL NOT NULL  DEFAULT False,
    "clinic_id" INT REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "doctor_id" INT REFERENCES "user" ("id") ON DELETE CASCADE,
    "receponist_id" INT REFERENCES "user" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "prescriptiontemplates" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "command" TEXT,
    "active" BOOL NOT NULL  DEFAULT True,
    "personal" BOOL NOT NULL  DEFAULT False,
    "clinic_id" INT REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "diagonsis_id" INT NOT NULL REFERENCES "diagonsis" ("id") ON DELETE CASCADE,
    "doctor_id" INT REFERENCES "clinic" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "monthlyplans" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "main_subscription" VARCHAR(9) NOT NULL  DEFAULT 'Monthly',
    "amount" INT NOT NULL  DEFAULT 0,
    "discount" INT NOT NULL  DEFAULT 0,
    "discount_percent" DOUBLE PRECISION NOT NULL  DEFAULT 0
);
COMMENT ON COLUMN "monthlyplans"."main_subscription" IS 'Monthly: Monthly\nQuarterly: Quarterly\nYearly: Yearly\nHalfly: Halfly';
CREATE TABLE IF NOT EXISTS "razorpayment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "subscription" VARCHAR(9) NOT NULL  DEFAULT 'Monthly',
    "status" VARCHAR(8) NOT NULL  DEFAULT 'Pending',
    "payment_mode" VARCHAR(4) NOT NULL  DEFAULT 'upi',
    "order_id" VARCHAR(800),
    "is_received" BOOL NOT NULL  DEFAULT False,
    "is_refunded" BOOL NOT NULL  DEFAULT False,
    "amount" INT NOT NULL  DEFAULT 0,
    "subscription_date" DATE,
    "valid_till" DATE,
    "is_cash" BOOL NOT NULL  DEFAULT False,
    "active" BOOL NOT NULL  DEFAULT True,
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "razorpayment"."subscription" IS 'Monthly: Monthly\nQuarterly: Quarterly\nYearly: Yearly\nHalfly: Halfly';
COMMENT ON COLUMN "razorpayment"."status" IS 'Pending: Pending\nSuccess: Success\nFailed: Failed\nRefunded: Refunded';
COMMENT ON COLUMN "razorpayment"."payment_mode" IS 'upi: upi\ncash: cash\ncard: card';
CREATE TABLE IF NOT EXISTS "createuserorder" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "order_status" VARCHAR(9) NOT NULL  DEFAULT 'PENDING',
    "order_mode" VARCHAR(7) NOT NULL  DEFAULT 'Dunzo',
    "user_lat" VARCHAR(600),
    "user_lang" VARCHAR(600),
    "medical_lat" VARCHAR(600),
    "medical_lang" VARCHAR(600),
    "total_price" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "discount_price" INT NOT NULL  DEFAULT 0,
    "accepted_price" INT NOT NULL  DEFAULT 0,
    "medical_store_id" INT REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "prescription_id" INT REFERENCES "prescription" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "createuserorder"."order_status" IS 'FAILED: FAILED\nCOMPLETED: COMPLETED\nACTIVE: ACTIVE\nDELIVERED: DELIVERED\nCANCELLED: CANCELLED\nPENDING: PENDING';
COMMENT ON COLUMN "createuserorder"."order_mode" IS 'Offline: Offline\nZomato: Zomato\nDunzo: Dunzo\nInstore: Instore\nSwiggy: Swiggy';
CREATE TABLE IF NOT EXISTS "dunzoorder" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "to_send" JSONB,
    "current_response" JSONB,
    "task_id" VARCHAR(500),
    "refund_id" VARCHAR(400),
    "order_id" VARCHAR(300),
    "payment_id" VARCHAR(300),
    "is_refunded" BOOL NOT NULL  DEFAULT False,
    "is_delivered" BOOL NOT NULL  DEFAULT False,
    "current_state" VARCHAR(500),
    "is_cancelled" BOOL NOT NULL  DEFAULT False,
    "estimated_price" DOUBLE PRECISION,
    "razor_price" DOUBLE PRECISION,
    "razor_commision" INT,
    "is_received" BOOL NOT NULL  DEFAULT False,
    "amount" INT NOT NULL  DEFAULT 0,
    "payment_status" VARCHAR(7) NOT NULL  DEFAULT 'Pending',
    "dunzo_status" VARCHAR(9) NOT NULL  DEFAULT 'PENDING',
    "payment_method" VARCHAR(12) NOT NULL  DEFAULT 'DUNZO_CREDIT',
    "main_order_id" INT REFERENCES "createuserorder" ("id") ON DELETE CASCADE,
    "medical_store_id" INT REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "dunzoorder"."payment_status" IS 'Pending: Pending\nSuccess: Success\nFailed: Failed';
COMMENT ON COLUMN "dunzoorder"."dunzo_status" IS 'FAILED: FAILED\nCOMPLETED: COMPLETED\nACTIVE: ACTIVE\nDELIVERED: DELIVERED\nCANCELLED: CANCELLED\nPENDING: PENDING';
COMMENT ON COLUMN "dunzoorder"."payment_method" IS 'COD: COD\nDUNZO_CREDIT: DUNZO_CREDIT';
CREATE TABLE IF NOT EXISTS "medicalaccepted" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "accepted_price" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "all_available" BOOL NOT NULL  DEFAULT False,
    "medical_store_id" INT REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "order_id" INT REFERENCES "createuserorder" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ordermedicines" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "quantity" INT NOT NULL  DEFAULT 0,
    "price" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "changed_price" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "is_drug" BOOL NOT NULL  DEFAULT False,
    "medicine_id" INT REFERENCES "medicine" ("id") ON DELETE CASCADE,
    "medicine_time_id" INT REFERENCES "presmedicines" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_permissions" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "permissions_id" INT NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "clinic_clinictimings" (
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE,
    "clinictimings_id" INT NOT NULL REFERENCES "clinictimings" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "doctor_timings" (
    "clinicdoctors_id" INT NOT NULL REFERENCES "clinicdoctors" ("id") ON DELETE CASCADE,
    "clinictimings_id" INT NOT NULL REFERENCES "clinictimings" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "prescription_presmedicines" (
    "prescription_id" INT NOT NULL REFERENCES "prescription" ("id") ON DELETE CASCADE,
    "presmedicines_id" INT NOT NULL REFERENCES "presmedicines" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "prescription_medicalreports" (
    "prescription_id" INT NOT NULL REFERENCES "prescription" ("id") ON DELETE CASCADE,
    "medicalreports_id" INT NOT NULL REFERENCES "medicalreports" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "prescription_diagonsis" (
    "prescription_id" INT NOT NULL REFERENCES "prescription" ("id") ON DELETE CASCADE,
    "diagonsis_id" INT NOT NULL REFERENCES "diagonsis" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "prescriptiontemplates_presmedicines" (
    "prescriptiontemplates_id" INT NOT NULL REFERENCES "prescriptiontemplates" ("id") ON DELETE CASCADE,
    "presmedicines_id" INT NOT NULL REFERENCES "presmedicines" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "event_teams" (
    "createuserorder_id" INT NOT NULL REFERENCES "createuserorder" ("id") ON DELETE CASCADE,
    "ordermedicines_id" INT NOT NULL REFERENCES "ordermedicines" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "createuserorder_clinic" (
    "createuserorder_id" INT NOT NULL REFERENCES "createuserorder" ("id") ON DELETE CASCADE,
    "clinic_id" INT NOT NULL REFERENCES "clinic" ("id") ON DELETE CASCADE
);
