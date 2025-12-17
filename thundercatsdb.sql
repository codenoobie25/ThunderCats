-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 16, 2025 at 11:40 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `thundercatsdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `categoryID` int(11) NOT NULL,
  `categoryName` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`categoryID`, `categoryName`) VALUES
(101, 'GPU'),
(102, 'CPU'),
(103, 'Motherboard'),
(104, 'RAM'),
(105, 'Storage'),
(106, 'PSU'),
(107, 'Mouse'),
(108, 'Keyboard'),
(109, 'Accessory');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `employeeID` int(11) NOT NULL,
  `roleID` int(11) NOT NULL,
  `emp_first_name` varchar(32) NOT NULL,
  `emp_last_name` varchar(32) NOT NULL,
  `emp_phone` varchar(32) DEFAULT NULL,
  `emp_email` varchar(32) DEFAULT NULL,
  `date_hired` date NOT NULL,
  `status` varchar(32) NOT NULL,
  `street_address` varchar(40) NOT NULL,
  `city` varchar(24) NOT NULL,
  `province` varchar(24) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`employeeID`, `roleID`, `emp_first_name`, `emp_last_name`, `emp_phone`, `emp_email`, `date_hired`, `status`, `street_address`, `city`, `province`, `user_id`) VALUES
(1, 2, 'Jane', 'Doe', '09171230001', 'Jane.Doe@zzzcorp.com', '2024-01-12', 'Active', '101 Sixth Street', 'New Eridu', 'Central District', 143),
(2, 1, 'Nicole', 'Demara', '09171230002', 'nicole.demara@zzzcorp.com', '2024-02-03', 'Active', '202 Hollow Avenue', 'New Eridu', 'Central District', 123),
(3, 2, 'Billy', 'Kid', '09171230003', 'billy.kid@zzzcorp.com', '2024-03-18', 'Active', '303 Gear Road', 'New Eridu', 'Industrial Zone', 142);

-- --------------------------------------------------------

--
-- Table structure for table `employee_roles`
--

CREATE TABLE `employee_roles` (
  `roleID` int(11) NOT NULL,
  `role_name` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_roles`
--

INSERT INTO `employee_roles` (`roleID`, `role_name`) VALUES
(1, 'Admin'),
(2, 'Cashier'),
(3, 'Sale Staff');

-- --------------------------------------------------------

--
-- Table structure for table `generated_reports`
--

CREATE TABLE `generated_reports` (
  `report_id` int(11) NOT NULL,
  `report_name` varchar(255) NOT NULL,
  `file_path` varchar(500) NOT NULL,
  `report_type` varchar(50) NOT NULL,
  `date_created` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `generated_reports`
--

INSERT INTO `generated_reports` (`report_id`, `report_name`, `file_path`, `report_type`, `date_created`) VALUES
(1, 'ThunderCats 2025-12-16 Full Sales Report.pdf', 'C:\\Users\\Blyte\\PycharmProjects\\ThunderCats\\ThunderCats 2025-12-16 Full Sales Report.pdf', 'Sale', '2025-12-16 17:06:59'),
(2, 'ThunderCats 2025-12-16 Sales Report_17-07-43.pdf', 'C:\\Users\\Blyte\\PycharmProjects\\ThunderCats\\ThunderCats 2025-12-16 Sales Report_17-07-43.pdf', 'Sale', '2025-12-16 17:07:44'),
(3, 'ThunderCats_2025-12-16_FULL_Sale_Report.pdf', 'C:\\Users\\Blyte\\PycharmProjects\\ThunderCats\\ThunderCats_2025-12-16_FULL_Sale_Report.pdf', 'Sale', '2025-12-16 17:56:16'),
(4, 'ThunderCats_2025-12-16_Sale_Report.pdf', 'C:\\Users\\Blyte\\PycharmProjects\\ThunderCats\\ThunderCats_2025-12-16_Sale_Report.pdf', 'Sale', '2025-12-16 18:07:09'),
(5, 'ThunderCats_2025-12-16_Sale_18-28-59.pdf', 'C:\\Users\\Blyte\\PycharmProjects\\ThunderCats\\ThunderCats_2025-12-16_Sale_18-28-59.pdf', 'Sale', '2025-12-16 18:28:59'),
(6, 'ThunderCats_2025-12-16_Sale_18-30-46.pdf', 'C:\\Users\\Blyte\\PycharmProjects\\ThunderCats\\ThunderCats_2025-12-16_Sale_18-30-46.pdf', 'Sale', '2025-12-16 18:30:46'),
(7, 'ThunderCats_2025-12-16_Sale_18-31-34.pdf', 'C:\\Users\\Blyte\\PycharmProjects\\ThunderCats\\ThunderCats_2025-12-16_Sale_18-31-34.pdf', 'Sale', '2025-12-16 18:31:34'),
(8, 'ThunderCats_2025-12-16_FULL_Product_Report.pdf', 'C:\\Users\\Blyte\\PycharmProjects\\ThunderCats\\ThunderCats_2025-12-16_FULL_Product_Report.pdf', 'Product', '2025-12-16 18:31:57');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `Status` varchar(20) NOT NULL,
  `stock_quantity` int(100) DEFAULT NULL,
  `categoryID` int(11) NOT NULL,
  `warranty` varchar(10) NOT NULL,
  `Add_Date` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `sku`, `price`, `Status`, `stock_quantity`, `categoryID`, `warranty`, `Add_Date`) VALUES
