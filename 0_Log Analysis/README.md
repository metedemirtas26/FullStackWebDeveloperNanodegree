
********* Udaciy Full Stack Web development Logs Analysis Project *********

- Download the project

- Go vagrant Path : ...\FSND-Virtual-Machine\vagrant>

- run to "vagrant up" command and after run "vagrant ssh" command

    # If you didn't install Vagrant, you can install this adress : https://www.vagrantup.com/downloads.html

    # If you didn't install VirtualBox, you can install this adress : https://www.virtualbox.org/wiki/Downloads

- Then go in machine 'vagrant' path : Command => "cd /vagrant"

- If you want to go sql command line, run "psql forum" command 
    ( psql command can run sql database and we can write sql query, forum is database name )

- After then you can write your sql query. (For exp : "select 2+2;")

* Question of Answers :

   1. What are the most popular three articles of all time? 

    Query : select a.title, mp.views from articles a, (select l.path,count(l.path) as views from log l where length(l.path)>5 and l.method = 'GET' and status='200 OK' group by l.path order by views desc limit 3) mp where right(mp.path,-9)=a.slug;
        
        Results :
                    "Candidate is jerk, alleges rival" --- 338647 views 
                    "Bears love berries, alleges bear" --- 253801 views 
                    "Bad things gone, say good people" --- 170098 views 

   2. Who are the most popular article authors of all time? 

    Query : select au.name, count(au.name) as views from authors au, articles ar,log l where au.id = ar.author and right(l.path,-9)=ar.slug and l.method = 'GET' and l.status='200 OK' group by au.name order by views desc;
        
        Results :
                    Markoff Chaney --- 84557 views 
                    Anonymous Contributor --- 170098 views 
                    Rudolf von Treppenwitz --- 423457 views 
                    Ursula La Multa --- 507594 views 


   3. On which days did more than 1% of requests lead to errors?

    Query : select datenf as datum, CAST(countNok AS float)*100/CAST(countOk AS float) as errorPercent from (select dateNf,count(dateNf) as countNok from (select TO_CHAR(time :: DATE, 'dd/mm/yyyy') as dateNf from log where status='404 NOT FOUND') as nfTable group by dateNf) as tableNok,(select dateOk,count(dateOk) as countOk from (select TO_CHAR(time :: DATE, 'dd/mm/yyyy') as dateOk from log) as okTable group by dateOk) as tableOk where tableOk.dateOk=tableNok.datenf and countNok*100>countOk; 

        Results :

                  17/07/2016 --- 2.26268624680273 percent errors 
       
** Additionaly, You can also see results of queries on web browser

- Go 'forum' path : Write "cd forum"

- In command line, Write "python forum.py" command. (Run the python code)

- Open your Browser 'http://localhost:8000/' => You can see first questions answer, can't see?

- If you open 'http://localhost:8000/2' , you can see second questions answer 

  And If you open 'http://localhost:8000/3' , you can see third questions answer :)

That very simple.. ;)


