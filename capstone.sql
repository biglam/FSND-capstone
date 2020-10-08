--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4 (Ubuntu 12.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.4 (Ubuntu 12.4-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actor_movies; Type: TABLE; Schema: public; Owner: lam
--

CREATE TABLE public.actor_movies (
    actor_id integer NOT NULL,
    movie_id integer NOT NULL
);


ALTER TABLE public.actor_movies OWNER TO lam;

--
-- Name: actors; Type: TABLE; Schema: public; Owner: lam
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying NOT NULL,
    age integer NOT NULL,
    gender character varying NOT NULL
);


ALTER TABLE public.actors OWNER TO lam;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: lam
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO lam;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: lam
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: lam
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO lam;

--
-- Name: movies; Type: TABLE; Schema: public; Owner: lam
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying NOT NULL,
    release_date date NOT NULL
);


ALTER TABLE public.movies OWNER TO lam;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: lam
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO lam;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: lam
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actor_movies; Type: TABLE DATA; Schema: public; Owner: lam
--

COPY public.actor_movies (actor_id, movie_id) FROM stdin;
1	2
1	3
2	1
2	2
4	1
4	2
4	4
\.


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: lam
--

COPY public.actors (id, name, age, gender) FROM stdin;
1	jim	50	male
2	john	21	male
3	jenny	24	female
4	anna	60	female
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: lam
--

COPY public.alembic_version (version_num) FROM stdin;
df9a9fc0e62f
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: lam
--

COPY public.movies (id, title, release_date) FROM stdin;
1	movie 1	2000-02-01
2	movie 2	2002-02-01
3	movie 3	1980-02-21
4	xmas movie	2020-12-25
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lam
--

SELECT pg_catalog.setval('public.actors_id_seq', 4, true);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lam
--

SELECT pg_catalog.setval('public.movies_id_seq', 4, true);


--
-- Name: actor_movies actor_movies_pkey; Type: CONSTRAINT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.actor_movies
    ADD CONSTRAINT actor_movies_pkey PRIMARY KEY (actor_id, movie_id);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: movies movies_title_key; Type: CONSTRAINT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_title_key UNIQUE (title);


--
-- Name: actor_movies actor_movies_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.actor_movies
    ADD CONSTRAINT actor_movies_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(id);


--
-- Name: actor_movies actor_movies_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lam
--

ALTER TABLE ONLY public.actor_movies
    ADD CONSTRAINT actor_movies_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id);


--
-- PostgreSQL database dump complete
--

