--Awoken Badges

use PADification;

insert into PADification.dbo.AwokenBadge (AwokenBadgeName, AwokenBadgeDesc)
Values
('Team Cost +100', 'Increases Max Team Cost by 100'),
('Move Time +1 second', 'Extends Orb move time by 1 second'),
('Mass Attack', 'Attacks become Mass Attacks'),
('Team RCV +25%', 'Increases Team RCV by 25%'),
('Team HP +5%', 'Increases Team HP by 5%'),
('Team ATK +5%', 'Increases Team ATK by 5%'),
('Skillboost', 'Team�s skills charged by 1 turn'),
('Leaders Bind immune', 'Team Leaders become Bind immune'),
('Skill Bind resists +50%', 'Increases Skill Bind Resist by 50%'),
('Team HP +15% / Team Cost -300', 'Increases Team HP by 15%, but decreases Max Team Cost by 300'), 
('Move Time +2 seconds / Team Cost -400', 'Extends Orb move time by 2 seconds, but decreases Max Team Cost by 400'),
('Team RCV +35% / Team Cost -300', 'Increases Team RCV by 35%, but decreases Max Team Cost by 300'),
('No Skyfall Combos', 'When erasing Orbs, new ones won’t appear until the turn is over'),
('Team ATK +15% / Team Cost -300', 'Increases Team ATK by 15%, but decreases Max Team Cost by 300');