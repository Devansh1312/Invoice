-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: Devansh1312.mysql.pythonanywhere-services.com    Database: Devansh1312$Invoice
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Module',6,'add_modules'),(22,'Can change Module',6,'change_modules'),(23,'Can delete Module',6,'delete_modules'),(24,'Can view Module',6,'view_modules'),(25,'Can add role',7,'add_role'),(26,'Can change role',7,'change_role'),(27,'Can delete role',7,'delete_role'),(28,'Can view role',7,'view_role'),(29,'Can add system settings',8,'add_systemsettings'),(30,'Can change system settings',8,'change_systemsettings'),(31,'Can delete system settings',8,'delete_systemsettings'),(32,'Can view system settings',8,'view_systemsettings'),(33,'Can add Permission',9,'add_permission'),(34,'Can change Permission',9,'change_permission'),(35,'Can delete Permission',9,'delete_permission'),(36,'Can view Permission',9,'view_permission'),(37,'Can add role has permission',10,'add_rolehaspermission'),(38,'Can change role has permission',10,'change_rolehaspermission'),(39,'Can delete role has permission',10,'delete_rolehaspermission'),(40,'Can view role has permission',10,'view_rolehaspermission'),(41,'Can add user',11,'add_user'),(42,'Can change user',11,'change_user'),(43,'Can delete user',11,'delete_user'),(44,'Can view user',11,'view_user'),(45,'Can add invoice',12,'add_invoice'),(46,'Can change invoice',12,'change_invoice'),(47,'Can delete invoice',12,'delete_invoice'),(48,'Can view invoice',12,'view_invoice'),(49,'Can add blacklisted token',13,'add_blacklistedtoken'),(50,'Can change blacklisted token',13,'change_blacklistedtoken'),(51,'Can delete blacklisted token',13,'delete_blacklistedtoken'),(52,'Can view blacklisted token',13,'view_blacklistedtoken'),(53,'Can add outstanding token',14,'add_outstandingtoken'),(54,'Can change outstanding token',14,'change_outstandingtoken'),(55,'Can delete outstanding token',14,'delete_outstandingtoken'),(56,'Can view outstanding token',14,'view_outstandingtoken');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_invoice_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_invoice_user_id` FOREIGN KEY (`user_id`) REFERENCES `invoice_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(12,'Invoice_admin','invoice'),(6,'Invoice_admin','modules'),(9,'Invoice_admin','permission'),(7,'Invoice_admin','role'),(10,'Invoice_admin','rolehaspermission'),(8,'Invoice_admin','systemsettings'),(11,'Invoice_admin','user'),(5,'sessions','session'),(13,'token_blacklist','blacklistedtoken'),(14,'token_blacklist','outstandingtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-20 09:34:49.229706'),(2,'contenttypes','0002_remove_content_type_name','2025-06-20 09:34:49.308079'),(3,'auth','0001_initial','2025-06-20 09:34:49.647163'),(4,'auth','0002_alter_permission_name_max_length','2025-06-20 09:34:49.726572'),(5,'auth','0003_alter_user_email_max_length','2025-06-20 09:34:49.738803'),(6,'auth','0004_alter_user_username_opts','2025-06-20 09:34:49.750473'),(7,'auth','0005_alter_user_last_login_null','2025-06-20 09:34:49.761898'),(8,'auth','0006_require_contenttypes_0002','2025-06-20 09:34:49.766885'),(9,'auth','0007_alter_validators_add_error_messages','2025-06-20 09:34:49.778474'),(10,'auth','0008_alter_user_username_max_length','2025-06-20 09:34:49.789853'),(11,'auth','0009_alter_user_last_name_max_length','2025-06-20 09:34:49.803959'),(12,'auth','0010_alter_group_name_max_length','2025-06-20 09:34:49.870909'),(13,'auth','0011_update_proxy_permissions','2025-06-20 09:34:49.880847'),(14,'auth','0012_alter_user_first_name_max_length','2025-06-20 09:34:49.889800'),(15,'Invoice_admin','0001_initial','2025-06-20 09:34:50.912780'),(16,'Invoice_admin','0002_invoice_other_invoice_other_amount_and_more','2025-06-20 09:34:51.052972'),(17,'Invoice_admin','0003_alter_invoice_options_alter_invoice_bill_amount_and_more','2025-06-20 09:34:51.091064'),(18,'Invoice_admin','0004_invoice_note_alter_role_permissions','2025-06-20 09:34:51.133285'),(19,'admin','0001_initial','2025-06-20 09:34:51.322984'),(20,'admin','0002_logentry_remove_auto_add','2025-06-20 09:34:51.339461'),(21,'admin','0003_logentry_add_action_flag_choices','2025-06-20 09:34:51.354964'),(22,'sessions','0001_initial','2025-06-20 09:34:51.416742'),(23,'token_blacklist','0001_initial','2025-06-20 09:34:51.671090'),(24,'token_blacklist','0002_outstandingtoken_jti_hex','2025-06-20 09:34:51.704262'),(25,'token_blacklist','0003_auto_20171017_2007','2025-06-20 09:34:51.727909'),(26,'token_blacklist','0004_auto_20171017_2013','2025-06-20 09:34:51.916151'),(27,'token_blacklist','0005_remove_outstandingtoken_jti','2025-06-20 09:34:52.014002'),(28,'token_blacklist','0006_auto_20171017_2113','2025-06-20 09:34:52.050336'),(29,'token_blacklist','0007_auto_20171017_2214','2025-06-20 09:34:52.371602'),(30,'token_blacklist','0008_migrate_to_bigautofield','2025-06-20 09:34:52.691151'),(31,'token_blacklist','0010_fix_migrate_to_bigautofield','2025-06-20 09:34:52.713404'),(32,'token_blacklist','0011_linearizes_history','2025-06-20 09:34:52.718356'),(33,'token_blacklist','0012_alter_outstandingtoken_user','2025-06-20 09:34:52.734947');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('dqjxtusvq4ysb2ol3ab3g7u0s1ny7tq2','.eJxVjssOwiAURP-FtSGAPEqX7v0GAvfeWtSAKW2iMf671nSh2zlnJvNkIS7zGJZGU8jIeqbY7jdLES5UVoDnWE6VQy3zlBNfFb7Rxo8V6XrY3L-BMbbx0wYg47UiaaxFY6U3siNnkzYSk5aAe0ygO-kjOqE8aBJDEk4r5wfVme-rRq3lWgLdb3l6sF4q4a0QrzfsQD-7:1uSVRe:m31mk1PUjXWFfPilt5QrDJyjfwAqg1Cnc7iyDR01V7g','2025-07-04 09:41:50.412287'),('hq2pvcxyjsitvv1ikousrrmy0esm38s7','.eJxVjMsOwiAQRf-FtSGADA-X7vsNBGamUjU0Ke3K-O_apAvd3nPOfYmUt7WmrfOSJhIXYcTpdysZH9x2QPfcbrPEua3LVOSuyIN2OczEz-vh_h3U3Ou3RmSI1rAG5wicjqADe1csaCpWI52poA06ZvLKRLSsxqK8NT6OJoAR7w_WODdM:1uVVUy:bqAlRGyv4yMbEvRr6HvZP992HDcC3CkYMG4LHXP7S5k','2025-07-12 16:21:40.035440'),('jle989mljok4j2bt2n3plbzphe9dxp7g','.eJxVjssOwiAURP-FtSGAPEqX7v0GAvfeWtSAKW2iMf671nSh2zlnJvNkIS7zGJZGU8jIeqbY7jdLES5UVoDnWE6VQy3zlBNfFb7Rxo8V6XrY3L-BMbbx0wYg47UiaaxFY6U3siNnkzYSk5aAe0ygO-kjOqE8aBJDEk4r5wfVme-rRq3lWgLdb3l6sF4q4a0QrzfsQD-7:1uSVa5:LfJl0JrIURuf3sk6oUbH6nKM5LNvh_zdf9jmQBph-_8','2025-07-04 09:50:33.079200'),('jnz9b0650tzacdllbqyj1iz5jrlzr5ar','.eJxVjssOwiAURP-FtSGAPEqX7v0GAvfeWtSAKW2iMf671nSh2zlnJvNkIS7zGJZGU8jIeqbY7jdLES5UVoDnWE6VQy3zlBNfFb7Rxo8V6XrY3L-BMbbx0wYg47UiaaxFY6U3siNnkzYSk5aAe0ygO-kjOqE8aBJDEk4r5wfVme-rRq3lWgLdb3l6sF4q4a0QrzfsQD-7:1uSd0X:kaQMV6XAonyWRtcEYQ4woaZm4v5A4GpCnMGh6zqbhDQ','2025-07-04 17:46:21.987034'),('owho9h2klcjik6y4dq5lksbiuany8n9i','.eJxVjssOwiAURP-FtSGAPEqX7v0GAvfeWtSAKW2iMf671nSh2zlnJvNkIS7zGJZGU8jIeqbY7jdLES5UVoDnWE6VQy3zlBNfFb7Rxo8V6XrY3L-BMbbx0wYg47UiaaxFY6U3siNnkzYSk5aAe0ygO-kjOqE8aBJDEk4r5wfVme-rRq3lWgLdb3l6sF4q4a0QrzfsQD-7:1uSWCj:1xYCU2z-_n-CJPuhF2oI2qV-vUVm_N7XA36l2vQL-Fs','2025-07-04 10:30:29.100866');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_invoice`
--

