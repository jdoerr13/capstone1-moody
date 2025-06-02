--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Postgres.app)
-- Dumped by pg_dump version 15.13 (Postgres.app)

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
-- Name: coping_solutions; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.coping_solutions (
    solution_id integer NOT NULL,
    solution_text text NOT NULL
);


ALTER TABLE public.coping_solutions OWNER TO jdboss;

--
-- Name: coping_solutions_solution_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.coping_solutions_solution_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.coping_solutions_solution_id_seq OWNER TO jdboss;

--
-- Name: coping_solutions_solution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.coping_solutions_solution_id_seq OWNED BY public.coping_solutions.solution_id;


--
-- Name: daily_assessment; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.daily_assessment (
    id integer NOT NULL,
    user_id integer,
    date date,
    weather_today character varying(64),
    mood_today character varying(64),
    stress_level text,
    positive_affect_rating text
);


ALTER TABLE public.daily_assessment OWNER TO jdboss;

--
-- Name: daily_assessment_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.daily_assessment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.daily_assessment_id_seq OWNER TO jdboss;

--
-- Name: daily_assessment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.daily_assessment_id_seq OWNED BY public.daily_assessment.id;


--
-- Name: diagnosis; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.diagnosis (
    issue_id integer NOT NULL,
    issue_name character varying(255) NOT NULL
);


ALTER TABLE public.diagnosis OWNER TO jdboss;

--
-- Name: diagnosis_issue_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.diagnosis_issue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.diagnosis_issue_id_seq OWNER TO jdboss;

--
-- Name: diagnosis_issue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.diagnosis_issue_id_seq OWNED BY public.diagnosis.issue_id;


--
-- Name: diagnosis_solutions; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.diagnosis_solutions (
    id integer NOT NULL,
    user_id integer,
    diagnosis_id integer,
    solution_id integer,
    solution_text text
);


ALTER TABLE public.diagnosis_solutions OWNER TO jdboss;

--
-- Name: diagnosis_solutions_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.diagnosis_solutions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.diagnosis_solutions_id_seq OWNER TO jdboss;

--
-- Name: diagnosis_solutions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.diagnosis_solutions_id_seq OWNED BY public.diagnosis_solutions.id;


--
-- Name: group_posts; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.group_posts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL,
    post_content character varying NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public.group_posts OWNER TO jdboss;

--
-- Name: group_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.group_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.group_posts_id_seq OWNER TO jdboss;

--
-- Name: group_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.group_posts_id_seq OWNED BY public.group_posts.id;


--
-- Name: groups; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.groups (
    group_id integer NOT NULL,
    group_name character varying(80) NOT NULL,
    description text
);


ALTER TABLE public.groups OWNER TO jdboss;

--
-- Name: groups_group_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.groups_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groups_group_id_seq OWNER TO jdboss;

--
-- Name: groups_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.groups_group_id_seq OWNED BY public.groups.group_id;


--
-- Name: journal_entries; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.journal_entries (
    id integer NOT NULL,
    user_id integer NOT NULL,
    date date NOT NULL,
    entry text NOT NULL
);


ALTER TABLE public.journal_entries OWNER TO jdboss;

--
-- Name: journal_entries_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.journal_entries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.journal_entries_id_seq OWNER TO jdboss;

--
-- Name: journal_entries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.journal_entries_id_seq OWNED BY public.journal_entries.id;


--
-- Name: user_diagnostic_ass; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.user_diagnostic_ass (
    user_id integer NOT NULL,
    diagnosis_id integer NOT NULL,
    date_recorded date
);


ALTER TABLE public.user_diagnostic_ass OWNER TO jdboss;

--
-- Name: user_friend_requests; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.user_friend_requests (
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL
);


ALTER TABLE public.user_friend_requests OWNER TO jdboss;

--
-- Name: user_friends; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.user_friends (
    user_id integer NOT NULL,
    friend_id integer NOT NULL
);


ALTER TABLE public.user_friends OWNER TO jdboss;

--
-- Name: user_group_association; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.user_group_association (
    user_id integer,
    group_id integer
);


ALTER TABLE public.user_group_association OWNER TO jdboss;

--
-- Name: user_history; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.user_history (
    history_id integer NOT NULL,
    user_id integer NOT NULL,
    weather_id integer NOT NULL,
    date_recorded date NOT NULL
);


ALTER TABLE public.user_history OWNER TO jdboss;

--
-- Name: user_history_history_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.user_history_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_history_history_id_seq OWNER TO jdboss;

--
-- Name: user_history_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.user_history_history_id_seq OWNED BY public.user_history.history_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    bio text,
    location character varying(255),
    image_url character varying(512),
    password character varying(120) NOT NULL,
    registration_date timestamp without time zone NOT NULL
);


