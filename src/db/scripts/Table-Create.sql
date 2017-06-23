/*================================================================================*/
/* DDL SCRIPT                                                                     */
/*================================================================================*/
/*  Title    : Padification DataBase                                              */
/*  FileName : PADification database schema.ecm                                   */
/*  Platform : SQL Server 2014                                                    */
/*  Version  : 0.01                                                               */
/*  Date     : June 21, 2017                                                      */
/*================================================================================*/
--Revision History
--June 22, 2017 - Integrated Drop table functions from Table-Drop.sql.

USE PADification
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


USE PADification
/*================================================================================*/
/* CREATE TABLES                                                                  */
/*================================================================================*/

CREATE TABLE PADification.dbo.LatentSkill (
  LatentSkillName VARCHAR(50) NOT NULL,
  LatentSkillDesc VARCHAR(MAX) NOT NULL,
  LSSlotsReq INT NOT NULL,
  CONSTRAINT PK_LatentSkill PRIMARY KEY (LatentSkillName)
)
GO

CREATE TABLE PADification.dbo.MonsterType (
  MonsterTypeName VARCHAR(50) NOT NULL,
  CONSTRAINT PK_MonsterType PRIMARY KEY (MonsterTypeName)
)
GO

CREATE TABLE PADification.dbo.Attribute (
  AttributeName VARCHAR(50) NOT NULL,
  CONSTRAINT PK_Attribute PRIMARY KEY (AttributeName)
)
GO

CREATE TABLE PADification.dbo.ActiveSkill (
  ActiveSkillName NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CS_AS NOT NULL,
  ActiveSkillDesc NVARCHAR(MAX) NOT NULL,
  ActiveSkillMaxLevel INT NOT NULL,
  ActiveSkillMaxCoolDown INT NOT NULL,
  CONSTRAINT PK_ActiveSkill PRIMARY KEY (ActiveSkillName)
)
GO

CREATE TABLE PADification.dbo.LeaderSkill (
  LeaderSkillName NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CS_AS NOT NULL,
  LeaderSkillDesc NVARCHAR(MAX) NOT NULL,
  CONSTRAINT PK_LeaderSkill PRIMARY KEY (LeaderSkillName)
)
GO

CREATE TABLE PADification.dbo.AwokenSkill (
  AwokenSkillName VARCHAR(100) NOT NULL,
  AwokenSkillDesc VARCHAR(MAX) NOT NULL,
  CONSTRAINT PK_AwokenSkill PRIMARY KEY (AwokenSkillName)
)
GO

CREATE TABLE PADification.dbo.AwokenSkillList (
  ASListID INT NOT NULL,
  AwokenSkillOne VARCHAR(100) NULL,
  AwokenSkillTwo VARCHAR(100) NULL,
  AwokenSkillThree VARCHAR(100) NULL,
  AwokenSkillFour VARCHAR(100) NULL,
  AwokenSkillFive VARCHAR(100) NULL,
  AwokenSkillSix VARCHAR(100) NULL,
  AwokenSkillSeven VARCHAR(100) NULL,
  AwokenSkillEight VARCHAR(100) NULL,
  AwokenSkillNine VARCHAR(100) NULL,
  CONSTRAINT PK_AwokenSkillList PRIMARY KEY (ASListID)
)
GO

CREATE TABLE PADification.dbo.MonsterClass (
  MonsterClassID INT NOT NULL,
  MonsterName NVARCHAR(100) NOT NULL,
  Rarity INT NOT NULL,
  PriAttribute VARCHAR(50) NOT NULL,
  SecAttribute VARCHAR(50) NULL,
  MonsterTypeOne VARCHAR(50) NOT NULL,
  MonsterTypeTwo VARCHAR(50) NULL,
  MonsterTypeThree VARCHAR(50) NULL,
  ExpCurve INT NOT NULL,
  MaxLevel INT NOT NULL,
  MonsterCost INT NOT NULL,
  ASListID INT NULL,
  LeaderSkillName NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CS_AS NULL,
  ActiveSkillName NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CS_AS NULL,
  MaxHP INT NOT NULL,
  MinHP INT NOT NULL,
  GrowthRateHP REAL NOT NULL,
  MaxATK INT NOT NULL,
  MinATK INT NOT NULL,
  GrowthRateATK REAL NOT NULL,
  MaxRCV INT NOT NULL,
  MinRCV INT NOT NULL,
  GrowthRateRCV REAL NOT NULL,
  CurSell INT NOT NULL,
  CurFodder INT NOT NULL,
  MonsterPointValue INT,
  LSSlots INT DEFAULT 5 NOT NULL,
  CONSTRAINT PK_MonsterClass PRIMARY KEY (MonsterClassID)
)
GO

