-- MySQL dump 10.13  Distrib 5.5.36-34.1, for Linux (x86_64)
--
-- Host: localhost    Database: saltweb
-- ------------------------------------------------------
-- Server version	5.5.36-34.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'deviceID',
  `devicename` varchar(30) NOT NULL COMMENT 'device名',
  `devicetype` varchar(30) NOT NULL DEFAULT 'JobManager' COMMENT 'device类型',
  `hostip` varchar(15) NOT NULL COMMENT '运行主机IP',
  `status` varchar(10) NOT NULL DEFAULT 'OnLine' COMMENT 'device状态',
  `startdate` date NOT NULL COMMENT '启动时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `devicename` (`devicename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_logs`
--

DROP TABLE IF EXISTS `login_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_logs` (
  `id` int(6) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `uid` int(3) NOT NULL COMMENT '用户ID',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
  `ip` varchar(15) NOT NULL DEFAULT '127.0.0.1' COMMENT '登录客户端IP',
  `location` varchar(30) DEFAULT NULL COMMENT '登录地点',
  `agent` varchar(150) NOT NULL DEFAULT 'User Agent' COMMENT '浏览器',
  `token` varchar(64) DEFAULT NULL COMMENT '令牌(用于记住我自动登录)',
  `expiry` datetime DEFAULT NULL COMMENT '过期时间',
  `status` varchar(3) NOT NULL DEFAULT 'yes' COMMENT '状态：描述该会话是否有效',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_logs`
--

LOCK TABLES `login_logs` WRITE;
/*!40000 ALTER TABLE `login_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `login_logs` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(3) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(20) NOT NULL,
  `password` varchar(60) NOT NULL,
  `nickname` varchar(20) DEFAULT NULL COMMENT '昵称，用于友好显示在页面上',
  `mobile` varchar(15) DEFAULT NULL COMMENT '手机号',
  `email` varchar(50) DEFAULT NULL COMMENT '用户E-mail地址',
  `level` int(1) NOT NULL DEFAULT '1' COMMENT '用户级别：0为管理员，1为普通用户',
  `status` varchar(3) NOT NULL DEFAULT 'yes' COMMENT '用户状态：yes表示启用，no表示禁用',
  `loginfo` int(5) NOT NULL DEFAULT '0' COMMENT '登录信息，对应login_logs表中的id',
  `regdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '用户注册时间',
  `comment` varchar(50) DEFAULT NULL COMMENT '用户备注信息',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (0,'System','00000000','系统','88888888','system@test.com',0,'no',0,'2014-03-30 06:18:50','System'),(1,'admin','21232f297a57a5a743894a0e4a801fc3','超级管理员','88888888','admin@test.com',0,'yes',99,'2014-03-30 06:18:50','Super Admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-09 15:42:39
