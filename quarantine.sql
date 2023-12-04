-- MySQL dump 10.13  Distrib 8.0.35, for Win64 (x86_64)
--
-- Host: localhost    Database: quarantine
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `operator`
--

DROP TABLE IF EXISTS `operator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operator` (
  `badge` int NOT NULL,
  `operatorname` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`badge`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operator`
--

LOCK TABLES `operator` WRITE;
/*!40000 ALTER TABLE `operator` DISABLE KEYS */;
INSERT INTO `operator` VALUES (440,'Martin Foley'),(466,'John Ryan'),(467,'David Higgins'),(999,'Jerome Murphy');
/*!40000 ALTER TABLE `operator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quar`
--

DROP TABLE IF EXISTS `quar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quar` (
  `lot` int NOT NULL,
  `part` varchar(30) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `datein` date DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `badge` int DEFAULT NULL,
  `badgeout` int DEFAULT NULL,
  `dateout` date DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `signoutcomment` varchar(255) DEFAULT NULL,
  `building` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`lot`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quar`
--

LOCK TABLES `quar` WRITE;
/*!40000 ALTER TABLE `quar` DISABLE KEYS */;
INSERT INTO `quar` VALUES (1046,'M5 nut',150000,'2023-09-10','tight threads',440,467,'2023-12-04',0,'scrapped off','B1'),(1444,'M19 screw',187000,'2023-12-04','length oversize and head damage',499,467,'2023-12-04',0,'regraded','B3'),(1576,'M2 standoff',16000,'2023-09-29','length undersize',440,NULL,NULL,1,NULL,'B1'),(1598,'M10 washer',6000,'2023-11-17','inner diameter oversize',455,NULL,NULL,1,NULL,'B6'),(1630,'M7 cam',490000,'2023-12-04','head damage',467,NULL,NULL,1,NULL,'B1'),(1632,'M5 threaded bush',5600,'2023-12-01','head damage',467,467,'2023-12-04',0,'passed by QA','B6'),(1673,'M3 screw',19000,'2023-12-04','missing phillips drive feature',467,647,'2023-12-04',0,'passed','B6'),(1799,'M6 panel fastener',66000,'2023-08-22','missing clinch feature',999,467,'2023-12-04',0,'moved to another building','B1'),(2411,'M12 bolt',5000,'2023-12-01','slivers on threads',467,NULL,NULL,1,NULL,'B1'),(5022,'Bearings',15000,'2023-11-27','corrosion present',999,NULL,NULL,1,NULL,NULL),(5566,'Tyres',5000,'2023-10-31','cracks in rubber',460,NULL,NULL,1,NULL,NULL);
/*!40000 ALTER TABLE `quar` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-04 19:19:42
