-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: 10.192.85.133    Database: db_21xe_clone
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app`
--

DROP TABLE IF EXISTS `app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app` (
  `id_app` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `market` varchar(45) DEFAULT NULL,
  `engine` varchar(45) DEFAULT NULL,
  `gearbox` varchar(45) DEFAULT NULL,
  `axle` varchar(45) DEFAULT NULL,
  `handle` varchar(45) DEFAULT NULL,
  `app` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_app`)
) ENGINE=InnoDB AUTO_INCREMENT=561 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app`
--

LOCK TABLES `app` WRITE;
/*!40000 ALTER TABLE `app` DISABLE KEYS */;
/*!40000 ALTER TABLE `app` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `header`
--

DROP TABLE IF EXISTS `header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `header` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_project` int(11) NOT NULL,
  `col1` varchar(100) DEFAULT NULL,
  `col2` varchar(100) DEFAULT NULL,
  `col3` varchar(100) DEFAULT NULL,
  `col4` varchar(100) DEFAULT NULL,
  `col5` varchar(100) DEFAULT NULL,
  `col6` varchar(100) DEFAULT NULL,
  `col7` varchar(100) DEFAULT NULL,
  `col8` varchar(100) DEFAULT NULL,
  `col9` varchar(100) DEFAULT NULL,
  `col10` varchar(100) DEFAULT NULL,
  `col11` varchar(100) DEFAULT NULL,
  `col12` varchar(100) DEFAULT NULL,
  `col13` varchar(100) DEFAULT NULL,
  `col14` varchar(100) DEFAULT NULL,
  `col15` varchar(100) DEFAULT NULL,
  `col16` varchar(100) DEFAULT NULL,
  `col17` varchar(100) DEFAULT NULL,
  `col18` varchar(100) DEFAULT NULL,
  `col19` varchar(100) DEFAULT NULL,
  `col20` varchar(100) DEFAULT NULL,
  `col21` varchar(100) DEFAULT NULL,
  `col22` varchar(100) DEFAULT NULL,
  `col23` varchar(100) DEFAULT NULL,
  `col24` varchar(100) DEFAULT NULL,
  `col25` varchar(100) DEFAULT NULL,
  `col26` varchar(100) DEFAULT NULL,
  `col27` varchar(100) DEFAULT NULL,
  `col28` varchar(100) DEFAULT NULL,
  `col29` varchar(100) DEFAULT NULL,
  `col30` varchar(100) DEFAULT NULL,
  `col31` varchar(100) DEFAULT NULL,
  `col32` varchar(100) DEFAULT NULL,
  `col33` varchar(100) DEFAULT NULL,
  `col34` varchar(100) DEFAULT NULL,
  `col35` varchar(100) DEFAULT NULL,
  `col36` varchar(100) DEFAULT NULL,
  `col37` varchar(100) DEFAULT NULL,
  `col38` varchar(100) DEFAULT NULL,
  `col39` varchar(100) DEFAULT NULL,
  `col40` varchar(100) DEFAULT NULL,
  `col41` varchar(100) DEFAULT NULL,
  `col42` varchar(100) DEFAULT NULL,
  `col43` varchar(100) DEFAULT NULL,
  `col44` varchar(100) DEFAULT NULL,
  `col45` varchar(100) DEFAULT NULL,
  `col46` varchar(100) DEFAULT NULL,
  `col47` varchar(100) DEFAULT NULL,
  `col48` varchar(100) DEFAULT NULL,
  `col49` varchar(100) DEFAULT NULL,
  `col50` varchar(100) DEFAULT NULL,
  `col51` varchar(100) DEFAULT NULL,
  `col52` varchar(100) DEFAULT NULL,
  `col53` varchar(100) DEFAULT NULL,
  `col54` varchar(100) DEFAULT NULL,
  `col55` varchar(100) DEFAULT NULL,
  `col56` varchar(100) DEFAULT NULL,
  `col57` varchar(100) DEFAULT NULL,
  `col58` varchar(100) DEFAULT NULL,
  `col59` varchar(100) DEFAULT NULL,
  `col60` varchar(100) DEFAULT NULL,
  `col61` varchar(100) DEFAULT NULL,
  `col62` varchar(100) DEFAULT NULL,
  `col63` varchar(100) DEFAULT NULL,
  `col64` varchar(100) DEFAULT NULL,
  `col65` varchar(100) DEFAULT NULL,
  `col66` varchar(100) DEFAULT NULL,
  `col67` varchar(100) DEFAULT NULL,
  `col68` varchar(100) DEFAULT NULL,
  `col69` varchar(100) DEFAULT NULL,
  `col70` varchar(100) DEFAULT NULL,
  `col71` varchar(100) DEFAULT NULL,
  `col72` varchar(100) DEFAULT NULL,
  `col73` varchar(100) DEFAULT NULL,
  `col74` varchar(100) DEFAULT NULL,
  `col75` varchar(100) DEFAULT NULL,
  `col76` varchar(100) DEFAULT NULL,
  `col77` varchar(100) DEFAULT NULL,
  `col78` varchar(100) DEFAULT NULL,
  `col79` varchar(100) DEFAULT NULL,
  `col80` varchar(100) DEFAULT NULL,
  `col81` varchar(100) DEFAULT NULL,
  `col82` varchar(100) DEFAULT NULL,
  `col83` varchar(100) DEFAULT NULL,
  `col84` varchar(100) DEFAULT NULL,
  `col85` varchar(100) DEFAULT NULL,
  `col86` varchar(100) DEFAULT NULL,
  `col87` varchar(100) DEFAULT NULL,
  `col88` varchar(100) DEFAULT NULL,
  `col89` varchar(100) DEFAULT NULL,
  `col90` varchar(100) DEFAULT NULL,
  `col91` varchar(100) DEFAULT NULL,
  `col92` varchar(100) DEFAULT NULL,
  `col93` varchar(100) DEFAULT NULL,
  `col94` varchar(100) DEFAULT NULL,
  `col95` varchar(100) DEFAULT NULL,
  `col96` varchar(100) DEFAULT NULL,
  `col97` varchar(100) DEFAULT NULL,
  `col98` varchar(100) DEFAULT NULL,
  `col99` varchar(100) DEFAULT NULL,
  `col100` varchar(100) DEFAULT NULL,
  `col101` varchar(100) DEFAULT NULL,
  `col102` varchar(100) DEFAULT NULL,
  `col103` varchar(100) DEFAULT NULL,
  `col104` varchar(100) DEFAULT NULL,
  `col105` varchar(100) DEFAULT NULL,
  `col106` varchar(100) DEFAULT NULL,
  `col107` varchar(100) DEFAULT NULL,
  `col108` varchar(100) DEFAULT NULL,
  `col109` varchar(100) DEFAULT NULL,
  `col110` varchar(100) DEFAULT NULL,
  `col111` varchar(100) DEFAULT NULL,
  `col112` varchar(100) DEFAULT NULL,
  `col113` varchar(100) DEFAULT NULL,
  `col114` varchar(100) DEFAULT NULL,
  `col115` varchar(100) DEFAULT NULL,
  `col116` varchar(100) DEFAULT NULL,
  `col117` varchar(100) DEFAULT NULL,
  `col118` varchar(100) DEFAULT NULL,
  `col119` varchar(100) DEFAULT NULL,
  `col120` varchar(100) DEFAULT NULL,
  `col121` varchar(100) DEFAULT NULL,
  `col122` varchar(100) DEFAULT NULL,
  `col123` varchar(100) DEFAULT NULL,
  `col124` varchar(100) DEFAULT NULL,
  `col125` varchar(100) DEFAULT NULL,
  `col126` varchar(100) DEFAULT NULL,
  `col127` varchar(100) DEFAULT NULL,
  `col128` varchar(100) DEFAULT NULL,
  `col129` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=283 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `header`
--

LOCK TABLES `header` WRITE;
/*!40000 ALTER TABLE `header` DISABLE KEYS */;
/*!40000 ALTER TABLE `header` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_table`
--

