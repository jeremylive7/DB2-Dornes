CREATE TABLE IF NOT EXISTS public.supercarros
(
    id integer NOT NULL,
    precio integer NOT NULL,
    motor varchar(50) NOT NULL,
    CONSTRAINT supercarros_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.supercarros
    OWNER to postgres;
	
	
	
	
CREATE TABLE IF NOT EXISTS public.motos
(
    id integer NOT NULL,
    precio integer NOT NULL,
    motor varchar(50) NOT NULL,
	tipo varchar(50) NOT NULL,
    CONSTRAINT motos_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.motos
    OWNER to postgres;
	
	
	
	
	
insert into public.supercarros values(1,500,'100mil caballos de fuerza');
insert into public.supercarros values(2,200,'20mil caballos de fuerza');
insert into public.supercarros values(3,300,'50mil caballos de fuerza');


insert into public.motos values(1,20,'50 calbarros de fuerza','normal');
insert into public.motos values(2,40,'70 calbarros de fuerza','super');
insert into public.motos values(3,60,'90 calbarros de fuerza','turbo');

