
DROP TABLE IF EXISTS `t_position_info`;

CREATE TABLE `t_position_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pos_name` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `area` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `salary` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1631 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
