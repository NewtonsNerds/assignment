drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  user text, 
  start_time text,
  end_time text,
  log text
);