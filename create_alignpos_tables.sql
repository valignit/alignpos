CREATE DATABASE alignpos;

USE alignpos;

CREATE TABLE `tabCustomer` (
	`name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`customer_name` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`customer_type` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`address` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`mobile_number` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`loyalty_points` INT(6) NULL DEFAULT NULL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`name`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabItem` (
	`name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`item_code` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`item_name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`item_group` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`barcode` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`uom` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`stock` DECIMAL(18,6) NULL DEFAULT NULL,
	`selling_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`maximum_retail_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`cgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`name`) USING BTREE,
	UNIQUE INDEX `Index item_code` (`item_code`) USING BTREE,
	UNIQUE INDEX `Index barcode` (`barcode`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabInvoice` (
	`name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`invoice_number` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`posting_date` DATETIME(6) NULL DEFAULT NULL,
	`customer` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`total_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`discount_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`cgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`invoice_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`credit_note_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`credit_note_reference` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`loyalty_points_redeemed` INT(6) NULL DEFAULT NULL,
	`loyalty_redeemed_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`paid_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`home_delivery` INT(1) NULL DEFAULT NULL,
	`terminal_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`approved_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`name`) USING BTREE,
	INDEX `FK_tabInvoice_tabCustomer` (`customer`) USING BTREE,
	CONSTRAINT `FK_tabInvoice_tabCustomer` FOREIGN KEY (`customer`) REFERENCES `alignpos`.`tabCustomer` (`name`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabInvoice Item` (
	`name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`parent` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`item` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`qty` DECIMAL(18,6) NULL DEFAULT NULL,
	`standard_selling_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`applied_selling_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`selling_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`cgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`approved_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`name`) USING BTREE,
	INDEX `FK_tabInvoice Item_tabItem` (`item`) USING BTREE,
	INDEX `FK_tabInvoice Item_tabInvoice` (`parent`) USING BTREE,
	CONSTRAINT `FK_tabInvoice Item_tabInvoice` FOREIGN KEY (`parent`) REFERENCES `alignpos`.`tabInvoice` (`name`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_tabInvoice Item_tabItem` FOREIGN KEY (`item`) REFERENCES `alignpos`.`tabItem` (`name`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabInvoice Payment` (
	`name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`parent` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`mode_of_payment` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`payment_reference_no` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`payment_reference_date` DATE NULL DEFAULT NULL,
	`received_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	PRIMARY KEY (`name`) USING BTREE,
	INDEX `FK_tabInvoice Payment_tabInvoice` (`parent`) USING BTREE,
	CONSTRAINT `FK_tabInvoice Payment_tabInvoice` FOREIGN KEY (`parent`) REFERENCES `alignpos`.`tabInvoice` (`name`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabSequence` (
	`name` VARCHAR(100) NOT NULL COLLATE 'utf8_general_ci',
	`increment` INT(11) NOT NULL DEFAULT '1',
	`min_value` INT(11) NOT NULL DEFAULT '1',
	`max_value` INT(11) NOT NULL DEFAULT '99999999',
	`cur_value` INT(11) NULL DEFAULT '1',
	`cycle` TINYINT(1) NOT NULL DEFAULT '0',
	`value_size` INT(11) NOT NULL DEFAULT '5',
	`prefix` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`name`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

insert into tabSequence (name) values ('REFERENCE_NUMBER');
insert into tabSequence (name, prefix) values ('INVOICE_NUMBER', 'SINV-');
insert into tabSequence (name, prefix) values ('ESTIMATE_NUMBER', 'EST-');
