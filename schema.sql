drop table if exists songs;
create table songs (
    id integer promary key autoincrement,
    title text not null,
    artist text not null,
    genre text not null
);
