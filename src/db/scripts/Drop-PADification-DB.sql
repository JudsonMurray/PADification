--PADification Databse Delete script--
--REVISION HISTORY
--July 6, 2017 - Initial creation of this script (V.1.0)

use PADification
--Drop Team table
if OBJECT_ID('PADification.dbo.Team', 'U') is not null
	ALTER TABLE Team DROP CONSTRAINT PK_Team
	GO
	DROP TABLE Team;
	GO

--Drop Awoken Badge table
if OBJECT_ID('PADification.dbo.AwokenBadge', 'U') is not null
	ALTER TABLE AwokenBadge DROP CONSTRAINT PK_AwokenBadge
	GO
	DROP TABLE AwokenBadge;
	GO

--Drop Monster Instance table
if OBJECT_ID('PADification.dbo.MonsterInstance', 'U') is not null
	ALTER TABLE MonsterInstance DROP CONSTRAINT PK_MonsterInstance
	GO
	DROP TABLE MonsterInstance;
	GO

--Drop Latent Skill List table
if OBJECT_ID('PADification.dbo.LatentSkillList', 'U') is not null
	ALTER TABLE LatentSkillList DROP CONSTRAINT PK_LatentSkillList
	GO
	DROP TABLE LatentSkillList;
	GO

--v.0.03
--Drop Follower table
if OBJECT_ID('PADification.dbo.Follower', 'U') is not null
	ALTER TABLE Follower DROP CONSTRAINT PK_Follower
	GO
	DROP TABLE Follower;
	GO

--Drop Player table
if OBJECT_ID('PADification.dbo.Player', 'U') is not null
	ALTER TABLE Player DROP CONSTRAINT PK_Player
	GO
	DROP TABLE Player;
	GO

--Drop Evolution Tree table
if OBJECT_ID('PADification.dbo.EvolutionTree', 'U') is not null
	ALTER TABLE EvolutionTree DROP CONSTRAINT PK_EvolutionTree
	GO
	DROP TABLE EvolutionTree;
	GO

--Drop Monster Class table
if OBJECT_ID('PADification.dbo.MonsterClass', 'U') is not null
	ALTER TABLE MonsterClass DROP CONSTRAINT PK_MonsterClass
	GO
	DROP TABLE MonsterClass;
	GO

--Drop Monster Type table
if OBJECT_ID('PADification.dbo.MonsterType', 'U') is not null
	ALTER TABLE MonsterType DROP CONSTRAINT PK_MonsterType
	GO
	DROP TABLE MonsterType;
	GO

--Drop Attribute table
if OBJECT_ID('PADification.dbo.Attribute', 'U') is not null
	ALTER TABLE Attribute DROP CONSTRAINT PK_Attribute
	GO
	DROP TABLE Attribute;
	GO

--Drop Active Skill table
if OBJECT_ID('PADification.dbo.Team', 'U') is not null
	ALTER TABLE ActiveSkill DROP CONSTRAINT PK_ActiveSkill
	GO
	DROP TABLE ActiveSkill;
	GO

--Drop Leader Skill table
if OBJECT_ID('PADification.dbo.LeaderSkill', 'U') is not null
	ALTER TABLE LeaderSkill DROP CONSTRAINT PK_LeaderSkill
	GO
	DROP TABLE LeaderSkill;
	GO

--Drop Awoken Skill List table
if OBJECT_ID('PADification.dbo.AwokenSkillList', 'U') is not null
	ALTER TABLE AwokenSkillList DROP CONSTRAINT PK_AwokenSkillList
	GO
	DROP TABLE AwokenSkillList;
	GO

--Drop Awoken Skill table
if OBJECT_ID('PADification.dbo.AwokenSkill', 'U') is not null
	ALTER TABLE AwokenSkill DROP CONSTRAINT PK_AwokenSkill
	GO
	DROP TABLE AwokenSkill;
	GO

--Drop Latent Skill table
if OBJECT_ID('PADification.dbo.LatentSkill', 'U') is not null
	ALTER TABLE LatentSkill DROP CONSTRAINT PK_LatentSkill
	GO
	DROP TABLE LatentSkill;
	GO

--Removed from v.0.06
----v.0.02
----Drop Monster Tags List table
--if OBJECT_ID('PADification.dbo.MonsterTagsList', 'U') is not null
--	ALTER TABLE MonsterTagsList DROP CONSTRAINT PK_MonsterTagsList
--	GO
--	DROP TABLE MonsterTagsList;
--	GO

--Removed from v.0.06
----v.0.02
----Drop Monster Tags table
--if OBJECT_ID('PADification.dbo.MonsterTags', 'U') is not null
--	ALTER TABLE MonsterTags DROP CONSTRAINT PK_MonsterTags
--	GO
--	DROP TABLE MonsterTags;
--	GO

--Removed from v.0.06
----v.0.02
----Drop Team Tags List table
--if OBJECT_ID('PADification.dbo.TeamTagsList', 'U') is not null
--	ALTER TABLE TeamTagsList DROP CONSTRAINT PK_TeamTagsList
--	GO
--	DROP TABLE TeamTagsList;
--	GO

--Removed from v.0.06
----v.0.02
----Drop Team Tags table
--if OBJECT_ID('PADification.dbo.TeamTags', 'U') is not null
--	ALTER TABLE TeamTags DROP CONSTRAINT PK_TeamTags
--	GO
--	DROP TABLE TeamTags;
--	GO

USE MASTER

--Drop PADification Database
if DB_ID('PADification') is not null
	 Use Master
	 drop database PADification;
	 GO	 

print 'complete'