-- Ejm de como crear una tabla

CREATE TABLE IF NOT EXISTS maquinas."motos"
(
    marca varchar(50) NOT NULL,
	motor varchar(50) NOT NULL,
    precio integer NOT NULL,
    CONSTRAINT motos_pkey PRIMARY KEY (marca)
)

TABLESPACE pg_default;

ALTER TABLE maquinas."motos"
    OWNER to postgres;
	

-- Insert

insert into maquinas.motos values('Toyota','400 caballos de fuerza',300)

-- Select

select * from maquinas.motos
