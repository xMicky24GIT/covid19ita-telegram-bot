create schema if not exists covid19 collate utf8mb4_0900_ai_ci;

create table if not exists admins
(
	user_id int not null
		primary key
);

create table if not exists users
(
	user_id int not null
		primary key,
	notifications tinyint(1) default 1 not null,
	status varchar(255) default '' null
);
