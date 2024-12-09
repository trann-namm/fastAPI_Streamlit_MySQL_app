# database/init.sql
DROP DATABASE IF EXISTS startup_db;
CREATE DATABASE startup_db;
USE startup_db;

CREATE TABLE startups (
    `index` INT,
    `Company` VARCHAR(255),
    `Valuation` VARCHAR(50),
    `Date_Joined` DATE,
    `Country` VARCHAR(100),
    `City` VARCHAR(100),
    `Industry` VARCHAR(255),
    `Selector_Investors` TEXT
);

INSERT INTO startups VALUES 
(0, 'ByteDance', "$225.0", '04/07/2017', 'China', 'Beijing', 'Media & Entertainment', 'Sequoia Capital China, SIG Asia Investments, Sina Weibo, SoftBank Group'),
(1, 'SpaceX', "$200.0", '01/12/2012', 'United States', 'Hawthorne', 'Industrials', 'Founders Fund, Draper Fisher Jurvetson, Rothenberg Ventures'),
(2, 'OpenAI', "$157.0", '22/07/2009', 'United States', 'San Francisco', 'Enterprise Tech', 'Khosla Ventures, Thrive Capital, Sequoia Capital'),
(3, 'SHEIN', "$66.0", '03/07/2018', 'Singapore', '', 'Consumer & Retail', 'Tiger Global Management, Sequoia Capital China, Shunwei Capital Partners'),
(4, 'Stripe', "$70.0", '23/01/2014', 'United States', 'San Francisco', 'Financial Services', 'Khosla Ventures, LowercaseCapital, capitalG');
