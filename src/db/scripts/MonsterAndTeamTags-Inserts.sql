--Purpose:	Tags Insert sql query for MonsterTags & TeamTags
--Date:		June 27th 2017
--Author:	Elie Godbout
--Version:	1.0

USE PADification

insert into PADification.dbo.MonsterTags Values

('Leader'),
('Recovery'),
('Damage Dealer'),
('Bulky HP'),
('Defensive'),
('Resistance'),
('Jammer Remover'),
('Poison Remover'),
('Skill Bind Resist'),
('Blind Remover'),
('Fire Synergy'),
('Water Synergy'),
('Wood Synergy'),
('Light Synergy'),
('Dark Synergy'),
('Attacker Synergy'),
('Physical Synergy'),
('Healer Synergy'),
('Dragon Synergy'),
('God Synergy'),
('Machine Synergy'),
('Devil Synergy'),
('Balanced Synergy');

insert into PADification.dbo.TeamTags Values

('Fire'),
('Water'),
('Wood'),
('Light'),
('Dark'),
('Rainbow'),
('One Shot'),
('ATK Heavy'),
('HP Heavy'),
('RCV Heavy'),
('High Cost'),
('Low Cost'),
('Technical'),
('Ranking'),
('Muliplayer'),
('Defensive'),
('Resistance');