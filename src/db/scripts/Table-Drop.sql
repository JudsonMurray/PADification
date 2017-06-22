/*================================================================================*/
/* DDL SCRIPT                                                                     */
/*================================================================================*/
/*  Title    : Padification DataBase                                              */
/*  FileName : PADification database schema.ecm                                   */
/*  Platform : SQL Server 2014                                                    */
/*  Version  : 0.01                                                               */
/*  Date     : June 21, 2017                                                      */
/*================================================================================*/
USE PADification
/*================================================================================*/
/* DROP FOREIGN KEYS                                                              */
/*================================================================================*/

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill2
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill3
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill4
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill5
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill6
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill7
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill8
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT FK_AwokenSkillList_AwokenSkill9
GO

ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_ActiveSkill
GO

ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_LeaderSkill
GO

ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_MonsterType
GO

ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_MonsterType2
GO

ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_MonsterType3
GO

ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_Attribute
GO

ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_Attribute2
GO

ALTER TABLE MonsterClass DROP CONSTRAINT FK_MonsterClass_AwokenSkillList
GO

ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass
GO

ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass2
GO

ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass3
GO

ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass4
GO

ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass5
GO

ALTER TABLE EvolutionTree DROP CONSTRAINT FK_EvolutionTree_MonsterClass6
GO

ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill
GO

ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill2
GO

ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill3
GO

ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill4
GO

ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill5
GO

ALTER TABLE LatentSkillList DROP CONSTRAINT FK_LatentSkillList_LatentSkill6
GO

ALTER TABLE MonsterInstance DROP CONSTRAINT FK_MonsterInstance_MonsterClass
GO

ALTER TABLE MonsterInstance DROP CONSTRAINT FK_MonsterInstance_Player
GO

ALTER TABLE MonsterInstance DROP CONSTRAINT FK_MonsterInstance_LatentSkillList
GO

ALTER TABLE Team DROP CONSTRAINT FK_Team_Player
GO

ALTER TABLE Team DROP CONSTRAINT FK_Team_Badge
GO

ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass
GO

ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass2
GO

ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass3
GO

ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass4
GO

ALTER TABLE Team DROP CONSTRAINT FK_Team_MonsterClass5
GO

/*================================================================================*/
/* DROP TABLES                                                                    */
/*================================================================================*/

ALTER TABLE ActiveSkill DROP CONSTRAINT PK_ActiveSkill
GO

DROP TABLE ActiveSkill
GO

ALTER TABLE Attribute DROP CONSTRAINT PK_Attribute
GO

DROP TABLE Attribute
GO

ALTER TABLE AwokenBadge DROP CONSTRAINT PK_AwokenBadge
GO

DROP TABLE AwokenBadge
GO

ALTER TABLE AwokenSkill DROP CONSTRAINT PK_AwokenSkill
GO

DROP TABLE AwokenSkill
GO

ALTER TABLE AwokenSkillList DROP CONSTRAINT PK_AwokenSkillList
GO

DROP TABLE AwokenSkillList
GO

ALTER TABLE LeaderSkill DROP CONSTRAINT PK_LeaderSkill
GO

DROP TABLE LeaderSkill
GO

ALTER TABLE MonsterType DROP CONSTRAINT PK_MonsterType
GO

DROP TABLE MonsterType
GO

ALTER TABLE MonsterClass DROP CONSTRAINT PK_MonsterClass
GO

DROP TABLE MonsterClass
GO

ALTER TABLE EvolutionTree DROP CONSTRAINT PK_EvolutionTree
GO

DROP TABLE EvolutionTree
GO

ALTER TABLE LatentSkill DROP CONSTRAINT PK_LatentSkill
GO

DROP TABLE LatentSkill
GO

ALTER TABLE LatentSkillList DROP CONSTRAINT PK_LatentSkillList
GO

DROP TABLE LatentSkillList
GO

ALTER TABLE Player DROP CONSTRAINT PK_Player
GO

DROP TABLE Player
GO

ALTER TABLE MonsterInstance DROP CONSTRAINT PK_MonsterInstance
GO

DROP TABLE MonsterInstance
GO

ALTER TABLE Team DROP CONSTRAINT PK_Team
GO

DROP TABLE Team
GO
