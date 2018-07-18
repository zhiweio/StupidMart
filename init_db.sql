CREATE DATABASE  stupidmart DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


DROP TABLE IF EXISTS `Role`;

CREATE TABLE `Role` (
  `roleID` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(64) NOT NULL UNIQUE,
  `permission` TINYINT NOT NULL,
  PRIMARY KEY (`roleID`),
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `User`;

CREATE TABLE `User` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `userSN` varchar(100) NOT NULL,
  `userName`  varchar(100) NOT NULL,
  `gender` TINYINT(1) NOT NULL,
  `age` TINYINT NOT NULL,
  `telephone` varchar(30) NOT NULL,
  `role_id` varchar(30) NOT NULL,
  PRIMARY KEY (`userID`),
  CONSTRAINT `user_fk` FOREIGN KEY (`role_id`) REFERENCES `Role` (`roleID`) ON DELETE CASCADE ON UPDATE CASCADE,
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Provider`;

CREATE TABLE `Provider` (
  `providerID` int(11) NOT NULL AUTO_INCREMENT,
  `providerSN` varchar(100) NOT NULL,
  `providerName` varchar(100) NOT NULL,
  `contact` varchar(100) NOT NULL,
  `telephone` varchar(30) NOT NULL,
  `fax` varchar(30) DEFAULT NULL,
  'createdTime' DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`providerID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Bill`;

CREATE TABLE `Bill` (
  `BillID` int(11) NOT NULL AUTO_INCREMENT,
  `BillSN` varchar(100) NOT NULL,
  `product` varchar(100) NOT NULL,
  `providerName` varchar(100) NOT NULL,
  'billAmount' DOUBLE NOT NULL,
  'paid' TINYINT(1) NOT NULL,
  'createdTime' DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`BillID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;


CREATE TABLE bills (
  id INTEGER NOT NULL AUTO_INCREMENT,
  bill_sn VARCHAR(32) NOT NULL,
  product VARCHAR(80) NOT NULL,
  unit VARCHAR(32) NOT NULL,
  amount DOUBLE,
  numbers FLOAT(2),
  is_paid BOOL,
  provider_id INTEGER,
  created_at DATETIME, PRIMARY KEY (id), FOREIGN KEY(provider_id) REFERENCES providers (id),
  UNIQUE (bill_sn),
  CHECK (is_paid IN (0, 1)
)