ALTER TABLE public.users OWNER TO jdboss;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO jdboss;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: weather; Type: TABLE; Schema: public; Owner: jdboss
--

CREATE TABLE public.weather (
    weather_id integer NOT NULL,
    weather_date date NOT NULL,
    temperature_value double precision NOT NULL,
    temperature_unit character varying(10) NOT NULL,
    real_time_weather_type character varying(50),
    real_time_condition character varying(255),
    real_time_icon character varying(255),
    real_time_feelslike_f double precision,
    real_time_feelslike_c double precision,
    real_time_humidity integer,
    real_time_uv_index double precision,
    forecast_weather_type character varying(50),
    forecast_condition character varying(255),
    forecast_icon character varying(255),
    forecast_high_temp_f double precision,
    forecast_low_temp_f double precision,
    forecast_high_temp_c double precision,
    forecast_low_temp_c double precision
);


ALTER TABLE public.weather OWNER TO jdboss;

--
-- Name: weather_weather_id_seq; Type: SEQUENCE; Schema: public; Owner: jdboss
--

CREATE SEQUENCE public.weather_weather_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.weather_weather_id_seq OWNER TO jdboss;

--
-- Name: weather_weather_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jdboss
--

ALTER SEQUENCE public.weather_weather_id_seq OWNED BY public.weather.weather_id;


--
-- Name: coping_solutions solution_id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.coping_solutions ALTER COLUMN solution_id SET DEFAULT nextval('public.coping_solutions_solution_id_seq'::regclass);


--
-- Name: daily_assessment id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.daily_assessment ALTER COLUMN id SET DEFAULT nextval('public.daily_assessment_id_seq'::regclass);


--
-- Name: diagnosis issue_id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.diagnosis ALTER COLUMN issue_id SET DEFAULT nextval('public.diagnosis_issue_id_seq'::regclass);


--
-- Name: diagnosis_solutions id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.diagnosis_solutions ALTER COLUMN id SET DEFAULT nextval('public.diagnosis_solutions_id_seq'::regclass);


--
-- Name: group_posts id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.group_posts ALTER COLUMN id SET DEFAULT nextval('public.group_posts_id_seq'::regclass);


--
-- Name: groups group_id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.groups ALTER COLUMN group_id SET DEFAULT nextval('public.groups_group_id_seq'::regclass);


--
-- Name: journal_entries id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.journal_entries ALTER COLUMN id SET DEFAULT nextval('public.journal_entries_id_seq'::regclass);


