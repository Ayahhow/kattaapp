sqlite3 C:\Users\fukuaya\Desktop\katta\katta.db
create table users(
  userid integer primary key autoincrement,
  username string not null,
  nickname string not null,
  password string not null,
  maincomuid integer default 0
);
-- insert into users (username, nickname, password) values ('ayaka', 'ayahhow', 'aaaa');
-- insert into users (username, nickname, password) values ('kazuki', 'kazu', 'kkkk');
-- insert into users (username, nickname, password) values ('yuuto', 'yuu', 'yyyy');
-- insert into users (username, nickname, password) values ('syun', 'syun', 'ssss');
-- insert into users (username, nickname, password) values ('souma', 'souma', 'ssss');
-- insert into users (username, nickname, password) values ('souma', 'souma', 'ssss');
-- insert into users (username, nickname, password) values ('tokuko', 'ママ', 'tttt');
-- insert into users (username, nickname, password) values ('kenji', 'パパ', 'kkkk');
-- insert into users (username, nickname, password) values ('sumiko', 'ばあちゃん', 'ssss');
-- kaname kkkk
n:souma p:saitou
n:egu p:eguchi
n:hanae p:hanae
n:ume p:umehara
n:ayaka p:fukunaga
n:kazuki
n:yuuto
n:sumiko p:ihara
n:tokuko
n:kenji

create table comunity(
  comuid integer primary key autoincrement,
  comuname string not null,
  comupass string not null
);
-- insert into comunity (comuname, comupass) values ('fukunaga', 'jikka');
-- insert into comunity (comuname, comupass) values ('jeys', 'syun');
-- insert into comunity (comuname, comupass) values ('abs', 'bukatu');




create table belongs(
  entcomuid integer not null,
  entuserid integer not null
);
-- insert into belongs values(1,1);
-- insert into belongs values(2,1);
-- insert into belongs values(3,1);
-- insert into belongs values(1,2);
-- insert into belongs values(2,4);
-- insert into belongs values(1,3);
-- insert into belongs values(1,8);
-- insert into belongs values(1,9);
-- insert into belongs values(1,10);

create table comubuys(
  comubuysid integer primary key autoincrement,
  buycomuid integer not null,
  buyuserid integer not null,
  comubuy string not null,
  comubuytime default CURRENT_TIMESTAMP,
  comuetc text default "",
  comubflag integer default 0
);
-- insert into comubuys (buycomuid, buyuserid, comubuy, comuetc) values(1,1,"牛乳", "");
-- insert into comubuys (buycomuid, buyuserid, comubuy, comuetc) values(2,1,"卵", "すき焼き用");
-- insert into comubuys (buycomuid, buyuserid, comubuy, comuetc) values(3,1,"お菓子", "甘いものがいい");
-- insert into comubuys (buycomuid, buyuserid, comubuy, comuetc) values(2,4,"洗剤", "");
-- insert into comubuys (buycomuid, buyuserid, comubuy, comuetc) values(1,3,"化粧水", "ママの");


create table comubhist(
  comubhsid integer primary key autoincrement,
  comubuysid integer,
  buycomuid integer not null,
  buyuserid integer not null,
  boughtuserid integer not null,
  comubuy string not null,
  comubuytime default CURRENT_TIMESTAMP,
  kattatime default CURRENT_TIMESTAMP,
  comuetc text default ""
);



create table mybuys(
  mybuysid integer primary key autoincrement,
  buymyid integer not null,
  mybuy string not null,
  mybuytime default CURRENT_TIMESTAMP,
  myetc text default "",
  mybflag integer default 0
);
-- insert into mybuys (buymyid, mybuy, myetc) values(1, "冷蔵庫", "はやく");
-- insert into mybuys (buymyid, mybuy, myetc) values(1, "洗濯機", "買わねば");
-- insert into mybuys (buymyid, mybuy, myetc) values(1, "電子レンジ", "");



create table mybhist(
  mybhsid integer primary key autoincrement,
  mybuysid integer,
  buymyid integer not null,
  mybuy string not null,
  mybuytime default CURRENT_TIMESTAMP,
  kattatime default CURRENT_TIMESTAMP,
  myetc text default ""
);




create table pubcolumn(
  colid integer primary key autoincrement,
  pubmyid integer not null,
  pubcol string not null,
  monthlydline integer not null,
  reminddline integer not null
);



create table pub(
  myid integer not null,
  thispubmonth integer not null,
  pubcolsid integer not null,
  pubflag integer not null default 0
);
