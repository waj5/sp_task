from typing import List

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> List[str]:
    return [
        """CREATE TABLE IF NOT EXISTS `users` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `password` VARCHAR(128) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `is_admin` BOOL NOT NULL  DEFAULT 0,
    `role` VARCHAR(20) NOT NULL  DEFAULT 'administered',
    UNIQUE KEY `uid_users_name_6aafa3` (`name`),
    UNIQUE KEY `uid_users_email_133a6f` (`email`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `master` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `user_id` CHAR(36) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `administered` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `master_id` CHAR(36),
    `user_id` CHAR(36) NOT NULL UNIQUE,
    CONSTRAINT `fk_administ_master_2188a11a` FOREIGN KEY (`master_id`) REFERENCES `master` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_administ_users_ed8cf2de` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `masters_administered` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `administered_id` CHAR(36) NOT NULL,
    `master_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_masters__administ_ce7719ed` FOREIGN KEY (`administered_id`) REFERENCES `administered` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_masters__master_97798cfd` FOREIGN KEY (`master_id`) REFERENCES `master` (`id`) ON DELETE CASCADE,
    KEY `idx_masters_adm_master__2b21c7` (`master_id`, `administered_id`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `task` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL,
    `content` LONGTEXT NOT NULL,
    `status` VARCHAR(20) NOT NULL  DEFAULT '未完成',
    `create_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `creator_id` CHAR(36) NOT NULL,
    `designee_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_task_users_50743fb0` FOREIGN KEY (`creator_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_task_users_1bd6f182` FOREIGN KEY (`designee_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""
    ]


async def downgrade(db: BaseDBAsyncClient) -> List[str]:
    return [
        
    ]