--
-- Name: user_history history_id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_history ALTER COLUMN history_id SET DEFAULT nextval('public.user_history_history_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: weather weather_id; Type: DEFAULT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.weather ALTER COLUMN weather_id SET DEFAULT nextval('public.weather_weather_id_seq'::regclass);


--
-- Data for Name: coping_solutions; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.coping_solutions (solution_id, solution_text) FROM stdin;
1	Stay informed about climate issues and actions you can take.
2	Practice eco-friendly habits to reduce personal environmental impact.
3	Seek professional therapy to address anxiety and fears related to climate change.
4	Create an emergency plan for your family and home.
5	Stay informed about disaster preparedness and local resources.
6	Consider professional therapy to address disaster-related anxiety.
7	Monitor weather forecasts and plan activities accordingly.
8	Engage in mood-boosting activities on gloomy days.
9	Consider therapy to manage mood swings influenced by the weather.
10	Use light therapy to mitigate the effects of reduced daylight.
11	Stay active and maintain a consistent daily routine.
12	Consult a mental health professional for SAD-specific therapies.
13	Engage in indoor hobbies or activities during poor weather.
14	Practice relaxation techniques to reduce stress and cabin fever.
15	Seek therapy for managing stress and coping with weather-induced stress.
16	Monitor your physical symptoms and seek medical advice as needed.
17	Stay active and maintain a healthy lifestyle regardless of the weather.
18	Consult healthcare professionals for addressing weather-induced physical issues.
\.


--
-- Data for Name: daily_assessment; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.daily_assessment (id, user_id, date, weather_today, mood_today, stress_level, positive_affect_rating) FROM stdin;
\.


--
-- Data for Name: diagnosis; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.diagnosis (issue_id, issue_name) FROM stdin;
1	Climate Change or Environmental Anxiety
2	Major Disaster or Severe Weather Anxiety
3	Weather-Induced Mood Swings (Moody)
4	Seasonal Affective Disorder (SAD)
5	General Weather Stress or Cabin Fever
6	Weather-Induced Physical Issues
\.


--
-- Data for Name: diagnosis_solutions; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.diagnosis_solutions (id, user_id, diagnosis_id, solution_id, solution_text) FROM stdin;
1	\N	1	1	Stay informed about disaster preparedness and local resources.
2	\N	1	2	Practice eco-friendly habits to reduce personal environmental impact.
3	\N	1	3	Seek professional therapy to address anxiety and fears related to climate change.
4	\N	2	4	Create an emergency plan for your family and home.
5	\N	2	5	Stay active and maintain a consistent daily routine.
6	\N	2	6	Consider professional therapy to address disaster-related anxiety.
7	\N	3	7	Monitor weather forecasts and plan activities accordingly.
8	\N	3	8	Engage in mood-boosting activities on gloomy days.
9	\N	3	9	Consider therapy to manage mood swings influenced by the weather.
10	\N	4	10	Use light therapy to mitigate the effects of reduced daylight.
11	\N	4	11	Stay active and maintain a consistent daily routine.
12	\N	4	12	Consult a mental health professional for SAD-specific therapies.
13	\N	5	13	Engage in indoor hobbies or activities during poor weather.
14	\N	5	14	Practice relaxation techniques to reduce stress and cabin fever.
15	\N	5	15	Seek therapy for managing stress and coping with weather-induced stress.
16	\N	6	16	Monitor your physical symptoms and seek medical advice as needed.
17	\N	6	17	Stay active and maintain a healthy lifestyle regardless of the weather.
18	\N	6	18	Consult healthcare professionals for addressing weather-induced physical issues.
\.


--
-- Data for Name: group_posts; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.group_posts (id, user_id, group_id, post_content, "timestamp") FROM stdin;
1	1	3	sadfsadfasdf	2023-11-27 20:29:55.986833
\.


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.groups (group_id, group_name, description) FROM stdin;
1	Climate Change Anxiety	Group for climate change-related discussions.
2	Major Disaster/Severe Weather Anxiety	Group for extreme weather and disaster discussions.
3	Weather makes me moody	Group for discussing mood and weather correlations.
4	SAD	Group for Seasonal Affective Disorder (SAD) support.
5	General Weather Stress/ Cabin Fever	Group for general weather-related stress discussions.
6	Weather & Physical Health	Weather & Physical Health
\.


--
-- Data for Name: journal_entries; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.journal_entries (id, user_id, date, entry) FROM stdin;
\.


--
-- Data for Name: user_diagnostic_ass; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.user_diagnostic_ass (user_id, diagnosis_id, date_recorded) FROM stdin;
\.


--
-- Data for Name: user_friend_requests; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.user_friend_requests (sender_id, receiver_id) FROM stdin;
\.


--
-- Data for Name: user_friends; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.user_friends (user_id, friend_id) FROM stdin;
\.


--
-- Data for Name: user_group_association; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.user_group_association (user_id, group_id) FROM stdin;
1	3
\.


--
-- Data for Name: user_history; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.user_history (history_id, user_id, weather_id, date_recorded) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.users (user_id, username, email, bio, location, image_url, password, registration_date) FROM stdin;
1	Jaime	Jaime@gmail.com	sdfsdfsdfsdf	Boca Raton, FL	1ec342ea-6681-4b8f-83e7-22498e351b55static-1522050.jpg	$2b$12$2uLavzp79U8O7U7BCul8..qKAk9oLwefgE8D8Ij0esMTzAEl/sjd2	2023-11-27 20:28:54.392768
2	jdoerr	jdoerr13@gmail.com	\N	\N	\N	$2b$12$gCFX.uMDytsvBeyBAHt.ouc7DzsUoEQYU4MYUzF42H2TEDAaHEKky	2025-05-09 18:26:42.805182
\.


--
-- Data for Name: weather; Type: TABLE DATA; Schema: public; Owner: jdboss
--

COPY public.weather (weather_id, weather_date, temperature_value, temperature_unit, real_time_weather_type, real_time_condition, real_time_icon, real_time_feelslike_f, real_time_feelslike_c, real_time_humidity, real_time_uv_index, forecast_weather_type, forecast_condition, forecast_icon, forecast_high_temp_f, forecast_low_temp_f, forecast_high_temp_c, forecast_low_temp_c) FROM stdin;
\.


--
-- Name: coping_solutions_solution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.coping_solutions_solution_id_seq', 1, false);


--
-- Name: daily_assessment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.daily_assessment_id_seq', 1, false);


--
-- Name: diagnosis_issue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.diagnosis_issue_id_seq', 1, false);


--
-- Name: diagnosis_solutions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.diagnosis_solutions_id_seq', 18, true);


--
-- Name: group_posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.group_posts_id_seq', 1, true);


--
-- Name: groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.groups_group_id_seq', 6, true);


--
-- Name: journal_entries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.journal_entries_id_seq', 1, false);


--
-- Name: user_history_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.user_history_history_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.users_user_id_seq', 2, true);


--
-- Name: weather_weather_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jdboss
--

SELECT pg_catalog.setval('public.weather_weather_id_seq', 1, false);


--
-- Name: coping_solutions coping_solutions_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.coping_solutions
    ADD CONSTRAINT coping_solutions_pkey PRIMARY KEY (solution_id);


--
-- Name: daily_assessment daily_assessment_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.daily_assessment
    ADD CONSTRAINT daily_assessment_pkey PRIMARY KEY (id);


--
-- Name: diagnosis diagnosis_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.diagnosis
    ADD CONSTRAINT diagnosis_pkey PRIMARY KEY (issue_id);


--
-- Name: diagnosis_solutions diagnosis_solutions_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.diagnosis_solutions
    ADD CONSTRAINT diagnosis_solutions_pkey PRIMARY KEY (id);


--
-- Name: group_posts group_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.group_posts
    ADD CONSTRAINT group_posts_pkey PRIMARY KEY (id);


--
-- Name: groups groups_group_name_key; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_group_name_key UNIQUE (group_name);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (group_id);


--
-- Name: journal_entries journal_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.journal_entries
    ADD CONSTRAINT journal_entries_pkey PRIMARY KEY (id);


--
-- Name: user_diagnostic_ass user_diagnostic_ass_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_diagnostic_ass
    ADD CONSTRAINT user_diagnostic_ass_pkey PRIMARY KEY (user_id, diagnosis_id);


--
-- Name: user_friend_requests user_friend_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_friend_requests
    ADD CONSTRAINT user_friend_requests_pkey PRIMARY KEY (sender_id, receiver_id);


--
-- Name: user_friends user_friends_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_friends
    ADD CONSTRAINT user_friends_pkey PRIMARY KEY (user_id, friend_id);


--
-- Name: user_history user_history_date_recorded_key; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_history
    ADD CONSTRAINT user_history_date_recorded_key UNIQUE (date_recorded);


--
-- Name: user_history user_history_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_history
    ADD CONSTRAINT user_history_pkey PRIMARY KEY (history_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: weather weather_pkey; Type: CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.weather
    ADD CONSTRAINT weather_pkey PRIMARY KEY (weather_id);


--
-- Name: daily_assessment daily_assessment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.daily_assessment
    ADD CONSTRAINT daily_assessment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: diagnosis_solutions diagnosis_solutions_diagnosis_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.diagnosis_solutions
    ADD CONSTRAINT diagnosis_solutions_diagnosis_id_fkey FOREIGN KEY (diagnosis_id) REFERENCES public.diagnosis(issue_id);


--
-- Name: diagnosis_solutions diagnosis_solutions_solution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.diagnosis_solutions
    ADD CONSTRAINT diagnosis_solutions_solution_id_fkey FOREIGN KEY (solution_id) REFERENCES public.coping_solutions(solution_id);


--
-- Name: diagnosis_solutions diagnosis_solutions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.diagnosis_solutions
    ADD CONSTRAINT diagnosis_solutions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: group_posts group_posts_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.group_posts
    ADD CONSTRAINT group_posts_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(group_id);


--
-- Name: group_posts group_posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.group_posts
    ADD CONSTRAINT group_posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: journal_entries journal_entries_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.journal_entries
    ADD CONSTRAINT journal_entries_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_diagnostic_ass user_diagnostic_ass_diagnosis_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_diagnostic_ass
    ADD CONSTRAINT user_diagnostic_ass_diagnosis_id_fkey FOREIGN KEY (diagnosis_id) REFERENCES public.diagnosis(issue_id);


--
-- Name: user_diagnostic_ass user_diagnostic_ass_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_diagnostic_ass
    ADD CONSTRAINT user_diagnostic_ass_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_friend_requests user_friend_requests_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_friend_requests
    ADD CONSTRAINT user_friend_requests_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.users(user_id);


--
-- Name: user_friend_requests user_friend_requests_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_friend_requests
    ADD CONSTRAINT user_friend_requests_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(user_id);


--
-- Name: user_friends user_friends_friend_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_friends
    ADD CONSTRAINT user_friends_friend_id_fkey FOREIGN KEY (friend_id) REFERENCES public.users(user_id);


--
-- Name: user_friends user_friends_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_friends
    ADD CONSTRAINT user_friends_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_group_association user_group_association_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_group_association
    ADD CONSTRAINT user_group_association_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(group_id);


--
-- Name: user_group_association user_group_association_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_group_association
    ADD CONSTRAINT user_group_association_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_history user_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_history
    ADD CONSTRAINT user_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_history user_history_weather_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jdboss
--

ALTER TABLE ONLY public.user_history
    ADD CONSTRAINT user_history_weather_id_fkey FOREIGN KEY (weather_id) REFERENCES public.weather(weather_id);


--
-- PostgreSQL database dump complete
--