(1, 'NVIDIA GeForce RTX 4060 Ti', 'SXU-98574', 23230.00, 'In Stock', 15, 101, '2 years', '2025-12-16'),
(2, 'AMD Ryzen 5 5600X', 'SXU-87452', 9800.00, 'Low Stock', 3, 102, '3 years', '2025-12-16'),
(3, 'Corsair Vengeance LPX 16GB (2x8GB)', 'SXU-58741', 3950.00, 'In Stock', 10, 104, 'Lifetime', '2025-12-16'),
(4, 'NVIDIA GeForce RTX 4090 Ti', 'SXU-91744', 23230.00, 'In Stock', 15, 101, '2 years', '2023-03-15'),
(100, 'Nvidia RTX 5090', 'SXU-89464', 35600.00, 'Low Stock', 5, 101, '1 year', '2025-12-16'),
(101, 'AMD Ryzen 7 5600X', 'SXU-74177', 9800.00, 'Low Stock', 3, 102, '3 years', '2023-05-22'),
(102, 'Corsair Vengeance LPX 32GB (2x16GB)', 'SXU-34342', 3950.00, 'Low Stock', 4, 104, 'Lifetime', '2023-08-11'),
(103, 'ASUS ROG Strix B550-F Gaming', 'SXU-61823', 12500.00, 'In Stock', 8, 103, '3 years', '2023-01-30'),
(104, 'Samsung 970 EVO Plus 1TB NVMe SSD', 'SXU-49281', 8500.00, 'In Stock', 12, 105, '5 years', '2023-07-18'),
(105, 'Corsair RM750x 80 Plus Gold', 'SXU-77534', 9200.00, 'Low Stock', 5, 106, '10 years', '2023-09-05'),
(106, 'Logitech G Pro X Superlight', 'SXU-20391', 6500.00, 'In Stock', 25, 107, '2 years', '2023-04-12'),
(107, 'Keychron K8 Pro Mechanical Keyboard', 'SXU-88912', 7200.00, 'In Stock', 18, 108, '1 year', '2023-11-28'),
(108, 'Antec Cable Extensions Kit', 'SXU-45673', 1800.00, 'In Stock', 42, 109, '1 year', '2023-02-14'),
(109, 'Intel Core i7-13700K', 'SXU-33467', 31500.00, 'In Stock', 7, 102, '3 years', '2023-06-09'),
(110, 'Gigabyte GeForce RTX 4070 Windforce', 'SXU-91245', 38500.00, 'Low Stock', 2, 101, '3 years', '2023-10-25'),
(111, 'MSI MPG Z790 Edge WiFi', 'SXU-67238', 24500.00, 'In Stock', 6, 103, '3 years', '2024-01-15'),
(112, 'G.Skill Trident Z5 RGB 32GB DDR5', 'SXU-78129', 11200.00, 'In Stock', 14, 104, 'Lifetime', '2024-03-08'),
(113, 'WD Black SN850X 2TB SSD', 'SXU-54326', 16500.00, 'In Stock', 9, 105, '5 years', '2024-05-20'),
(114, 'Seasonic Focus GX-850', 'SXU-39874', 10500.00, 'In Stock', 11, 106, '12 years', '2024-07-03'),
(115, 'Razer DeathAdder V3 Pro', 'SXU-62983', 7800.00, 'Low Stock', 4, 107, '2 years', '2024-02-28'),
(116, 'Ducky One 3 Mechanical Keyboard', 'SXU-11234', 8900.00, 'In Stock', 16, 108, '2 years', '2024-09-14'),
(117, 'Deepcool AK620 CPU Cooler', 'SXU-76543', 4200.00, 'In Stock', 22, 109, '5 years', '2024-04-30'),
(118, 'AMD Ryzen 9 7900X', 'SXU-98712', 42800.00, 'Low Stock', 3, 102, '3 years', '2024-08-22'),
(119, 'ASUS TUF Gaming RTX 3080', 'SXU-43189', 52000.00, 'Out of Stock', 0, 101, '3 years', '2024-12-05'),
(120, 'ASRock B650M Pro RS', 'SXU-87654', 13500.00, 'In Stock', 10, 103, '3 years', '2024-06-17'),
(121, 'Kingston Fury Beast 64GB DDR4', 'SXU-21987', 15800.00, 'In Stock', 8, 104, 'Lifetime', '2024-10-11'),
(122, 'Crucial P5 Plus 1TB PCIe 4.0', 'SXU-65432', 7200.00, 'In Stock', 20, 105, '5 years', '2024-01-25'),
(123, 'EVGA SuperNOVA 1000 G6', 'SXU-34567', 18500.00, 'Low Stock', 3, 106, '10 years', '2024-11-08'),
(124, 'SteelSeries Aerox 5 Wireless', 'SXU-78901', 9200.00, 'In Stock', 13, 107, '2 years', '2024-03-19'),
(125, 'HyperX Alloy Origins 65', 'SXU-43210', 6800.00, 'In Stock', 19, 108, '2 years', '2025-01-12'),
(126, 'NZXT H7 Flow Mid-Tower Case', 'SXU-56789', 12500.00, 'In Stock', 15, 109, '2 years', '2025-05-24'),
(127, 'Intel Core i5-13600KF', 'SXU-87612', 24500.00, 'In Stock', 11, 102, '3 years', '2025-07-30'),
(128, 'Sapphire Pulse RX 7800 XT', 'SXU-34128', 42500.00, 'Low Stock', 4, 101, '3 years', '2025-09-16'),
(129, 'Gigabyte B760 Gaming X AX', 'SXU-98231', 16500.00, 'In Stock', 9, 103, '3 years', '2025-02-08'),
(130, 'TeamGroup T-Force Delta RGB 16GB', 'SXU-56712', 4800.00, 'In Stock', 27, 104, 'Lifetime', '2025-11-21'),
(131, 'Seagate FireCuda 530 2TB', 'SXU-78123', 19500.00, 'Low Stock', 5, 105, '5 years', '2025-04-03'),
(132, 'Cooler Master V850 Gold', 'SXU-45678', 12500.00, 'In Stock', 12, 106, '10 years', '2025-08-14'),
(133, 'Glorious Model D Wireless', 'SXU-89123', 5600.00, 'In Stock', 24, 107, '2 years', '2023-12-09'),
(134, 'Logitech G915 TKL Wireless', 'SXU-23456', 16800.00, 'Low Stock', 6, 108, '2 years', '2023-10-31'),
(135, 'Arctic Liquid Freezer II 360', 'SXU-78945', 8500.00, 'In Stock', 18, 109, '6 years', '2023-02-25'),
(136, 'AMD Ryzen 7 5800X3D', 'SXU-65478', 28500.00, 'In Stock', 8, 102, '3 years', '2023-07-04'),
(137, 'ZOTAC Gaming RTX 4060 Twin Edge', 'SXU-32145', 26500.00, 'In Stock', 14, 101, '3 years', '2023-11-15'),
(138, 'ASUS Prime Z790-P WiFi', 'SXU-98765', 19500.00, 'Low Stock', 5, 103, '3 years', '2024-02-20'),
(139, 'Patriot Viper Steel 32GB DDR4', 'SXU-54321', 6200.00, 'In Stock', 21, 104, 'Lifetime', '2024-06-28'),
(140, 'Kingston A2000 1TB NVMe SSD', 'SXU-67890', 5200.00, 'In Stock', 33, 105, '5 years', '2024-09-07'),
(141, 'Thermaltake Toughpower GF3 1000W', 'SXU-13579', 21500.00, 'In Stock', 7, 106, '12 years', '2024-12-18'),
(142, 'Razer Viper Ultimate', 'SXU-24680', 11200.00, 'Low Stock', 3, 107, '2 years', '2024-04-22'),
(143, 'Corsair K70 RGB TKL', 'SXU-86420', 13800.00, 'In Stock', 11, 108, '2 years', '2025-03-05'),
(144, 'Lian Li Uni Fan SL-INF 120', 'SXU-97531', 3200.00, 'In Stock', 45, 109, '2 years', '2025-06-19'),
(145, 'Intel Core i9-14900K', 'SXU-75319', 58500.00, 'Low Stock', 2, 102, '3 years', '2025-10-01'),
(146, 'MSI GeForce RTX 4090 Suprim X', 'SXU-15926', 168000.00, 'Out of Stock', 0, 101, '3 years', '2023-08-29'),
(147, 'ASUS ROG Crosshair X670E Hero', 'SXU-35791', 42500.00, 'Low Stock', 1, 103, '3 years', '2023-04-17'),
(148, 'Corsair Dominator Platinum RGB 64GB', 'SXU-68234', 24500.00, 'In Stock', 6, 104, 'Lifetime', '2023-09-24'),
(149, 'Sabrent Rocket 4 Plus 2TB', 'SXU-42857', 18500.00, 'In Stock', 10, 105, '5 years', '2023-12-30'),
(150, 'be quiet! Dark Power 13 850W', 'SXU-91735', 19800.00, 'In Stock', 8, 106, '10 years', '2024-05-09'),
(151, 'Logitech G502 X Plus', 'SXU-64281', 10500.00, 'In Stock', 17, 107, '2 years', '2024-07-26'),
(152, 'SteelSeries Apex Pro TKL', 'SXU-31975', 15800.00, 'Low Stock', 4, 108, '2 years', '2024-10-04'),
(153, 'Noctua NH-D15 Chromax Black', 'SXU-57413', 9200.00, 'In Stock', 14, 109, '6 years', '2024-01-31'),
(154, 'AMD Ryzen 5 7600X', 'SXU-82649', 21500.00, 'In Stock', 12, 102, '3 years', '2025-08-23'),
(155, 'Gigabyte AORUS RTX 4070 Ti Master', 'SXU-19375', 62500.00, 'Low Stock', 3, 101, '3 years', '2025-11-14'),
(156, 'MSI MAG B650 Tomahawk WiFi', 'SXU-46821', 18500.00, 'In Stock', 9, 103, '3 years', '2025-02-27'),
(157, 'ADATA XPG Lancer RGB 32GB DDR5', 'SXU-72954', 12800.00, 'In Stock', 15, 104, 'Lifetime', '2025-04-08'),
(158, 'Samsung 980 Pro 2TB with Heatsink', 'SXU-38516', 19500.00, 'In Stock', 11, 105, '5 years', '2025-12-15'),
(159, 'Corsair HX1000i Platinum', 'SXU-64293', 22500.00, 'Low Stock', 4, 106, '12 years', '2025-07-01'),
(160, 'Razer Basilisk V3 Pro', 'SXU-15782', 12500.00, 'In Stock', 13, 107, '2 years', '2023-05-14'),
(161, 'Keychron Q3 Custom Mechanical', 'SXU-89461', 14500.00, 'In Stock', 8, 108, '1 year', '2023-08-08'),
(162, 'Fractal Design Torrent Case', 'SXU-32678', 18500.00, 'Low Stock', 5, 109, '2 years', '2023-10-20'),
(163, 'Intel Core i3-14100', 'SXU-75324', 13500.00, 'In Stock', 25, 102, '3 years', '2024-03-01'),
(164, 'ASUS Dual RX 7600 OC Edition', 'SXU-48629', 28500.00, 'In Stock', 16, 101, '3 years', '2024-06-12'),
(165, 'ASRock H770 Steel Legend', 'SXU-61943', 14500.00, 'In Stock', 14, 103, '3 years', '2024-09-25'),
(166, 'Crucial Ballistix 16GB DDR4 3600MHz', 'SXU-28751', 4200.00, 'In Stock', 38, 104, 'Lifetime', '2024-12-08'),
(167, 'WD Blue SN580 1TB NVMe SSD', 'SXU-93462', 4800.00, 'In Stock', 29, 105, '5 years', '2025-01-17'),
(168, 'EVGA 850 BQ 80 Plus Bronze', 'SXU-56189', 7800.00, 'In Stock', 21, 106, '5 years', '2025-05-29'),
(169, 'SteelSeries Rival 650 Wireless', 'SXU-41872', 8500.00, 'Low Stock', 7, 107, '2 years', '2025-09-11'),
(170, 'Akko 3068B Plus Wireless Keyboard', 'SXU-73951', 6200.00, 'In Stock', 23, 108, '1 year', '2023-01-08'),
(171, 'Thermalright Peerless Assassin 120', 'SXU-82547', 3800.00, 'In Stock', 32, 109, '5 years', '2023-03-21'),
(172, 'AMD Ryzen 3 5300G', 'SXU-19463', 9800.00, 'In Stock', 18, 102, '3 years', '2023-06-04'),
(173, 'PNY XLR8 RTX 3060 12GB', 'SXU-57284', 23500.00, 'Low Stock', 6, 101, '3 years', '2023-09-27'),
(174, 'Gigabyte A520M DS3H', 'SXU-68195', 6500.00, 'In Stock', 27, 103, '3 years', '2024-04-14'),
(175, 'OLOy Blade RGB 32GB DDR4 3200MHz', 'SXU-42971', 5200.00, 'In Stock', 31, 104, 'Lifetime', '2024-08-01'),
(176, 'Intel 670p 2TB QLC NVMe SSD', 'SXU-83642', 6800.00, 'In Stock', 24, 105, '5 years', '2024-11-23'),
(177, 'Cooler Master MWE Gold 750 V2', 'SXU-71539', 9200.00, 'In Stock', 19, 106, '5 years', '2025-03-16'),
(178, 'Corsair M65 RGB Ultra Wireless', 'SXU-29468', 7800.00, 'In Stock', 15, 107, '2 years', '2025-06-28'),
(179, 'Royal Kludge RK84 Wireless', 'SXU-56317', 5200.00, 'In Stock', 35, 108, '1 year', '2025-10-10'),
(180, 'Phanteks T30-120 Premium Fan', 'SXU-87245', 2800.00, 'In Stock', 48, 109, '2 years', '2023-12-22'),
(181, 'Intel Xeon W5-3435X', 'SXU-31946', 125000.00, 'Low Stock', 1, 102, '3 years', '2024-02-05'),
(182, 'NVIDIA RTX A4000 16GB', 'SXU-75823', 95000.00, 'Out of Stock', 0, 101, '3 years', '2024-07-19'),
(183, 'Supermicro X13SAE-F Motherboard', 'SXU-64219', 28500.00, 'Low Stock', 2, 103, '3 years', '2024-10-29'),
(184, 'Samsung 64GB DDR5 ECC Registered', 'SXU-91573', 38500.00, 'In Stock', 5, 104, 'Lifetime', '2025-01-05'),
(185, 'Seagate Exos X20 20TB HDD', 'SXU-28461', 42500.00, 'In Stock', 8, 105, '5 years', '2025-08-18'),
(186, 'SilverStone ST1000-PTS 1000W', 'SXU-73952', 15500.00, 'In Stock', 13, 106, '7 years', '2025-11-30'),
(187, 'Microsoft Pro IntelliMouse', 'SXU-46185', 6500.00, 'In Stock', 28, 107, '1 year', '2023-04-26'),
(188, 'Logitech MX Keys S Wireless', 'SXU-82574', 10500.00, 'In Stock', 22, 108, '2 years', '2023-07-10'),
(189, 'CableMod Custom Cable Kit', 'SXU-39267', 4800.00, 'In Stock', 39, 109, '1 year', '2023-11-02'),
(190, 'AMD Threadripper PRO 5995WX', 'SXU-63914', 485000.00, 'Low Stock', 1, 102, '3 years', '2024-05-13'),
(191, 'PowerColor Red Devil RX 7900 XTX', 'SXU-85729', 84500.00, 'In Stock', 3, 101, '3 years', '2024-09-02'),
(192, 'Gigabyte X670E AORUS Master', 'SXU-39146', 38500.00, 'Low Stock', 4, 103, '3 years', '2024-12-24'),
(193, 'Corsair Vengeance RGB 128GB DDR5', 'SXU-26847', 58500.00, 'In Stock', 2, 104, 'Lifetime', '2025-02-14'),
(194, 'SK Hynix Platinum P41 4TB SSD', 'SXU-71632', 42500.00, 'In Stock', 6, 105, '5 years', '2025-09-27'),
(195, 'ASUS ROG Thor 1200P2 Platinum', 'SXU-54981', 32500.00, 'Low Stock', 3, 106, '10 years', '2025-12-03'),
(196, 'Finalmouse Starlight-12 Pro', 'SXU-82375', 18500.00, 'Out of Stock', 0, 107, '2 years', '2023-08-15'),
(197, 'Wooting 60HE Analog Keyboard', 'SXU-91462', 16500.00, 'In Stock', 9, 108, '1 year', '2023-10-07'),
(198, 'EKWB Quantum Velocity² CPU Block', 'SXU-73529', 8500.00, 'In Stock', 14, 109, '2 years', '2024-03-25'),
(199, 'AMD EPYC 9654 96-Core Processor', 'SXU-18245', 625000.00, 'Low Stock', 1, 102, '3 years', '2024-11-17');

