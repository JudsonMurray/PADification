--PADification Databse Creation script--
--REVISION HISTORY
--June 22, 2017 - Initial creation of this script (V.1.0)
--June 26, 2017 - Added table inserts for EvolutionTree & AwokenBadge (V.1.1)
--June 28, 2017 - Removed the execution of inserts for tags both team & monster (V.1.2)
--July 7, 2017 - Removed the functionality of delete PADification Database (V.1.3)

--if DB_ID('PADification') is not null
--	 Use Master
--	 drop database PADification;
--	 GO	 

USE MASTER

/****** Object:  Database [PADification]    Script Date: 2017-06-22 9:37:57 AM ******/
CREATE DATABASE [PADification]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'PADification', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL12.MSSQLSERVER\MSSQL\DATA\PADification.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'PADification_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL12.MSSQLSERVER\MSSQL\DATA\PADification_log.ldf' , SIZE = 2048KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [PADification] SET COMPATIBILITY_LEVEL = 120
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [PADification].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [PADification] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [PADification] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [PADification] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [PADification] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [PADification] SET ARITHABORT OFF 
GO
ALTER DATABASE [PADification] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [PADification] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [PADification] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [PADification] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [PADification] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [PADification] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [PADification] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [PADification] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [PADification] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [PADification] SET  DISABLE_BROKER 
GO
ALTER DATABASE [PADification] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [PADification] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [PADification] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [PADification] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [PADification] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [PADification] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [PADification] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [PADification] SET RECOVERY FULL 
GO
ALTER DATABASE [PADification] SET  MULTI_USER 
GO
ALTER DATABASE [PADification] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [PADification] SET DB_CHAINING OFF 
GO
ALTER DATABASE [PADification] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [PADification] SET TARGET_RECOVERY_TIME = 0 SECONDS 
GO
ALTER DATABASE [PADification] SET DELAYED_DURABILITY = DISABLED 
GO
EXEC sys.sp_db_vardecimal_storage_format N'PADification', N'ON'
GO
ALTER DATABASE [PADification] SET  READ_WRITE 
GO

--Execute table create
use PADification

:r .\Table-Create.sql
:r .\LatentSkill-Inserts.sql
:r .\AttributeAndType-Inserts.sql
:r .\ActiveSkill-Inserts.sql
:r .\LeaderSkill-Inserts.sql
:r .\AwokenSkill-Inserts.sql
--:r .\MonsterAndTeamTags-Inserts.sql
GO

:r .\AwokenSkillList-Inserts.sql
GO

:r .\MonsterClass-Inserts.sql
GO

:r .\EvolutionTree-Inserts.sql
:r .\AwokenBadges-Inserts.sql
GO

print 'complete'