DROP TABLE IF EXISTS `main_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` longtext,
  `cadic_number` longtext NOT NULL,
  `snt` longtext,
  `regulations` longtext,
  `pep` longtext,
  `Other` longtext,
  `good_design` longtext,
  `y0` longtext,
  `y0_number` longtext,
  `car_recurrence_prevention` longtext,
  `solution` longtext,
  `solution_number` longtext,
  `common_validation_item` longtext,
  `procedure_item` longtext,
  `requirement` longtext,
  `step1_pt_jp` longtext,
  `step2_pt_jp` longtext,
  `step1_vt_jp` longtext,
  `step2_vt_jp` longtext,
  `step3_vt_jp` longtext,
  `lv1_ct_jp` longtext,
  `lv2_ct_jp` longtext,
  `lv3_ct_jp` longtext,
  `lv4_ct_jp` longtext,
  `comment_ct_jp` longtext,
  `step1_pt_en` longtext,
  `step2_pt_en` longtext,
  `step1_vt_en` longtext,
  `step2_vt_en` longtext,
  `step3_vt_en` longtext,
  `lv1_ct_en` longtext,
  `lv2_ct_en` longtext,
  `lv3_ct_en` longtext,
  `lv4_ct_en` longtext,
  `comment_ct_en` longtext,
  `digital_evaluation_app` longtext,
  `pf_evaluation_app` longtext,
  `physical_evaluation_app` longtext,
  `kca_project_group_deploy` longtext,
  `team_deploy` longtext,
  `manager_name_deploy` longtext,
  `id_or_mail_account_deploy` longtext,
  `name_of_person_in_charge_deploy` longtext,
  `id_or_mail_account_2_deploy` longtext,
  `target_value_deploy` longtext,
  `comment_deploy` longtext,
  `kca_project_group_ac` longtext,
  `team_ac` longtext,
  `manager_name_ac` longtext,
  `id_or_mail_account_ac` longtext,
  `name_of_person_in_charge_ac` longtext,
  `id_or_mail_account_2_ac` longtext,
  `agreement_of_target_ac` longtext,
  `comment_ac` longtext,
  `kca_project_group_digital` longtext,
  `team_digital` longtext,
  `manager_name_digital` longtext,
  `id_or_mail_account_digital` longtext,
  `evaluation_responsible_digital` longtext,
  `id_or_mail_account_2_digital` longtext,
  `evaluate_or_not_ds` longtext,
  `result_first_ds` longtext,
  `report_number_ds` longtext,
  `number_of_qbase_ds` longtext,
  `qbase_number_ds` longtext,
  `result_counter_ds` longtext,
  `comment_ds` longtext,
  `evaluate_or_not_dc` longtext,
  `result_first_dc` longtext,
  `report_number_dc` longtext,
  `number_of_qbase_dc` longtext,
  `qbase_number_dc` longtext,
  `result_counter_dc` longtext,
  `comment_dc` longtext,
  `kca_project_group_ppc` longtext,
  `team_ppc` longtext,
  `manager_name_ppc` longtext,
  `id_or_mail_account_ppc` longtext,
  `evaluation_responsible_ppc` longtext,
  `id_or_mail_account_2_ppc` longtext,
  `evaluate_or_not_pfc` longtext,
  `confirmation_first_pfc` longtext,
  `feedback_timing_pfc` longtext,
  `result_first_pfc` longtext,
  `confirmation_completion_pfc` longtext,
  `report_number_pfc` longtext,
  `number_of_qbase_pfc` longtext,
  `qbase_number_pfc` longtext,
  `result_counter_pfc` longtext,
  `confirmation_completion_date_pfc` longtext,
  `comment_pfc` longtext,
  `kca_project_group_ppe` longtext,
  `team_ppe` longtext,
  `manager_name_ppe` longtext,
  `id_or_mail_account_ppe` longtext,
  `evaluation_responsible_ppe` longtext,
  `id_or_mail_account_2_ppe` longtext,
  `evaluate_or_not_vc` longtext,
  `confirm_first_date_vc` longtext,
  `result_first_vc` longtext,
  `confirm_first_completion_vc` longtext,
  `report_number_vc` longtext,
  `number_of_qbase_vc` longtext,
  `qbase_number_vc` longtext,
  `result_counter_vc` longtext,
  `confirm_first_completion_2_vc` longtext,
  `comment_vc` longtext,
  `evaluate_or_not_pt1` longtext,
  `confirm_first_date_pt1` longtext,
  `result_first_pt1` longtext,
  `confirm_first_completion_pt1` longtext,
  `report_number_pt1` longtext,
  `number_of_qbase_pt1` longtext,
  `qbase_number_pt1` longtext,
  `result_counter_pt1` longtext,
  `confirm_first_completion_2_pt1` longtext,
  `comment_pt1` longtext,
  `evaluate_or_not_pt2` longtext,
  `confirmation_first_time_pt2` longtext,
  `result_first_pt2` longtext,
  `confirm_first_completion_pt2` longtext,
  `report_number_pt2` longtext,
  `number_of_qbase_pt2` longtext,
  `qbase_number_pt2` longtext,
  `result_counter_pt2` longtext,
  `confirm_first_completion_2_pt2` longtext,
  `comment_pt2` longtext,
  `common_unique` longtext,
  `id_project` int(11) NOT NULL,
  `id_app` int(11) NOT NULL,
  `value` varchar(100) DEFAULT NULL,
  `note_1` longtext,
  `note_2` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `index_test` (`id`),
  KEY `FK_id_project_idx` (`id_project`),
  KEY `FK_id_app_idx` (`id_app`),
  CONSTRAINT `FK_id_app` FOREIGN KEY (`id_app`) REFERENCES `app` (`id_app`) ON UPDATE CASCADE,
  CONSTRAINT `FK_id_project` FOREIGN KEY (`id_project`) REFERENCES `project` (`id_project`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1135733 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_table`
--

LOCK TABLES `main_table` WRITE;
/*!40000 ALTER TABLE `main_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `id_project` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(45) NOT NULL,
  `power_train` varchar(45) NOT NULL,
  `market` varchar(45) NOT NULL,
  `develop_case` varchar(45) NOT NULL,
  PRIMARY KEY (`id_project`),
  UNIQUE KEY `id_UNIQUE` (`id_project`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `permission` varchar(45) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'ADMIN_H61A','12345678','admin',NULL),(2,'STAFF_1','12345678','staff',NULL),(3,'ADMIN','12345678','master',NULL),(5,'STAFF_2','12345678','staff',NULL),(12,'ADMIN_WZ1J','12345678','admin',NULL),(13,'ADMIN_P02A','12345678','admin',NULL),(14,'ADMIN_PO2F','12345678','admin',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-07 14:45:54
