# scrapy-grap-joke
A source code to  grap jokes from a  joke site.
The code use scrapy framework ,so if you want to let it work ,you should install scrapy.
The database is my local database .  You should create your own database, and change the setting.py and the db configure.
There is only one table in the database . In my project , it calls joke_detail. the sql is :

CREATE TABLE `joke_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'primary key id',
  `origin` varchar(100) NOT NULL COMMENT 'source',
  `type` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '1' COMMENT 'type',
  `title` varchar(100) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'title',
  `content` text CHARACTER SET utf8 NOT NULL COMMENT 'content',
  `url` varchar(150) NOT NULL DEFAULT '' COMMENT 'url',
  `ctime` char(14) NOT NULL DEFAULT '' COMMENT 'create time ',
  `grap_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'grap time',
  `is_used` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'whether used',
  `is_star` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'whether star',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8