-- --------------------------------------------------------

--
-- Table structure for table `return_requests`
--

CREATE TABLE `return_requests` (
  `return_id` int(11) NOT NULL,
  `sale_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `staff_id` int(11) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `request_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `sale_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `sale_date` datetime DEFAULT current_timestamp(),
  `total_amount` decimal(10,2) DEFAULT NULL,
  `payment_method` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`sale_id`, `user_id`, `sale_date`, `total_amount`, `payment_method`) VALUES
(1, 142, '2024-01-05 00:00:00', 12450.00, 'GCash'),
(2, 143, '2024-01-12 00:00:00', 38500.00, 'Credit'),
(3, 142, '2024-01-18 00:00:00', 7800.00, 'Cash'),
(4, 143, '2024-01-22 00:00:00', 26500.00, 'GCash'),
(5, 142, '2024-01-30 00:00:00', 9200.00, 'GCash'),
(6, 143, '2024-02-03 00:00:00', 15800.00, 'Credit'),
(7, 142, '2024-02-10 00:00:00', 4250.00, 'Cash'),
(8, 143, '2024-02-15 00:00:00', 62500.00, 'Credit'),
(9, 142, '2024-02-21 00:00:00', 11200.00, 'GCash'),
(10, 143, '2024-02-28 00:00:00', 32500.00, 'Credit'),
(11, 142, '2024-03-05 00:00:00', 6800.00, 'Cash'),
(12, 143, '2024-03-11 00:00:00', 48500.00, 'Credit'),
(13, 142, '2024-03-17 00:00:00', 14500.00, 'GCash'),
(14, 143, '2024-03-24 00:00:00', 19500.00, 'Credit'),
(15, 142, '2024-03-31 00:00:00', 5600.00, 'Cash'),
(16, 143, '2024-04-07 00:00:00', 38500.00, 'Credit'),
(17, 142, '2024-04-13 00:00:00', 8500.00, 'GCash'),
(18, 143, '2024-04-19 00:00:00', 24500.00, 'GCash'),
(19, 142, '2024-04-25 00:00:00', 12500.00, 'Cash'),
(20, 143, '2024-04-30 00:00:00', 58500.00, 'Credit'),
(21, 142, '2024-05-08 00:00:00', 3200.00, 'GCash'),
(22, 143, '2024-05-14 00:00:00', 42500.00, 'Credit'),
(23, 142, '2024-05-20 00:00:00', 9800.00, 'Cash'),
(24, 143, '2024-05-26 00:00:00', 168000.00, 'Credit'),
(25, 142, '2024-06-02 00:00:00', 7200.00, 'GCash'),
(26, 143, '2024-06-09 00:00:00', 28500.00, 'Credit'),
(27, 142, '2024-06-15 00:00:00', 18500.00, 'Cash'),
(28, 143, '2024-06-22 00:00:00', 95000.00, 'Credit'),
(29, 142, '2024-06-28 00:00:00', 4200.00, 'GCash'),
(30, 143, '2024-07-04 00:00:00', 32500.00, 'Credit'),
(31, 142, '2024-07-11 00:00:00', 12500.00, 'Cash'),
(32, 143, '2024-07-18 00:00:00', 62500.00, 'Credit'),
(33, 142, '2024-07-24 00:00:00', 7800.00, 'GCash'),
(34, 143, '2024-07-30 00:00:00', 42500.00, 'Credit'),
(35, 142, '2024-08-06 00:00:00', 16500.00, 'Cash'),
(36, 143, '2024-08-12 00:00:00', 24500.00, 'GCash'),
(37, 142, '2024-08-19 00:00:00', 5200.00, 'GCash'),
(38, 143, '2024-08-25 00:00:00', 38500.00, 'Credit'),
(39, 142, '2024-08-31 00:00:00', 10500.00, 'Cash'),
(40, 143, '2024-09-07 00:00:00', 58500.00, 'Credit'),
(41, 142, '2024-09-14 00:00:00', 8500.00, 'GCash'),
(42, 143, '2024-09-21 00:00:00', 168000.00, 'Credit'),
(43, 142, '2024-09-28 00:00:00', 6200.00, 'Cash'),
(44, 143, '2024-10-05 00:00:00', 32500.00, 'Credit'),
(45, 142, '2024-10-12 00:00:00', 13500.00, 'GCash'),
(46, 143, '2024-10-19 00:00:00', 42500.00, 'Credit'),
(47, 142, '2024-10-26 00:00:00', 4800.00, 'Cash'),
(48, 143, '2024-11-02 00:00:00', 625000.00, 'Credit'),
(49, 142, '2024-11-09 00:00:00', 9200.00, 'GCash'),
(50, 143, '2024-11-16 00:00:00', 28500.00, 'Credit'),
(51, 142, '2024-11-23 00:00:00', 15800.00, 'Cash'),
(52, 143, '2024-11-30 00:00:00', 485000.00, 'Credit'),
(53, 142, '2024-12-07 00:00:00', 6500.00, 'GCash'),
(54, 143, '2024-12-14 00:00:00', 38500.00, 'Credit'),
(55, 142, '2024-12-21 00:00:00', 12500.00, 'Cash'),
(56, 143, '2024-12-28 00:00:00', 24500.00, 'Credit'),
(57, 142, '2025-01-04 00:00:00', 7800.00, 'GCash'),
(58, 143, '2025-01-11 00:00:00', 62500.00, 'Credit'),
(59, 142, '2025-01-18 00:00:00', 14500.00, 'Cash'),
(60, 143, '2025-01-25 00:00:00', 38500.00, 'Credit'),
(61, 142, '2025-02-01 00:00:00', 4200.00, 'GCash'),
(62, 143, '2025-02-08 00:00:00', 84500.00, 'Credit'),
(63, 142, '2025-02-15 00:00:00', 11200.00, 'Cash'),
(64, 143, '2025-02-22 00:00:00', 32500.00, 'Credit'),
(65, 142, '2025-03-01 00:00:00', 9800.00, 'GCash'),
(66, 143, '2025-03-08 00:00:00', 42500.00, 'Credit'),
(67, 142, '2025-03-15 00:00:00', 18500.00, 'Cash'),
(68, 143, '2025-03-22 00:00:00', 58500.00, 'Credit'),
(69, 142, '2025-03-29 00:00:00', 6800.00, 'GCash'),
(70, 143, '2025-04-05 00:00:00', 38500.00, 'Credit'),
(71, 142, '2025-04-12 00:00:00', 12500.00, 'Cash'),
(72, 143, '2025-04-19 00:00:00', 24500.00, 'Credit'),
(73, 142, '2025-04-26 00:00:00', 5600.00, 'GCash'),
(74, 143, '2025-05-03 00:00:00', 62500.00, 'Credit'),
(75, 142, '2025-05-10 00:00:00', 16500.00, 'Cash'),
(76, 143, '2025-05-17 00:00:00', 42500.00, 'Credit'),
(77, 142, '2025-05-24 00:00:00', 7800.00, 'GCash'),
(78, 143, '2025-05-31 00:00:00', 168000.00, 'Credit'),
(79, 142, '2025-06-07 00:00:00', 9200.00, 'Cash'),
(80, 143, '2025-06-14 00:00:00', 28500.00, 'Credit'),
(81, 142, '2025-06-21 00:00:00', 14500.00, 'GCash'),
(82, 143, '2025-06-28 00:00:00', 38500.00, 'Credit'),
(83, 142, '2025-07-05 00:00:00', 5200.00, 'Cash'),
(84, 143, '2025-07-12 00:00:00', 625000.00, 'Credit'),
(85, 142, '2025-07-19 00:00:00', 10500.00, 'GCash'),
(86, 143, '2025-07-26 00:00:00', 32500.00, 'Credit'),
(87, 142, '2025-08-02 00:00:00', 8500.00, 'Cash'),
(88, 143, '2025-08-09 00:00:00', 42500.00, 'Credit'),
(89, 142, '2025-08-16 00:00:00', 12500.00, 'GCash'),
(90, 143, '2025-08-23 00:00:00', 485000.00, 'Credit'),
(91, 142, '2025-08-30 00:00:00', 6800.00, 'Cash'),
(92, 143, '2025-09-06 00:00:00', 24500.00, 'Credit'),
(93, 142, '2025-09-13 00:00:00', 18500.00, 'GCash'),
(94, 143, '2025-09-20 00:00:00', 38500.00, 'Credit'),
(95, 142, '2025-09-27 00:00:00', 4800.00, 'Cash'),
(96, 143, '2025-10-04 00:00:00', 62500.00, 'Credit'),
(97, 142, '2025-10-11 00:00:00', 14500.00, 'GCash'),
(98, 143, '2025-10-18 00:00:00', 42500.00, 'Credit'),
(99, 142, '2025-10-25 00:00:00', 9200.00, 'Cash'),
(100, 143, '2025-11-01 00:00:00', 58500.00, 'Credit');

-- --------------------------------------------------------

--
-- Table structure for table `sale_details`
--

CREATE TABLE `sale_details` (
  `transactionID` int(11) NOT NULL,
  `sale_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `unit_price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sale_details`
--

INSERT INTO `sale_details` (`transactionID`, `sale_id`, `product_id`, `quantity`, `subtotal`, `unit_price`) VALUES
(1, 1, 103, 1, 12500.00, 12500.00),
(2, 1, 106, 1, 6500.00, 6500.00),
(3, 2, 110, 1, 38500.00, 38500.00),
(4, 3, 136, 1, 28500.00, 28500.00),
(5, 4, 137, 1, 26500.00, 26500.00),
(6, 5, 105, 1, 9200.00, 9200.00),
(7, 6, 148, 1, 24500.00, 24500.00),
(8, 7, 171, 1, 3800.00, 3800.00),
(9, 8, 155, 1, 62500.00, 62500.00),
(10, 9, 112, 1, 11200.00, 11200.00),
(11, 10, 114, 2, 21000.00, 10500.00),
(12, 11, 108, 2, 3600.00, 1800.00),
(13, 12, 118, 1, 42800.00, 42800.00),
(14, 13, 129, 1, 16500.00, 16500.00),
(15, 14, 149, 1, 18500.00, 18500.00),
(16, 15, 133, 1, 5600.00, 5600.00),
(17, 16, 113, 2, 33000.00, 16500.00),
(18, 17, 104, 1, 8500.00, 8500.00),
(19, 18, 111, 1, 24500.00, 24500.00),
(20, 19, 126, 1, 12500.00, 12500.00),
(21, 20, 145, 1, 58500.00, 58500.00),
(22, 21, 144, 3, 9600.00, 3200.00),
(23, 22, 119, 1, 52000.00, 52000.00),
(24, 23, 109, 1, 31500.00, 31500.00),
(25, 24, 146, 1, 168000.00, 168000.00),
(26, 25, 107, 1, 7200.00, 7200.00),
(27, 26, 120, 1, 13500.00, 13500.00),
(28, 27, 150, 1, 19800.00, 19800.00),
(29, 28, 182, 1, 95000.00, 95000.00),
(30, 29, 117, 1, 4200.00, 4200.00),
(31, 30, 114, 2, 21000.00, 10500.00),
(32, 31, 126, 1, 12500.00, 12500.00),
(33, 32, 155, 1, 62500.00, 62500.00),
(34, 33, 101, 1, 9800.00, 9800.00),
(35, 34, 119, 1, 52000.00, 52000.00),
(36, 35, 129, 1, 16500.00, 16500.00),
(37, 36, 148, 1, 24500.00, 24500.00),
(38, 37, 140, 2, 10400.00, 5200.00),
(39, 38, 113, 2, 33000.00, 16500.00),
(40, 39, 105, 1, 9200.00, 9200.00),
(41, 40, 145, 1, 58500.00, 58500.00),
(42, 41, 104, 1, 8500.00, 8500.00),
(43, 42, 146, 1, 168000.00, 168000.00),
(44, 43, 139, 1, 6200.00, 6200.00),
(45, 44, 114, 3, 31500.00, 10500.00),
(46, 45, 127, 1, 24500.00, 24500.00),
(47, 46, 119, 1, 52000.00, 52000.00),
(48, 47, 130, 2, 9600.00, 4800.00),
(49, 48, 181, 1, 125000.00, 125000.00),
(50, 49, 105, 1, 9200.00, 9200.00),
(51, 50, 120, 2, 27000.00, 13500.00),
(52, 51, 116, 1, 8900.00, 8900.00),
(53, 52, 199, 1, 625000.00, 625000.00),
(54, 53, 106, 1, 6500.00, 6500.00),
(55, 54, 113, 2, 33000.00, 16500.00),
(56, 55, 126, 1, 12500.00, 12500.00),
(57, 56, 111, 1, 24500.00, 24500.00),
(58, 57, 101, 1, 9800.00, 9800.00),
(59, 58, 155, 1, 62500.00, 62500.00),
(60, 59, 129, 1, 16500.00, 16500.00),
(61, 60, 113, 2, 33000.00, 16500.00),
(62, 61, 117, 1, 4200.00, 4200.00),
(63, 62, 191, 1, 84500.00, 84500.00),
(64, 63, 112, 1, 11200.00, 11200.00),
(65, 64, 114, 3, 31500.00, 10500.00),
(66, 65, 172, 1, 9800.00, 9800.00),
(67, 66, 119, 1, 52000.00, 52000.00),
(68, 67, 150, 1, 19800.00, 19800.00),
(69, 68, 145, 1, 58500.00, 58500.00),
(70, 69, 108, 2, 3600.00, 1800.00),
(71, 70, 113, 2, 33000.00, 16500.00),
(72, 71, 126, 1, 12500.00, 12500.00),
(73, 72, 111, 1, 24500.00, 24500.00),
(74, 73, 133, 1, 5600.00, 5600.00),
(75, 74, 155, 1, 62500.00, 62500.00),
(76, 75, 129, 1, 16500.00, 16500.00),
(77, 76, 119, 1, 52000.00, 52000.00),
(78, 77, 101, 1, 9800.00, 9800.00),
(79, 78, 146, 1, 168000.00, 168000.00),
(80, 79, 105, 1, 9200.00, 9200.00),
(81, 80, 120, 2, 27000.00, 13500.00),
(82, 81, 129, 1, 16500.00, 16500.00),
(83, 82, 113, 2, 33000.00, 16500.00),
(84, 83, 140, 1, 5200.00, 5200.00),
(85, 84, 199, 1, 625000.00, 625000.00),
(86, 85, 105, 1, 9200.00, 9200.00),
(87, 86, 114, 3, 31500.00, 10500.00),
(88, 87, 104, 1, 8500.00, 8500.00),
(89, 88, 119, 1, 52000.00, 52000.00),
(90, 89, 126, 1, 12500.00, 12500.00),
(91, 90, 190, 1, 485000.00, 485000.00),
(92, 91, 108, 2, 3600.00, 1800.00),
(93, 92, 111, 1, 24500.00, 24500.00),
(94, 93, 150, 1, 19800.00, 19800.00),
(95, 94, 113, 2, 33000.00, 16500.00),
(96, 95, 130, 1, 4800.00, 4800.00),
(97, 96, 155, 1, 62500.00, 62500.00),
(98, 97, 129, 1, 16500.00, 16500.00),
(99, 98, 119, 1, 52000.00, 52000.00),
(100, 99, 105, 1, 9200.00, 9200.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userID` int(6) NOT NULL,
  `Username` varchar(20) NOT NULL,
  `Passwords` varchar(12) NOT NULL,
  `Role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `Username`, `Passwords`, `Role`) VALUES
(123, 'admin.123', '123', 'Admin'),
(142, 'cashier144', '144', 'Cashier'),
(143, 'cashier143', '143', 'Cashier');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`categoryID`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`employeeID`),
  ADD KEY `user_id` (`user_id`) USING BTREE,
  ADD KEY `fk_role` (`roleID`);

