drop table if exists songs;
create table songs (
    id integer primary key autoincrement,
    title text not null,
    artist text not null,
    genre text not null
);
