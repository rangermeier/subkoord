-- phpMyAdmin SQL Dump
-- version 3.4.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 22, 2012 at 11:25 AM
-- Server version: 5.5.20
-- PHP Version: 5.3.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `subkoord_testing`
--

-- --------------------------------------------------------

--
-- Table structure for table `attachment_attachment`
--

CREATE TABLE IF NOT EXISTS `attachment_attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(200) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `attachment_attachment_e4470c6e` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(2, 'Admins'),
(1, 'Newsletter');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=40 ;

--
-- Dumping data for table `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(24, 1, 49),
(30, 1, 50),
(29, 1, 51),
(32, 1, 52),
(31, 1, 53),
(26, 1, 54),
(25, 1, 55),
(28, 1, 56),
(27, 1, 57),
(23, 1, 58),
(22, 1, 59),
(33, 1, 60),
(34, 1, 61),
(35, 1, 62),
(36, 1, 63),
(37, 1, 64),
(38, 1, 65),
(39, 1, 66),
(21, 2, 28),
(15, 2, 29),
(9, 2, 30),
(8, 2, 31),
(7, 2, 32),
(6, 2, 33),
(19, 2, 34),
(12, 2, 35),
(13, 2, 36),
(16, 2, 37),
(2, 2, 38),
(1, 2, 39),
(5, 2, 40),
(3, 2, 41),
(10, 2, 42),
(11, 2, 43),
(20, 2, 44),
(18, 2, 45),
(14, 2, 46),
(17, 2, 47),
(4, 2, 48);

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=67 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add message', 4, 'add_message'),
(11, 'Can change message', 4, 'change_message'),
(12, 'Can delete message', 4, 'delete_message'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add site', 7, 'add_site'),
(20, 'Can change site', 7, 'change_site'),
(21, 'Can delete site', 7, 'delete_site'),
(22, 'Can add flat page', 8, 'add_flatpage'),
(23, 'Can change flat page', 8, 'change_flatpage'),
(24, 'Can delete flat page', 8, 'delete_flatpage'),
(25, 'Can add log entry', 9, 'add_logentry'),
(26, 'Can change log entry', 9, 'change_logentry'),
(27, 'Can delete log entry', 9, 'delete_logentry'),
(28, 'Can add task', 10, 'add_task'),
(29, 'Can change task', 10, 'change_task'),
(30, 'Can delete task', 10, 'delete_task'),
(31, 'Can add event type', 11, 'add_eventtype'),
(32, 'Can change event type', 11, 'change_eventtype'),
(33, 'Can delete event type', 11, 'delete_eventtype'),
(34, 'Can add event', 12, 'add_event'),
(35, 'Can change event', 12, 'change_event'),
(36, 'Can delete event', 12, 'delete_event'),
(37, 'Can add job', 13, 'add_job'),
(38, 'Can change job', 13, 'change_job'),
(39, 'Can delete job', 13, 'delete_job'),
(40, 'Can add note', 14, 'add_note'),
(41, 'Can change note', 14, 'change_note'),
(42, 'Can delete note', 14, 'delete_note'),
(43, 'Can add wikicategory', 15, 'add_wikicategory'),
(44, 'Can change wikicategory', 15, 'change_wikicategory'),
(45, 'Can delete wikicategory', 15, 'delete_wikicategory'),
(46, 'Can add wikipage', 16, 'add_wikipage'),
(47, 'Can change wikipage', 16, 'change_wikipage'),
(48, 'Can delete wikipage', 16, 'delete_wikipage'),
(49, 'Can add list', 17, 'add_list'),
(50, 'Can change list', 17, 'change_list'),
(51, 'Can delete list', 17, 'delete_list'),
(52, 'Can add subscriber', 18, 'add_subscriber'),
(53, 'Can change subscriber', 18, 'change_subscriber'),
(54, 'Can delete subscriber', 18, 'delete_subscriber'),
(55, 'Can add message', 19, 'add_message'),
(56, 'Can change message', 19, 'change_message'),
(57, 'Can delete message', 19, 'delete_message'),
(58, 'Can add attachement', 20, 'add_attachement'),
(59, 'Can change attachement', 20, 'change_attachement'),
(60, 'Can delete attachement', 20, 'delete_attachement'),
(61, 'Can add job', 21, 'add_job'),
(62, 'Can change job', 21, 'change_job'),
(63, 'Can delete job', 21, 'delete_job'),
(64, 'Can add letter', 22, 'add_letter'),
(65, 'Can change letter', 22, 'change_letter'),
(66, 'Can delete letter', 22, 'delete_letter');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`) VALUES
(1, 'admin', '', '', '', 'sha1$9def7$ac62b33d174d6ba716fa7d5fdf3b097be8fcd0fd', 1, 1, 1, '2011-04-22 12:11:38', '2010-12-19 15:53:23'),
(2, 'test', '', '', '', 'sha1$0224f$7bf7d73be0eb1abf79b640104a3abca5d4e0e467', 0, 1, 0, '2011-04-24 16:08:49', '2010-12-19 15:53:23'),
(3, 'susi', '', '', '', 'sha1$27175$502f09eaa9cd497adbaf0a1c82c7d83fa635ac59', 0, 1, 0, '2010-12-19 16:07:41', '2010-12-19 16:07:41'),
(4, 'letterman', '', '', '', 'sha1$456df$7d9153bf6795f76a5177d593b49925a1f953ecfe', 0, 1, 0, '2011-12-24 10:10:10', '2010-12-19 16:42:31'),
(5, 'partyman', '', '', '', 'sha1$9dfa3$f6283db0c0bdaf5efa7544a449e6fad4509cb150', 0, 1, 0, '2011-12-24 10:05:03', '2011-04-22 12:11:59');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 4, 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=23 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'permission', 'auth', 'permission'),
(2, 'group', 'auth', 'group'),
(3, 'user', 'auth', 'user'),
(4, 'message', 'auth', 'message'),
(5, 'content type', 'contenttypes', 'contenttype'),
(6, 'session', 'sessions', 'session'),
(7, 'site', 'sites', 'site'),
(8, 'flat page', 'flatpages', 'flatpage'),
(9, 'log entry', 'admin', 'logentry'),
(10, 'task', 'event', 'task'),
(11, 'event type', 'event', 'eventtype'),
(12, 'event', 'event', 'event'),
(13, 'job', 'event', 'job'),
(14, 'note', 'event', 'note'),
(15, 'wikicategory', 'wiki', 'wikicategory'),
(16, 'wikipage', 'wiki', 'wikipage'),
(17, 'list', 'newsletter', 'list'),
(18, 'subscriber', 'newsletter', 'subscriber'),
(19, 'message', 'newsletter', 'message'),
(20, 'attachement', 'newsletter', 'attachement'),
(21, 'job', 'newsletter', 'job'),
(22, 'letter', 'newsletter', 'letter');

-- --------------------------------------------------------

--
-- Table structure for table `django_flatpage`
--

CREATE TABLE IF NOT EXISTS `django_flatpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `enable_comments` tinyint(1) NOT NULL,
  `template_name` varchar(70) NOT NULL,
  `registration_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_flatpage_a4b49ab` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_flatpage_sites`
--

CREATE TABLE IF NOT EXISTS `django_flatpage_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flatpage_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `flatpage_id` (`flatpage_id`,`site_id`),
  KEY `django_flatpage_sites_dedefef8` (`flatpage_id`),
  KEY `django_flatpage_sites_6223029` (`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('24df8e35f22f145ecb788d394a7a35a8', 'ZWZiN2NiMjY1ZGY3YTY2YTA3MTA5ZmY5MjEzMTMyNmNiMGM2OWZhZjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQR1Lg==\n', '2012-01-07 10:10:10');

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

-- --------------------------------------------------------

--
-- Table structure for table `event_event`
--

CREATE TABLE IF NOT EXISTS `event_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `date` datetime NOT NULL,
  `type_id` int(11) NOT NULL,
  `info` longtext NOT NULL,
  `cron` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `event_event_777d41c8` (`type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `event_event`
--

INSERT INTO `event_event` (`id`, `title`, `date`, `type_id`, `info`, `cron`) VALUES
(1, 'The rocking Testers', '2010-12-15 19:30:00', 1, 'schwer experimentell!', NULL),
(2, 'Chorprobe', '2010-12-21 19:30:00', 2, 'wir singen', NULL),
(3, 'Weihnachten', '2010-12-24 18:00:00', 1, 'das Christkind kommt', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `event_eventtype`
--

CREATE TABLE IF NOT EXISTS `event_eventtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `info` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `event_eventtype`
--

INSERT INTO `event_eventtype` (`id`, `name`, `info`) VALUES
(1, 'Konzert', ''),
(2, 'Chorprobe', ''),
(3, 'externe Veranstaltung', '');

-- --------------------------------------------------------

--
-- Table structure for table `event_eventtype_tasks`
--

CREATE TABLE IF NOT EXISTS `event_eventtype_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eventtype_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `eventtype_id` (`eventtype_id`,`task_id`),
  KEY `event_eventtype_tasks_b2a881ff` (`eventtype_id`),
  KEY `event_eventtype_tasks_c00fe455` (`task_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `event_eventtype_tasks`
--

INSERT INTO `event_eventtype_tasks` (`id`, `eventtype_id`, `task_id`) VALUES
(1, 1, 1),
(3, 1, 2),
(2, 1, 3),
(5, 2, 4),
(4, 2, 5),
(6, 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `event_job`
--

CREATE TABLE IF NOT EXISTS `event_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_job_e9b82f95` (`event_id`),
  KEY `event_job_c00fe455` (`task_id`),
  KEY `event_job_fbfc09f1` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `event_job`
--

INSERT INTO `event_job` (`id`, `event_id`, `task_id`, `user_id`) VALUES
(1, 2, 5, 2),
(2, 3, 2, 2),
(3, 3, 3, 2),
(4, 3, 2, 3),
(5, 3, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `event_note`
--

CREATE TABLE IF NOT EXISTS `event_note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `note` longtext NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_note_e9b82f95` (`event_id`),
  KEY `event_note_fbfc09f1` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `event_task`
--

CREATE TABLE IF NOT EXISTS `event_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `info` longtext NOT NULL,
  `min_persons` int(11) DEFAULT NULL,
  `max_persons` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `event_task`
--

INSERT INTO `event_task` (`id`, `name`, `info`, `min_persons`, `max_persons`) VALUES
(1, 'Koordination', '', 1, 1),
(2, 'Fruehdienst', '', 2, NULL),
(3, 'Spaetdienst', '', 2, NULL),
(4, 'Teilnahme', '', NULL, NULL),
(5, 'Aufsperren', '', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `newsletter_job`
--

CREATE TABLE IF NOT EXISTS `newsletter_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(11) NOT NULL,
  `to_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `sender_id` int(11) NOT NULL,
  `last_delivery` datetime DEFAULT NULL,
  `letters_sent` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `newsletter_job_38373776` (`message_id`),
  KEY `newsletter_job_80e39a0d` (`to_id`),
  KEY `newsletter_job_901f59e9` (`sender_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `newsletter_job`
--

INSERT INTO `newsletter_job` (`id`, `message_id`, `to_id`, `date`, `sender_id`, `last_delivery`, `letters_sent`) VALUES
(1, 1, 2, '2010-12-19 17:03:58', 4, NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `newsletter_letter`
--

CREATE TABLE IF NOT EXISTS `newsletter_letter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `newsletter_letter_751f44ae` (`job_id`),
  KEY `newsletter_letter_fcd09624` (`recipient_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `newsletter_letter`
--

INSERT INTO `newsletter_letter` (`id`, `job_id`, `recipient_id`) VALUES
(1, 1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `newsletter_list`
--

CREATE TABLE IF NOT EXISTS `newsletter_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `praefix` varchar(20) NOT NULL,
  `footer_text` longtext NOT NULL,
  `footer_html` longtext NOT NULL,
  `from_address` varchar(75) NOT NULL,
  `from_bounce_address` varchar(75) NOT NULL,
  `reply_to_address` varchar(75) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `newsletter_list`
--

INSERT INTO `newsletter_list` (`id`, `name`, `praefix`, `footer_text`, `footer_html`, `from_address`, `from_bounce_address`, `reply_to_address`) VALUES
(1, 'Subterrarium', '[subt]', '', '', '', '', ''),
(2, 'Test', '[test]', '', '', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `newsletter_message`
--

CREATE TABLE IF NOT EXISTS `newsletter_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(200) NOT NULL,
  `text` longtext NOT NULL,
  `text_format` varchar(8) NOT NULL,
  `date` date NOT NULL,
  `locked` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `newsletter_message`
--

INSERT INTO `newsletter_message` (`id`, `subject`, `text`, `text_format`, `date`, `locked`) VALUES
(1, 'Testmail', 'Liebe Leute,\r\n\r\nblabla blabl ', 'plain', '2010-12-19', 1),
(2, 'Testmail 2', 'ladadadi ladadada\r\n\r\n* erstens\r\n* zweitens\r\n* drittens', 'textile', '2010-12-19', 0);

-- --------------------------------------------------------

--
-- Table structure for table `newsletter_subscriber`
--

CREATE TABLE IF NOT EXISTS `newsletter_subscriber` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `email` varchar(75) NOT NULL,
  `subscription_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `token` varchar(12) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `newsletter_subscriber_104f5ac1` (`subscription_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `newsletter_subscriber`
--

INSERT INTO `newsletter_subscriber` (`id`, `name`, `email`, `subscription_id`, `date`, `confirmed`, `token`) VALUES
(1, 'Tester', 'test@example.com', 1, '2010-12-19 17:00:50', 1, 'a4b3e44f0701'),
(2, '', 'foo@example.org', 1, '2010-12-19 17:00:50', 1, 'df3c72b3703c'),
(3, '', 'bar@example.org', 1, '2010-12-19 17:00:50', 1, 'a3805ca62d7e'),
(4, '', 'baz@example.org', 1, '2010-12-19 17:00:50', 1, '0d2d1e0c8a24'),
(5, '', 'test@powidl.org', 2, '2010-12-19 17:01:11', 1, '4f1aa36d592f');

-- --------------------------------------------------------

--
-- Table structure for table `wiki_wikicategory`
--

CREATE TABLE IF NOT EXISTS `wiki_wikicategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `wiki_wikicategory`
--

INSERT INTO `wiki_wikicategory` (`id`, `name`) VALUES
(1, 'Anleitungen'),
(2, 'Booking');

-- --------------------------------------------------------

--
-- Table structure for table `wiki_wikipage`
--

CREATE TABLE IF NOT EXISTS `wiki_wikipage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `content` longtext NOT NULL,
  `content_html` longtext NOT NULL,
  `last_changed` datetime NOT NULL,
  `author_id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `wiki_wikipage_cc846901` (`author_id`),
  KEY `wiki_wikipage_42dc49bc` (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `wiki_wikipage`
--

INSERT INTO `wiki_wikipage` (`id`, `title`, `content`, `content_html`, `last_changed`, `author_id`, `category_id`) VALUES
(1, 'Test-Page', 'this is a test', '	<p>this is a test</p>', '2011-04-24 16:09:16', 2, 1);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attachment_attachment`
--
ALTER TABLE `attachment_attachment`
  ADD CONSTRAINT `content_type_id_refs_id_4ac47ba8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_flatpage_sites`
--
ALTER TABLE `django_flatpage_sites`
  ADD CONSTRAINT `flatpage_id_refs_id_c0e84f5a` FOREIGN KEY (`flatpage_id`) REFERENCES `django_flatpage` (`id`),
  ADD CONSTRAINT `site_id_refs_id_4e3eeb57` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`);

--
-- Constraints for table `event_event`
--
ALTER TABLE `event_event`
  ADD CONSTRAINT `type_id_refs_id_ede229ab` FOREIGN KEY (`type_id`) REFERENCES `event_eventtype` (`id`);

--
-- Constraints for table `event_eventtype_tasks`
--
ALTER TABLE `event_eventtype_tasks`
  ADD CONSTRAINT `eventtype_id_refs_id_42251296` FOREIGN KEY (`eventtype_id`) REFERENCES `event_eventtype` (`id`),
  ADD CONSTRAINT `task_id_refs_id_52e65dba` FOREIGN KEY (`task_id`) REFERENCES `event_task` (`id`);

--
-- Constraints for table `event_job`
--
ALTER TABLE `event_job`
  ADD CONSTRAINT `event_id_refs_id_da409d08` FOREIGN KEY (`event_id`) REFERENCES `event_event` (`id`),
  ADD CONSTRAINT `task_id_refs_id_2e40f4e8` FOREIGN KEY (`task_id`) REFERENCES `event_task` (`id`),
  ADD CONSTRAINT `user_id_refs_id_bac64249` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `event_note`
--
ALTER TABLE `event_note`
  ADD CONSTRAINT `event_id_refs_id_3ee6c820` FOREIGN KEY (`event_id`) REFERENCES `event_event` (`id`),
  ADD CONSTRAINT `user_id_refs_id_e9805eff` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `newsletter_job`
--
ALTER TABLE `newsletter_job`
  ADD CONSTRAINT `to_id_refs_id_de8b7923` FOREIGN KEY (`to_id`) REFERENCES `newsletter_list` (`id`),
  ADD CONSTRAINT `message_id_refs_id_998976d5` FOREIGN KEY (`message_id`) REFERENCES `newsletter_message` (`id`),
  ADD CONSTRAINT `sender_id_refs_id_f10d7263` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `newsletter_letter`
--
ALTER TABLE `newsletter_letter`
  ADD CONSTRAINT `job_id_refs_id_ec82bbf1` FOREIGN KEY (`job_id`) REFERENCES `newsletter_job` (`id`),
  ADD CONSTRAINT `recipient_id_refs_id_a4ec1c51` FOREIGN KEY (`recipient_id`) REFERENCES `newsletter_subscriber` (`id`);

--
-- Constraints for table `newsletter_subscriber`
--
ALTER TABLE `newsletter_subscriber`
  ADD CONSTRAINT `subscription_id_refs_id_50f52003` FOREIGN KEY (`subscription_id`) REFERENCES `newsletter_list` (`id`);

--
-- Constraints for table `wiki_wikipage`
--
ALTER TABLE `wiki_wikipage`
  ADD CONSTRAINT `author_id_refs_id_b9a5b28f` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `category_id_refs_id_4ccaafc2` FOREIGN KEY (`category_id`) REFERENCES `wiki_wikicategory` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