--
-- Indexes for table `employee_roles`
--
ALTER TABLE `employee_roles`
  ADD PRIMARY KEY (`roleID`);

--
-- Indexes for table `generated_reports`
--
ALTER TABLE `generated_reports`
  ADD PRIMARY KEY (`report_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD UNIQUE KEY `sku` (`sku`) USING BTREE,
  ADD KEY `FK_category` (`categoryID`);

--
-- Indexes for table `return_requests`
--
ALTER TABLE `return_requests`
  ADD PRIMARY KEY (`return_id`),
  ADD KEY `sale_id` (`sale_id`),
  ADD KEY `staff_id` (`staff_id`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`sale_id`),
  ADD KEY `FK_User` (`user_id`);

--
-- Indexes for table `sale_details`
--
ALTER TABLE `sale_details`
  ADD PRIMARY KEY (`transactionID`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `FK_Sale` (`sale_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `generated_reports`
--
ALTER TABLE `generated_reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=200;

--
-- AUTO_INCREMENT for table `return_requests`
--
ALTER TABLE `return_requests`
  MODIFY `return_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sales`
--
ALTER TABLE `sales`
  MODIFY `sale_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `sale_details`
--
ALTER TABLE `sale_details`
  MODIFY `transactionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1051;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`userID`),
  ADD CONSTRAINT `fk_role` FOREIGN KEY (`roleID`) REFERENCES `employee_roles` (`roleID`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `FK_category` FOREIGN KEY (`categoryID`) REFERENCES `category` (`categoryID`);

--
-- Constraints for table `return_requests`
--
ALTER TABLE `return_requests`
  ADD CONSTRAINT `return_requests_ibfk_1` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`sale_id`),
  ADD CONSTRAINT `return_requests_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `employee` (`employeeID`);

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `FK_User` FOREIGN KEY (`user_id`) REFERENCES `users` (`userID`),
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`userID`);

--
-- Constraints for table `sale_details`
--
ALTER TABLE `sale_details`
  ADD CONSTRAINT `FK_Sale` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`sale_id`),
  ADD CONSTRAINT `sale_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
