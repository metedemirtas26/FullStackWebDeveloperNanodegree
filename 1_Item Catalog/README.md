#Udaciy Full Stack Web Development Item Catalog Project

-------------

- Download the project

- Go vagrant Path : ...\Item Catalog\vagrant>

- run to <abbr title="Hyper Text Markup Language">vagrant up</abbr> command and after run  <abbr title="Hyper Text Markup Language">vagrant ssh</abbr> command

  If you didn't install Vagrant, you can install this adress :  
  `<link>` : <https://www.vagrantup.com/downloads.html> 

  If you didn't install VirtualBox, you can install this adress :  
  `<link>` : <https://www.virtualbox.org/wiki/Downloads>  

- Then go in machine 'vagrant' path : Command => 

   `cd /vagrant`

- If you want to go sql command line, run "psql forum" command 
    ( psql command can run sql database and we can write sql query, forum is database name )

    `psql forum`

- After then you can write your sql query. (For exp : "select 2+2;")

In Db

    You can these :

    Some other things you can do:

    \dt — list all the tables in the database.

    \dt+ — list tables plus additional information (notably, how big each table is on disk).

    \H — switch between printing tables in plain text vs. HTML.

    <=

    If you exit to command line, write this command : "\q" after click Enter

- You have to add tables to this commands :

```
    CREATE TABLE users
            (id INTEGER primary key,name varchar(150),email varchar(150),password varchar(150));

	CREATE TABLE category
            (id INTEGER primary key,name varchar(150));

    CREATE TABLE product
            (id INTEGER     primary key,    title varchar(300), 
            description varchar(2000), category_id integer not NULL,
            FOREIGN KEY(category_id) references category(id));

```

    
- You have to add columns to this commands :

``` 
    insert into category (id,name) values (1,'Basketball');
            insert into category (id,name) values (2,'Baseball');
            insert into category (id,name) values (3,'Frisbee');
            insert into category (id,name) values (4,'Snowboarding');
            insert into category (id,name) values (5,'Rock Climbing');
            insert into category (id,name) values (6,'Foosball');
            insert into category (id,name) values (7,'Skating');
            insert into category (id,name) values (8,'Hockey');
	```
     
	 insert into product (id,title,description,category_id) values (1,'Goggles','Lorem Ipsum is simply dummy text of the printing and typesetting industry',4);
            insert into product (id,title,description,category_id) values (2,'Snowboard','Lorem Ipsum has been the industrys standard dummy text ever since the 1500s',4);
            insert into product (id,title,description,category_id) values (3,'Frisbee','when an unknown printer took a galley of type and scrambled it to make a type specimen book',3);
            insert into product (id,title,description,category_id) values (4,'Bat','It has survived not only five centuries',2);

- Quit the database :

    `\q`

- For Packages, run this commend : 
	`sudo pip install -r requirements.txt`

    ( When you havan't install pip, you can run once "npm i pip" comment )

- Go to Catalog Path :

    `cd catalog/`

After Run

`python application.py`

*: If you want to new Item Add :

- Sigup User Name and Password or Sigup to Google Account

-----

Mete  | Demirtas
------------- | -------------
Udacity | Full Stack Web Development
Python  | Item Catalog 