DROP TABLE IF EXISTS `invoice_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_invoice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bill_template` varchar(10) NOT NULL,
  `bill_number` varchar(100) NOT NULL,
  `bill_date` date NOT NULL,
  `bill_amount` decimal(10,2) NOT NULL,
  `jug` int NOT NULL,
  `jug_count` int NOT NULL,
  `jug_amount` decimal(10,2) NOT NULL,
  `bottle` int NOT NULL,
  `bottle_count` int NOT NULL,
  `bottle_amount` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `bill_created_at` datetime(6) NOT NULL,
  `bill_updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `other` varchar(255) DEFAULT NULL,
  `other_amount` decimal(10,2) NOT NULL,
  `note` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_invoice_bill_number_e0b25de3_uniq` (`bill_number`),
  KEY `invoice_invoice_user_id_b8c84949_fk_invoice_user_id` (`user_id`),
  CONSTRAINT `invoice_invoice_user_id_b8c84949_fk_invoice_user_id` FOREIGN KEY (`user_id`) REFERENCES `invoice_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_invoice`
--

LOCK TABLES `invoice_invoice` WRITE;
/*!40000 ALTER TABLE `invoice_invoice` DISABLE KEYS */;
INSERT INTO `invoice_invoice` VALUES (2,'1','20250001','2025-06-21',500.00,20,20,25.00,0,0,25.00,500.00,'2025-06-21 18:06:30.674402','2025-06-21 18:06:30.674447',6,'',0.00,''),(3,'2','20250002','2025-06-27',10100.00,0,0,25.00,404,404,25.00,10100.00,'2025-06-28 16:26:51.366629','2025-06-28 16:26:51.366644',26,'',0.00,'');
/*!40000 ALTER TABLE `invoice_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_modules`
--

DROP TABLE IF EXISTS `invoice_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_modules` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name_en` varchar(100) DEFAULT NULL,
  `name_ar` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_modules`
--

LOCK TABLES `invoice_modules` WRITE;
/*!40000 ALTER TABLE `invoice_modules` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice_modules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_permissions`
--

DROP TABLE IF EXISTS `invoice_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `display_name` varchar(255) DEFAULT NULL,
  `description` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `module_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `invoice_permissions_module_id_ad1787b8_fk_invoice_modules_id` (`module_id`),
  CONSTRAINT `invoice_permissions_module_id_ad1787b8_fk_invoice_modules_id` FOREIGN KEY (`module_id`) REFERENCES `invoice_modules` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_permissions`
--

LOCK TABLES `invoice_permissions` WRITE;
/*!40000 ALTER TABLE `invoice_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_role`
--

DROP TABLE IF EXISTS `invoice_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name_en` varchar(100) DEFAULT NULL,
  `name_ar` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_role`
--

LOCK TABLES `invoice_role` WRITE;
/*!40000 ALTER TABLE `invoice_role` DISABLE KEYS */;
INSERT INTO `invoice_role` VALUES (1,'Super Admin','Super Admin',NULL,NULL),(2,'Customer','Customer',NULL,NULL);
/*!40000 ALTER TABLE `invoice_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_role_has_permissions`
--

DROP TABLE IF EXISTS `invoice_role_has_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_role_has_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `permission_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `invoice_role_has_per_permission_id_6dec5230_fk_invoice_p` (`permission_id`),
  KEY `invoice_role_has_permissions_role_id_48c050a5_fk_invoice_role_id` (`role_id`),
  CONSTRAINT `invoice_role_has_per_permission_id_6dec5230_fk_invoice_p` FOREIGN KEY (`permission_id`) REFERENCES `invoice_permissions` (`id`),
  CONSTRAINT `invoice_role_has_permissions_role_id_48c050a5_fk_invoice_role_id` FOREIGN KEY (`role_id`) REFERENCES `invoice_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_role_has_permissions`
--

LOCK TABLES `invoice_role_has_permissions` WRITE;
/*!40000 ALTER TABLE `invoice_role_has_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice_role_has_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_systemsettings`
--

DROP TABLE IF EXISTS `invoice_systemsettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_systemsettings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fav_icon` varchar(255) DEFAULT NULL,
  `header_logo` varchar(255) DEFAULT NULL,
  `website_name_english` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext,
  `currency_symbol` varchar(10) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_systemsettings`
--

LOCK TABLES `invoice_systemsettings` WRITE;
/*!40000 ALTER TABLE `invoice_systemsettings` DISABLE KEYS */;
INSERT INTO `invoice_systemsettings` VALUES (1,'system_settings/fav_icon_NZ4MrKxv.png','system_settings/header_logo_4r3uqG5R.png','Khodal Water','8849029071','shahdevansh13122002@gmail.com','19/50 MANSAROVAR COMPLEX, OPP GURUDWARA,CHHANI,VADODARA',NULL,'2025-06-20 09:43:05.675262','2025-06-20 09:43:05.675304');
/*!40000 ALTER TABLE `invoice_systemsettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_user`
--

DROP TABLE IF EXISTS `invoice_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `address` longtext,
  `email` varchar(254) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `name` varchar(150) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `invoice_user_role_id_77709f8b_fk_invoice_role_id` (`role_id`),
  CONSTRAINT `invoice_user_role_id_77709f8b_fk_invoice_role_id` FOREIGN KEY (`role_id`) REFERENCES `invoice_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_user`
--

LOCK TABLES `invoice_user` WRITE;
/*!40000 ALTER TABLE `invoice_user` DISABLE KEYS */;
INSERT INTO `invoice_user` VALUES (2,'2025-06-28 16:21:40.024075',1,'Devansh',NULL,'Devansh@gmail.com','',NULL,'pbkdf2_sha256$1000000$n863TASsCdkprt8weRdZRR$asGT8R/5UM4DXTO8SfX3i39fWJAGgMrUpCDpIT7riqY=',1,1,'2025-06-17 17:44:26.720203','2025-06-17 17:44:26.720203',1),(4,NULL,0,'cust_9825206989','Patel Hotel',NULL,'9825206989','Patel Hotel','',1,0,'2025-06-20 17:47:37.101743','2025-06-20 17:52:46.657776',2),(6,NULL,0,'cust_8733005000','Chhani',NULL,'8733005000','Vijay Store (Chhani)','',1,0,'2025-06-20 19:45:48.986373','2025-06-20 19:50:12.410810',2),(7,NULL,0,'cust_9909358159','Chhani',NULL,'9909358159','Sarpanch ','',1,0,'2025-06-20 19:47:02.901881','2025-06-20 19:47:02.901909',2),(8,NULL,0,'cust_123','Chhani',NULL,'123',' Mahavir Courier','',1,0,'2025-06-20 19:48:27.294269','2025-06-20 19:48:27.294288',2),(9,NULL,0,'cust_6358848678','Chhani',NULL,'6358848678','Gandhi Tiffin','',1,0,'2025-06-20 19:49:57.558923','2025-06-20 19:49:57.558942',2),(10,NULL,0,'cust_12','',NULL,'12','Yogi Green 101 (Bharuch)','',1,0,'2025-06-20 19:51:32.851296','2025-06-20 19:51:32.851320',2),(11,NULL,0,'cust_1234','',NULL,'1234','Yogi Green (Security)','',1,0,'2025-06-20 19:52:31.474602','2025-06-20 19:52:31.474621',2),(12,NULL,0,'cust_9879066339','Chhani',NULL,'9879066339','Kaju Badam','',1,0,'2025-06-20 19:54:53.892629','2025-06-20 19:54:53.892657',2),(13,NULL,0,'cust_10','Chhani',NULL,'10','Narayan Enterprise','',1,0,'2025-06-20 19:58:31.181028','2025-06-20 19:58:31.181051',2),(14,NULL,0,'cust_11','Chhani',NULL,'11','Harmanbhai Patel ','',1,0,'2025-06-20 19:59:22.770847','2025-06-20 19:59:22.770863',2),(15,NULL,0,'cust_13','Chhani',NULL,'13','Sun Agro','',1,0,'2025-06-20 20:00:21.355550','2025-06-20 20:00:21.355583',2),(16,NULL,0,'cust_9722697721','Chhani',NULL,'9722697721','Vimal Icecream','',1,0,'2025-06-20 20:01:47.368371','2025-06-20 20:01:47.368399',2),(17,NULL,0,'cust_9998486546','Chhani',NULL,'9998486546','Charmy Clinic','',1,0,'2025-06-20 20:02:56.789715','2025-06-20 20:02:56.789739',2),(18,NULL,0,'cust_9120503323','Chhani',NULL,'9120503323','Amin Nagar 44','',1,0,'2025-06-20 20:03:53.399305','2025-06-20 20:03:53.399335',2),(19,NULL,0,'cust_21','Chhani',NULL,'21','Shreenathji Hardware','',1,0,'2025-06-20 20:05:01.095075','2025-06-20 20:05:01.095107',2),(20,NULL,0,'cust_9427','',NULL,'9427','Bagga Garage','',1,0,'2025-06-20 20:05:44.127966','2025-06-20 20:05:44.127988',2),(21,NULL,0,'cust_32','',NULL,'32','AR Auto','',1,0,'2025-06-20 20:11:37.037081','2025-06-20 20:11:37.037112',2),(22,NULL,0,'cust_9879198666','',NULL,'9879198666','CEAT Tyres','',1,0,'2025-06-20 20:12:22.409413','2025-06-20 20:12:22.409435',2),(23,NULL,0,'cust_9227210803','',NULL,'9227210803','Coca Cola','',1,0,'2025-06-20 20:13:29.500576','2025-06-20 20:13:29.500604',2),(24,NULL,0,'cust_9974030231','',NULL,'9974030231','Doodh Ni Dairy (Vishnu Kaka)','',1,0,'2025-06-20 20:16:21.700711','2025-06-20 20:16:21.700743',2),(25,NULL,0,'cust_33','',NULL,'33','Jay Ambe (Marble)','',1,0,'2025-06-20 20:17:59.413613','2025-06-20 20:17:59.413631',2),(26,NULL,0,'cust_8866003056','',NULL,'8866003056','T G Gathiya','',1,0,'2025-06-20 20:18:48.654541','2025-06-20 20:18:48.654569',2);
/*!40000 ALTER TABLE `invoice_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_user_groups`
--

DROP TABLE IF EXISTS `invoice_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_user_groups_user_id_group_id_a53d1111_uniq` (`user_id`,`group_id`),
  KEY `invoice_user_groups_group_id_70b6eadb_fk_auth_group_id` (`group_id`),
  CONSTRAINT `invoice_user_groups_group_id_70b6eadb_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `invoice_user_groups_user_id_c960e346_fk_invoice_user_id` FOREIGN KEY (`user_id`) REFERENCES `invoice_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_user_groups`
--

LOCK TABLES `invoice_user_groups` WRITE;
/*!40000 ALTER TABLE `invoice_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_user_user_permissions`
--

DROP TABLE IF EXISTS `invoice_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_user_user_permis_user_id_permission_id_184a121d_uniq` (`user_id`,`permission_id`),
  KEY `invoice_user_user_pe_permission_id_d8bba337_fk_auth_perm` (`permission_id`),
  CONSTRAINT `invoice_user_user_pe_permission_id_d8bba337_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `invoice_user_user_pe_user_id_9e1f61fd_fk_invoice_u` FOREIGN KEY (`user_id`) REFERENCES `invoice_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_user_user_permissions`
--

LOCK TABLES `invoice_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `invoice_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outs_user_id_83bc629a_fk_invoice_u` (`user_id`),
  CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_invoice_u` FOREIGN KEY (`user_id`) REFERENCES `invoice_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-28 14:18:39