CREATE TABLE PADification.dbo.EvolutionTree (
  EvoID INT IDENTITY(1,1) NOT NULL,
  NextMonsterID INT NOT NULL,
  BaseMonsterID INT NOT NULL,
  EvoMaterialIDOne INT,
  EvoMaterialIDTwo INT,
  EvoMaterialIDThree INT,
  EvoMaterialIDFour INT,
  EvoMaterialIDFive INT,
  Ultimate BIT NOT NULL,
  CONSTRAINT PK_EvolutionTree PRIMARY KEY (EvoID)
)
GO

CREATE TABLE PADification.dbo.Player (
  PlayerID INT NOT NULL,
  Password VARCHAR(10) NOT NULL,
  Email VARCHAR(50),
  Username VARCHAR(15) NOT NULL,
  CONSTRAINT PK_Player PRIMARY KEY (UserName)
)
GO

CREATE TABLE PADification.dbo.LatentSkillList (
  InstanceID INT NOT NULL,
  LatentSkillOne VARCHAR(50) NOT NULL,
  LatentSkillTwo VARCHAR(50) NOT NULL,
  LatentSkillThree VARCHAR(50) NOT NULL,
  LatentSkillFour VARCHAR(50) NOT NULL,
  LatentSkillFive VARCHAR(50) NOT NULL,
  LatentSkillSix VARCHAR(50) NOT NULL,
  ExtraSlot BIT NOT NULL,
  CONSTRAINT PK_LatentSkillList PRIMARY KEY (InstanceID)
)
GO

CREATE TABLE PADification.dbo.MonsterInstance (
  InstanceID INT NOT NULL,
  Username VARCHAR(15) NOT NULL,
  MonsterClassID INT NOT NULL,
  CurrentExperience INT NOT NULL,
  PlusATK INT NOT NULL,
  PlusRCV INT NOT NULL,
  PlusHP INT NOT NULL,
  SkillsAwoke INT NOT NULL,
  AssistMonsterID INT,
  SkillLevel INT,
  LSListID INT NOT NULL,
  CONSTRAINT PK_MonsterInstance PRIMARY KEY (InstanceID)
)
GO

CREATE TABLE PADification.dbo.AwokenBadge (
  AwokenBadgeName VARCHAR(50) NOT NULL,
  AwokenBadgeDesc VARCHAR(MAX) NOT NULL,
  CONSTRAINT PK_AwokenBadge PRIMARY KEY (AwokenBadgeName)
)
GO

CREATE TABLE PADification.dbo.Team (
  TeamInstanceID INT NOT NULL,
  Username VARCHAR(15) NOT NULL,
  TeamName VARCHAR(50),
  LeaderMonster INT NOT NULL,
  SubMonsterOne INT NOT NULL,
  SubMonsterTwo INT NOT NULL,
  SubMonsterThree INT NOT NULL,
  SubMonsterFour INT NOT NULL,
  BadgeName VARCHAR(50) NOT NULL,
  CONSTRAINT PK_Team PRIMARY KEY (TeamInstanceID)
)
GO

/*================================================================================*/
/* CREATE FOREIGN KEYS                                                            */
/*================================================================================*/

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill
  FOREIGN KEY (AwokenSkillOne) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill2
  FOREIGN KEY (AwokenSkillTwo) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill3
  FOREIGN KEY (AwokenSkillThree) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill4
  FOREIGN KEY (AwokenSkillFour) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill5
  FOREIGN KEY (AwokenSkillFive) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill6
  FOREIGN KEY (AwokenSkillSix) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill7
  FOREIGN KEY (AwokenSkillSeven) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill8
  FOREIGN KEY (AwokenSkillEight) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE AwokenSkillList
  ADD CONSTRAINT FK_AwokenSkillList_AwokenSkill9
  FOREIGN KEY (AwokenSkillNine) REFERENCES AwokenSkill (AwokenSkillName)
GO

ALTER TABLE MonsterClass
  ADD CONSTRAINT FK_MonsterClass_ActiveSkill
  FOREIGN KEY (ActiveSkillName) REFERENCES ActiveSkill (ActiveSkillName)
GO

ALTER TABLE MonsterClass
  ADD CONSTRAINT FK_MonsterClass_LeaderSkill
  FOREIGN KEY (LeaderSkillName) REFERENCES LeaderSkill (LeaderSkillName)
GO

ALTER TABLE MonsterClass
  ADD CONSTRAINT FK_MonsterClass_MonsterType
  FOREIGN KEY (MonsterTypeOne) REFERENCES MonsterType (MonsterTypeName)
GO

ALTER TABLE MonsterClass
  ADD CONSTRAINT FK_MonsterClass_MonsterType2
  FOREIGN KEY (MonsterTypeTwo) REFERENCES MonsterType (MonsterTypeName)
GO

ALTER TABLE MonsterClass
  ADD CONSTRAINT FK_MonsterClass_MonsterType3
  FOREIGN KEY (MonsterTypeThree) REFERENCES MonsterType (MonsterTypeName)
