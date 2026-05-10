CREATE TABLE `agents` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`description` text,
	`status` enum('active','inactive','suspended') NOT NULL DEFAULT 'active',
	`reputationScore` int NOT NULL DEFAULT 0,
	`totalJobsCompleted` int NOT NULL DEFAULT 0,
	`totalVolumeSettled` varchar(255) NOT NULL DEFAULT '0',
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `agents_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `jobs` (
	`id` int AUTO_INCREMENT NOT NULL,
	`agentId` int NOT NULL,
	`title` varchar(255) NOT NULL,
	`description` text,
	`status` enum('pending','executing','completed','failed','settled') NOT NULL DEFAULT 'pending',
	`inputData` text,
	`outputData` text,
	`executionTime` int,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`completedAt` timestamp,
	`settledAt` timestamp,
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `jobs_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `metrics` (
	`id` int AUTO_INCREMENT NOT NULL,
	`totalSettlements` int NOT NULL DEFAULT 0,
	`registeredAgents` int NOT NULL DEFAULT 0,
	`volumeTransacted` varchar(255) NOT NULL DEFAULT '0',
	`networkStatus` enum('online','degraded','offline') NOT NULL DEFAULT 'online',
	`averageSettlementTime` int NOT NULL DEFAULT 0,
	`successRate` varchar(10) NOT NULL DEFAULT '0',
	`timestamp` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `metrics_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `settlements` (
	`id` int AUTO_INCREMENT NOT NULL,
	`jobId` int NOT NULL,
	`agentId` int NOT NULL,
	`amount` varchar(255) NOT NULL,
	`currency` varchar(10) NOT NULL DEFAULT 'USDC',
	`blockchainNetwork` varchar(100) NOT NULL,
	`transactionHash` varchar(255),
	`status` enum('pending','confirmed','failed','settled') NOT NULL DEFAULT 'pending',
	`gasUsed` varchar(255),
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`confirmedAt` timestamp,
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `settlements_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
ALTER TABLE `agents` ADD CONSTRAINT `agents_userId_users_id_fk` FOREIGN KEY (`userId`) REFERENCES `users`(`id`) ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `jobs` ADD CONSTRAINT `jobs_agentId_agents_id_fk` FOREIGN KEY (`agentId`) REFERENCES `agents`(`id`) ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `settlements` ADD CONSTRAINT `settlements_jobId_jobs_id_fk` FOREIGN KEY (`jobId`) REFERENCES `jobs`(`id`) ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `settlements` ADD CONSTRAINT `settlements_agentId_agents_id_fk` FOREIGN KEY (`agentId`) REFERENCES `agents`(`id`) ON DELETE no action ON UPDATE no action;