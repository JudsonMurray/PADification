-- Evolution Tree inserts--
--Intial Creation by William Gale--
--April 21, 2017

--V 1.0 --Billy's EvoTree Added
--V 1.0 --Kyle's EvoTree Added
--V 1.1 --Elie's EvolTree Added April 21 2017

USE PADification

--Billy's
INSERT INTO PADification.dbo.EvolutionTree
(NextMonsterID, BaseMonsterID, EvoMaterialIDOne, EvoMaterialIDTwo, EvoMaterialIDThree, EvoMaterialIDFour, EvoMaterialIDFive, MinLevel, Devolveable, LevelReset)
VALUES
-- Evolution Tree for Orange DragonBound, Saria
(2441, 2440, 150, 321, 174, 246, 251, 50, 0, 1),
-- Evolution Tree for Andromeda
(1068, 1067, 148, 321, 172, 247, 247, 50, 0, 1),
(1733, 1068, 321, 1294, 1294, 247, 251, 1, 1, 0),
(2658, 1733, 1324, 148, 1294, 1326, 1326, 1, 1, 0)

--Kyle's
INSERT INTO PADification.dbo.EvolutionTree
(NextMonsterID, BaseMonsterID, EvoMaterialIDOne, EvoMaterialIDTwo, EvoMaterialIDThree, EvoMaterialIDFour, EvoMaterialIDFive, MinLevel, Devolveable, LevelReset)
Values
--Phantom God, Odin Tree
(1108, 1107, 321, 171, 234, 246, 251, 50, 0,1), 
(2179, 1108, 147, 321, 246, 250, 251, 1, 1,0),
(3392, 1108, 147, 1085, 1085, 1085, 246, 1, 1, 0),
--Castor Tree
(2424,2423, 151, 175, 250, 247, 251, 50, 0, 1),
(3061,2424, 151, 1176, 234, 250, 247, 1, 1, 0),
(3062, 2424,151, 1176, 234, 250, 249, 1, 1, 0)

--Ryan
insert into PADification.dbo.EvolutionTree(BaseMonsterID, NextMonsterID, EvoMaterialIDOne, EvoMaterialIDTwo, EvoMaterialIDThree, EvoMaterialIDFour, EvoMaterialIDFive, MinLevel, Devolveable, LevelReset) values
(140,141,175,160,160,151,151,50,0,1),		--Tsuku Yomi
(141,989,321,234,250,251,915,1,1,0),		--War Deity of the Night, Tsukuyomi
(141,990,151,321,175,250,251,1,1,0),		--Nocturne Chanter, Tsukuyomi
(141,2325,814,2129,1329,1329,1327,1,1,0),	--Awoken Tsukuyomi
(2325,3389,165,165,165,165,165,99,0,1),		--Reincarnated Tsukuyomi
(2944,2945,149,234,227,227,247,50,0,1),		--Steel Wand Mechdragon God, Balboa
(2945,3372,149,321,173,247,251,1,1,0),		--Radiant Staff Mechdragon God, Balboa
(2945,3373,149,321,1295,1295,1087,1,1,0);	--Steel Chronicle Mechdragon God, Balboa

--Zach
INSERT INTO PADification.dbo.EvolutionTree
(BaseMonsterID, NextMonsterID, EvoMaterialIDOne, EvoMaterialIDTwo, EvoMaterialIDThree, EvoMaterialIDFour, EvoMaterialIDFive, MinLevel, Devolveable, LevelReset)
VALUES
--Evolution Tree for Amon
(632,633,148,151,172,247,250,50,0,1), 
(633,1258,148,321,1176,247,247,1,1,0), 
(1258,2504,1324,148,916,1326,1328,1,1,0), 
(633,3532,2263,2639,1326,1326,1327,1,1,0), 
--Evolution Tree for Satsuki
(2149,2150,151,321,234,227,250,50,0,1), 
(2150,3580,151,321,916,916,916,1,1,0), 
(2150,3581,151,321,175,249,251,1,1,0);

--Elie
INSERT INTO PADification.dbo.EvolutionTree
(BaseMonsterID, NextMonsterID, EvoMaterialIDOne, EvoMaterialIDTwo, EvoMaterialIDThree, EvoMaterialIDFour, EvoMaterialIDFive, MinLevel, Devolveable, LevelReset)
VALUES
--Evolution Tree for Spinon
(17,18,152,NULL,NULL,NULL,NULL,5,0,1),
(18,19,153,159,NULL,NULL,NULL,15,0,1),
(19,20,154,153,152,159,151,35,0,1),
(20,484,251,234,321,321,227,1,1,0),
--Evolution Tree for Fallen Angel Lucifer
(638,639,151,151,175,250,250,50,0,1),
(639,1552,151,321,246,250,916,1,1,0),
(1552,1553,151,321,250,916,916,1,1,0),
(1552,2507,1646,917,1329,1329,1328,1,1,0);







