DROP DATABASE IF EXISTS alignpos;
CREATE DATABASE alignpos;
USE alignpos;


CREATE TABLE `tabBranch` (
	`branch_id` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`branch_name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`current_date` DATETIME(6) NULL DEFAULT NULL,
	`day_open` int(1) DEFAULT 0,
	`settings` JSON CHECK (JSON_VALID(settings)),
	`name` VARCHAR(140) GENERATED ALWAYS AS (`branch_id`) VIRTUAL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`branch_id`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabTerminal` (
	`terminal_id` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`branch_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`enabled` int(1) DEFAULT 0,
	`current_user` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`name` VARCHAR(140) GENERATED ALWAYS AS (`terminal_id`) VIRTUAL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`terminal_id`) USING BTREE
	CONSTRAINT `FK_tabTerminal_tabBranch` FOREIGN KEY (`branch_id`) REFERENCES `alignpos`.`tabTerminal` (`branch_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabFavorite_Item` (
	`item_code` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`name` VARCHAR(140) GENERATED ALWAYS AS (`item_code`) VIRTUAL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`item_code`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabFast_Item` (
	`item_code` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`name` VARCHAR(140) GENERATED ALWAYS AS (`item_code`) VIRTUAL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`item_code`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabCustomer` (
	`customer_id` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`customer_name` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`customer_type` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`customer_group` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`address` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`mobile_number` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`loyalty_points` INT(6) NULL DEFAULT NULL,
	`name` VARCHAR(140) GENERATED ALWAYS AS (`customer_id`) VIRTUAL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`customer_id`) USING BTREE,
	UNIQUE INDEX `Index customer_id` (`customer_id`) USING BTREE,
	UNIQUE INDEX `Index mobile_number` (`mobile_number`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabItem` (
	`item_code` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`item_name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`item_group` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`barcode` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`uom` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`stock` DECIMAL(18,6) NULL DEFAULT NULL,
	`standard_selling_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`maximum_retail_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`cgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`bundle` INT(1) NULL DEFAULT NULL,
	`name` VARCHAR(140) GENERATED ALWAYS AS (`item_code`) VIRTUAL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`item_code`) USING BTREE
	UNIQUE INDEX `Index item_code` (`item_code`) USING BTREE,
	UNIQUE INDEX `Index barcode` (`barcode`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabInvoice` (
	`draft_invoice_number` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`final_invoice_number` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`posting_date` DATETIME(6) NULL DEFAULT NULL,
	`customer_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`cgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`total_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`discount_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`invoice_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`exchange_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`exchange_reference` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`redeemed_points` INT(6) NULL DEFAULT NULL,
	`redeemed_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`cash_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`other_payment_mode` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`other_payment_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`other_payment_reference` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`cash_return` DECIMAL(18,6) NULL DEFAULT NULL,
	`paid_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`home_delivery` INT(1) NULL DEFAULT NULL,
	`branch_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`terminal_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`approved_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`name` VARCHAR(140) DEFAULT NULL AS (`draft_invoice_number`) virtual COLLATE 'utf8_general_ci',
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`draft_invoice_number`) USING BTREE,
	INDEX `FK_tabInvoice_tabCustomer` (`customer_id`) USING BTREE,
	INDEX `FK_tabInvoice_tabBranch` (`branch_id`) USING BTREE,
	INDEX `FK_tabInvoice_tabTerminal` (`terminal_id`) USING BTREE,
	CONSTRAINT `FK_tabInvoice_tabBranch` FOREIGN KEY (`branch_id`) REFERENCES `alignpos`.`tabBranch` (`branch_id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_tabInvoice_tabCustomer` FOREIGN KEY (`customer_id`) REFERENCES `alignpos`.`tabCustomer` (`customer_id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_tabInvoice_tabTerminal` FOREIGN KEY (`terminal_id`) REFERENCES `alignpos`.`tabTerminal` (`terminal_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabInvoice_Item` (
	`invoice_item_id` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`draft_invoice_number` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`item_code` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`qty` DECIMAL(18,6) NULL DEFAULT NULL,
	`standard_selling_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`applied_selling_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`item_discount_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`selling_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`cgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`cgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`approved_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`name` VARCHAR(140) DEFAULT NULL AS (`invoice_item_id`) virtual COLLATE 'utf8_general_ci',
	`parent` VARCHAR(140) DEFAULT NULL AS (`draft_invoice_number`) virtual COLLATE 'utf8_general_ci',
	PRIMARY KEY (`invoice_item_id`) USING BTREE,
	INDEX `FK_tabInvoice_Item_tabInvoice` (`draft_invoice_number`) USING BTREE,
	INDEX `FK_tabInvoice_Item_tabItem` (`item_code`) USING BTREE,
	CONSTRAINT `FK_tabInvoice_Item_tabInvoice` FOREIGN KEY (`draft_invoice_number`) REFERENCES `alignpos`.`tabInvoice` (`draft_invoice_number`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_tabInvoice_Item_tabItem` FOREIGN KEY (`item_code`) REFERENCES `alignpos`.`tabItem` (`item_code`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `tabExchange` (
	`name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`customer` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`invoice_number` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`exchange_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`name`) USING BTREE,
	INDEX `FK_tabExchange_tabCustomer` (`customer`) USING BTREE,
	CONSTRAINT `FK_tabExchange_tabCustomer` FOREIGN KEY (`customer`) REFERENCES `alignpos`.`tabCustomer` (`name`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabEstimate` (
	`name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`estimate_number` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`posting_date` DATETIME(6) NULL DEFAULT NULL,
	`customer` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`cgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`total_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`discount_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`estimate_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`branch_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`terminal_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`approved_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`name`) USING BTREE,
	INDEX `FK_tabEstimate_tabCustomer` (`customer`) USING BTREE,
	CONSTRAINT `FK_tabEstimate_tabCustomer` FOREIGN KEY (`customer`) REFERENCES `alignpos`.`tabCustomer` (`name`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

CREATE TABLE `tabEstimate_Item` (
	`name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`parent` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`item` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`qty` DECIMAL(18,6) NULL DEFAULT NULL,
	`standard_selling_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`applied_selling_price` DECIMAL(18,6) NULL DEFAULT NULL,
	`item_discount_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`selling_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`cgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`cgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`sgst_tax_rate` DECIMAL(18,6) NULL DEFAULT NULL,
	`approved_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`name`) USING BTREE,
	INDEX `FK_tabEstimate_Item_tabItem` (`item`) USING BTREE,
	INDEX `FK_tabEstimate_Item_tabInvoice` (`parent`) USING BTREE,
	CONSTRAINT `FK_tabEstimate_Item_tabInvoice` FOREIGN KEY (`parent`) REFERENCES `alignpos`.`tabEstimate` (`name`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_tabEstimate_Item_tabItem` FOREIGN KEY (`item`) REFERENCES `alignpos`.`tabItem` (`name`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `tabDenomination` (
	`denomination_name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`cash_value` DECIMAL(18,6) NULL DEFAULT NULL,
	`sort_order` INT(1) NULL DEFAULT NULL,
	`name` VARCHAR(140) DEFAULT NULL AS (`denomination_name`) virtual COLLATE 'utf8_general_ci',
	PRIMARY KEY (`denomination_name`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `tabCash_Transaction` (
	`cash_transaction_number` VARCHAR(100) NOT NULL COLLATE 'utf8_general_ci',
	`transaction_type` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`transaction_context` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`transaction_reference` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`transaction_date` DATETIME(6) NULL DEFAULT NULL,
	`posting_date` DATETIME(6) NULL DEFAULT NULL,
	`receipt_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`payment_amount` DECIMAL(18,6) NULL DEFAULT NULL,
	`party_type` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`customer_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`branch_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`terminal_id` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`approved_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`name` VARCHAR(140) AS (`cash_transaction_number`),
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`cash_transaction_number`) USING BTREE,
	INDEX `FK_tabCash_Transaction_tabCustomer` (`customer_id`) USING BTREE,
	INDEX `FK_tabCash_Transaction_tabBranch` (`branch_id`) USING BTREE,
	INDEX `FK_tabCash_Transaction_tabTerminal` (`terminal_id`) USING BTREE,
	CONSTRAINT `FK_tabCash_Transaction_tabBranch` FOREIGN KEY (`branch_id`) REFERENCES `alignpos`.`tabBranch` (`branch_id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_tabCash_Transaction_tabCustomer` FOREIGN KEY (`customer_id`) REFERENCES `alignpos`.`tabCustomer` (`customer_id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_tabCash_Transaction_tabTerminal` FOREIGN KEY (`terminal_id`) REFERENCES `alignpos`.`tabTerminal` (`terminal_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `tabCash_Transaction_Denomination` (
	`cash_transaction_denomination_id` VARCHAR(100) NOT NULL COLLATE 'utf8_general_ci',
	`cash_transaction_number` VARCHAR(100) NOT NULL COLLATE 'utf8_general_ci',
	`denomination_name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`count` INT(1) NULL DEFAULT '0',
	`name` VARCHAR(140) AS (`cash_transaction_denomination_id`),
	`parent` VARCHAR(140) AS (`cash_transaction_number`),
	PRIMARY KEY (`cash_transaction_denomination_id`) USING BTREE,
	INDEX `FK_tabCash_Transaction_Denomination_tabCash_Transaction` (`cash_transaction_number`) USING BTREE,
	INDEX `FK_tabCash_Transaction_Denomination_tabDenomination` (`denomination_name`) USING BTREE,
	CONSTRAINT `FK_tabCash_Transaction_Denomination_tabCash_Transaction` FOREIGN KEY (`cash_transaction_number`) REFERENCES `alignpos`.`tabCash_Transaction` (`cash_transaction_number`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_tabCash_Transaction_Denomination_tabDenomination` FOREIGN KEY (`denomination_name`) REFERENCES `alignpos`.`tabDenomination` (`denomination_name`) ON UPDATE RESTRICT ON DELETE RESTRICT
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


CREATE TABLE `tabUser` (
	`user_name` VARCHAR(140) NOT NULL COLLATE 'utf8_general_ci',
	`full_name` varchar(255) DEFAULT NULL,
	`passwd` blob,
	`role` varchar(255) DEFAULT NULL,
	`enabled` int(1) DEFAULT 1,
	`name` VARCHAR(140) GENERATED ALWAYS AS (`user_name`) VIRTUAL,
	`creation` DATETIME(6) NULL DEFAULT NULL,
	`modified` DATETIME(6) NULL DEFAULT NULL,
	`modified_by` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`owner` VARCHAR(140) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`user_name`) USING BTREE
) ENGINE=InnoDB
;

insert into tabUser (name, full_name, passwd, role, enabled, creation, owner) values ('administrator', 'administrator', ENCODE('welcome', 'secret'), 'Alignpos Administrator', 1, now(), 'administrator');
insert into tabSequence (name) values ('DRAFT_INVOICE_NUMBER');
insert into tabSequence (name, prefix) values ('TAX_INVOICE_NUMBER', 'SINV-');
insert into tabSequence (name, prefix) values ('ESTIMATE_NUMBER', 'EST-');
insert into tabSequence (name, prefix) values ('ORDER_NUMBER', 'ORD-');
insert into tabSequence (name, prefix) values ('CASH_NUMBER', 'CASH-');
insert into tabDenomination (name, cash_value, sort_order) values ('2000 Notes', 2000.00, 1);
insert into tabDenomination (name, cash_value, sort_order) values ('500 Notes', 500.00, 2);
insert into tabDenomination (name, cash_value, sort_order) values ('200 Notes', 200.00, 3);
insert into tabDenomination (name, cash_value, sort_order) values ('100 Notes', 100.00, 4);
insert into tabDenomination (name, cash_value, sort_order) values ('50 Notes', 50.00, 5);
insert into tabDenomination (name, cash_value, sort_order) values ('20 Notes', 20.00, 6);
insert into tabDenomination (name, cash_value, sort_order) values ('10 Notes', 10.00, 7);
insert into tabDenomination (name, cash_value, sort_order) values ('10 Coins', 10.00, 8);
insert into tabDenomination (name, cash_value, sort_order) values ('5 Coins', 5.00, 9);
insert into tabDenomination (name, cash_value, sort_order) values ('2 Coins', 2.00, 10);
insert into tabDenomination (name, cash_value, sort_order) values ('1 Coins', 1.00, 11);
insert into tabDenomination (name, cash_value, sort_order) values ('None', 1.00, 12);
