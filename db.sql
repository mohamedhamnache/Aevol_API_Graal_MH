CREATE TABLE deployment ( 
    id_deployment int unsigned not null auto_increment,
    job_name varchar(40) not null,
    nb_nodes int unsigned not null,
    frontend varchar(40) not null,
    walltime int unsigned not null,
    job_id int unsigned not null,
    deployment_time int unsigned not null,
    primary key (id_deployment) 
)ENGINE = InnoDB;




CREATE TABLE g5khosts (
  id_host INT not null auto_increment,
  id_dep INT unsigned,
  hostName varchar(50) NOT NULL,
  INDEX par_ind (id_dep),
  primary key (id_host),
  CONSTRAINT fk_g5khosts FOREIGN KEY (id_dep)
  REFERENCES deployment(id_deployment)
  ON DELETE CASCADE
  ON UPDATE CASCADE
) ENGINE=INNODB;

CREATE TABLE Users ( 
    ID_USER int not null auto_increment,
    Password varchar(120) not null,
    Name varchar(40) not null,
    primary key (Id_USER) 
)ENGINE = InnoDB;

CREATE TABLE Jobs ( 
    ID_JOB int not null auto_increment,
    ID_USER int  not null ,
    Nom_simu varchar(120) not null,
    Statut varchar(40) not null,
    Start_time DATETIME,
    End_time DATETIME,
    Percentage int,
    id_deployment int unsigned,
    primary key (ID_JOB),
    CONSTRAINT fk_USER FOREIGN KEY (ID_USER)
    REFERENCES Users(ID_USER)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    CONSTRAINT fk_deployment FOREIGN KEY (id_deployment)
    REFERENCES deployment(id_deployment)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)ENGINE = InnoDB;