GO

ALTER TABLE MonsterClass
  ADD CONSTRAINT FK_MonsterClass_Attribute
  FOREIGN KEY (PriAttribute) REFERENCES Attribute (AttributeName)
GO

ALTER TABLE MonsterClass
  ADD CONSTRAINT FK_MonsterClass_Attribute2
  FOREIGN KEY (SecAttribute) REFERENCES Attribute (AttributeName)
GO

ALTER TABLE MonsterClass
  ADD CONSTRAINT FK_MonsterClass_AwokenSkillList
  FOREIGN KEY (ASListID) REFERENCES AwokenSkillList (ASListID)
GO

ALTER TABLE EvolutionTree
  ADD CONSTRAINT FK_EvolutionTree_MonsterClass
  FOREIGN KEY (BaseMonsterID) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE EvolutionTree
  ADD CONSTRAINT FK_EvolutionTree_MonsterClass2
  FOREIGN KEY (EvoMaterialIDOne) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE EvolutionTree
  ADD CONSTRAINT FK_EvolutionTree_MonsterClass3
  FOREIGN KEY (EvoMaterialIDTwo) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE EvolutionTree
  ADD CONSTRAINT FK_EvolutionTree_MonsterClass4
  FOREIGN KEY (EvoMaterialIDThree) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE EvolutionTree
  ADD CONSTRAINT FK_EvolutionTree_MonsterClass5
  FOREIGN KEY (EvoMaterialIDFour) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE EvolutionTree
  ADD CONSTRAINT FK_EvolutionTree_MonsterClass6
  FOREIGN KEY (EvoMaterialIDFive) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE EvolutionTree
  ADD CONSTRAINT FK_EvolutionTree_MonsterClass7
  FOREIGN KEY (NextMonsterID) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE LatentSkillList
  ADD CONSTRAINT FK_LatentSkillList_LatentSkill
  FOREIGN KEY (LatentSkillOne) REFERENCES LatentSkill (LatentSkillName)
GO

ALTER TABLE LatentSkillList
  ADD CONSTRAINT FK_LatentSkillList_LatentSkill2
  FOREIGN KEY (LatentSkillTwo) REFERENCES LatentSkill (LatentSkillName)
GO

ALTER TABLE LatentSkillList
  ADD CONSTRAINT FK_LatentSkillList_LatentSkill3
  FOREIGN KEY (LatentSkillThree) REFERENCES LatentSkill (LatentSkillName)
GO

ALTER TABLE LatentSkillList
  ADD CONSTRAINT FK_LatentSkillList_LatentSkill4
  FOREIGN KEY (LatentSkillFour) REFERENCES LatentSkill (LatentSkillName)
GO

ALTER TABLE LatentSkillList
  ADD CONSTRAINT FK_LatentSkillList_LatentSkill5
  FOREIGN KEY (LatentSkillFive) REFERENCES LatentSkill (LatentSkillName)
GO

ALTER TABLE LatentSkillList
  ADD CONSTRAINT FK_LatentSkillList_LatentSkill6
  FOREIGN KEY (LatentSkillSix) REFERENCES LatentSkill (LatentSkillName)
GO

ALTER TABLE MonsterInstance
  ADD CONSTRAINT FK_MonsterInstance_MonsterClass
  FOREIGN KEY (MonsterClassID) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE MonsterInstance
  ADD CONSTRAINT FK_MonsterInstance_Player
  FOREIGN KEY (Username) REFERENCES Player (UserName)
GO

ALTER TABLE MonsterInstance
  ADD CONSTRAINT FK_MonsterInstance_LatentSkillList
  FOREIGN KEY (LSListID) REFERENCES LatentSkillList (InstanceID)
GO

ALTER TABLE Team
  ADD CONSTRAINT FK_Team_Player
  FOREIGN KEY (Username) REFERENCES Player (UserName)
GO

ALTER TABLE Team
  ADD CONSTRAINT FK_Team_Badge
  FOREIGN KEY (BadgeName) REFERENCES AwokenBadge (AwokenBadgeName)
GO

ALTER TABLE Team
  ADD CONSTRAINT FK_Team_MonsterClass
  FOREIGN KEY (LeaderMonster) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE Team
  ADD CONSTRAINT FK_Team_MonsterClass2
  FOREIGN KEY (SubMonsterOne) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE Team
  ADD CONSTRAINT FK_Team_MonsterClass3
  FOREIGN KEY (SubMonsterTwo) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE Team
  ADD CONSTRAINT FK_Team_MonsterClass4
  FOREIGN KEY (SubMonsterThree) REFERENCES MonsterClass (MonsterClassID)
GO

ALTER TABLE Team
  ADD CONSTRAINT FK_Team_MonsterClass5
  FOREIGN KEY (SubMonsterFour) REFERENCES MonsterClass (MonsterClassID)
GO
