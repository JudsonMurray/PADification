/*================================================================================*/
/* DDL SCRIPT                                                                     */
/*================================================================================*/
/*  Title    : Padification DataBase                                              */
/*  FileName : PADification database schema.ecm                                   */
/*  Platform : SQL Server 2014                                                    */
/*  Version  : 1.0																  */
/*  Date     : June 22, 2017                                                      */
/*================================================================================*/
--Revision History
--June 22, 2017 - Reformating groups of table drops and order in which tables should be dropped.


USE PADification
/*================================================================================*/
/* DROP FOREIGN KEYS                                                              */
/*================================================================================*/

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill
--GO

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill2
--GO

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill3
--GO

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill4
--GO

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill5
--GO

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill6
--GO

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill7
--GO

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill8
--GO

--ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill9
--GO

--ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_ActiveSkill
--GO

--ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_LeaderSkill
--GO

--ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_MonsterType
--GO

--ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_MonsterType2
--GO

--ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_MonsterType3
--GO

--ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_Attribute
--GO

--ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_Attribute2
--GO

--ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_AwokenSkillList
--GO

--ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass
--GO

--ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass2
--GO

--ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass3
--GO

--ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass4
--GO

--ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass5
--GO

--ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass6
--GO

--ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill
--GO

--ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill2
--GO

--ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill3
--GO

--ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill4
--GO

--ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill5
--GO

--ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill6
--GO

--ALTER TABLE MonsterInstance DROP CONSTRAINT FK_MonsterInstance_MonsterClass
--GO

--ALTER TABLE MonsterInstance DROP CONSTRAINT FK_MonsterInstance_Player
--GO

--ALTER TABLE MonsterInstance DROP CONSTRAINT FK_MonsterInstance_LatentSkillList
--GO

--ALTER TABLE Team DROP CONSTRAINT FK_Team_Player
--GO

--ALTER TABLE Team DROP CONSTRAINT FK_Team_Badge
--GO

--ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass
--GO

--ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass2
--GO

--ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass3
--GO

--ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass4
--GO

--ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass5
--GO

/*================================================================================*/
/* DROP TABLES                                                                    */
/*================================================================================*/

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
