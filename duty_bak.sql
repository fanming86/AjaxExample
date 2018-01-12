/*
SQLyog Enterprise v12.09 (64 bit)
MySQL - 5.7.20-log 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `du_user` (
	`user_id` int (11),
	`username` varchar (192),
	`phone` varchar (48),
	`password` varchar (192),
	`create_time` int (11)
); 
insert into `du_user` (`user_id`, `username`, `phone`, `password`, `create_time`) values('1','zzz','111','123',NULL);
insert into `du_user` (`user_id`, `username`, `phone`, `password`, `create_time`) values('136','qwe','222','123','1513819105');


create table `du_duty` (
	`duty_id` int (11),
	`category_id` int (11),
	`user_id` int (11),
	`title` varchar (3072),
	`status` int (2),
	`is_show` int (2),
	`create_time` int (11)
); 
insert into `du_duty` (`duty_id`, `category_id`, `user_id`, `title`, `status`, `is_show`, `create_time`) values('1','7','16','test','1','1','1513567322');


create table `du_category` (
	`category_id` int (11),
	`name` varchar (192)
); 
insert into `du_category` (`category_id`, `name`) values('7','test');
