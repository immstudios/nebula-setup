--
-- SYSTEM SETTINGS
--

CREATE TABLE public.settings (
        key VARCHAR(255) NOT NULL,
        value JSONB,
        CONSTRAINT settings_pkey PRIMARY KEY (key)
    );

CREATE TABLE public.storages (
        id serial NOT NULL,
        settings JSONB NOT NULL,
        CONSTRAINT storages_pkey PRIMARY KEY (id)
    );

CREATE TABLE public.channels (
        id SERIAL NOT NULL,
        channel_type INTEGER NOT NULL,
        settings JSONB NOT NULL,
        CONSTRAINT channels_pkey PRIMARY KEY (id)
    );

CREATE TABLE public.services (
        id SERIAL NOT NULL,
        service_type VARCHAR(50) NOT NULL,
        host VARCHAR(50) NOT NULL,
        title VARCHAR(50) NOT NULL,
        settings XML NULL,
        autostart BOOLEAN NOT NULL DEFAULT false,
        loop_delay INTEGER NOT NULL DEFAULT 5,
        state INTEGER NOT NULL DEFAULT 0,
        pid INTEGER NOT NULL DEFAULT 0,
        last_seen INTEGER NOT NULL DEFAULT 0,
        CONSTRAINT services_pkey PRIMARY KEY (id)
    );

CREATE TABLE public.actions (
        id SERIAL NOT NULL,
        service_type VARCHAR(255) NOT NULL,
        title VARCHAR(255) NOT NULL,
        settings XML NOT NULL,
        CONSTRAINT actions_pkey PRIMARY KEY (id)
    );

CREATE TABLE public.folders (
        id SERIAL NOT NULL,
        settings JSONB,
        CONSTRAINT folders_pkey PRIMARY KEY (id)
    );

CREATE TABLE public.meta_types (
        key VARCHAR(127) NOT NULL,
        settings JSONB NOT NULL,
        CONSTRAINT meta_types_pkey PRIMARY KEY (key)
    );

CREATE TABLE public.cs (
        cs VARCHAR(255) NOT NULL,
        value VARCHAR(255) NOT NULL,
        settings JSONB,
        CONSTRAINT cs_pkey PRIMARY KEY (cs, value)
    );

CREATE TABLE public.views (
        id SERIAL NOT NULL,
        title VARCHAR(255) NOT NULL,
        settings XML NOT NULL,
        owner INTEGER NOT NULL DEFAULT 0,
        position INTEGER NOT NULL DEFAULT 0,
        CONSTRAINT views_pkey PRIMARY KEY (id)
    );

--
-- MAM
--

-- ASSETS

CREATE TABLE public.assets (
        id SERIAL NOT NULL,
        id_folder INTEGER NOT NULL,
        content_type INTEGER NOT NULL,
        media_type INTEGER NOT NULL,
        status INTEGER NOT NULL DEFAULT 1,
        version_of INTEGER NOT NULL DEFAULT 0,
        ctime INTEGER NOT NULL,
        mtime INTEGER NOT NULL,
        meta JSONB,
        CONSTRAINT assets_pkey PRIMARY KEY (id)
    );

CREATE INDEX idx_folder ON assets(id_folder);
CREATE INDEX idx_content_type ON assets(content_type);
CREATE INDEX idx_media_type ON assets(media_type);
CREATE INDEX idx_status ON assets(id_folder);
CREATE INDEX idx_ctime ON assets(ctime);
CREATE INDEX idx_mtime ON assets(mtime);

-- BINS

CREATE TABLE public.bins (
        id SERIAL NOT NULL,
        bin_type INTEGER DEFAULT 0,
        meta JSONB,
        CONSTRAINT bins_pkey PRIMARY KEY (id)
    );

-- ITEMS

CREATE TABLE public.items (
        id SERIAL NOT NULL,
        id_asset INTEGER NOT NULL, -- can be zero (default, virtual item)
        id_bin INTEGER REFERENCES public.bins(id),
        position INTEGER NOT NULL,
        meta JSONB,
        CONSTRAINT items_pkey PRIMARY KEY (id)
    );

CREATE INDEX idx_items_asset ON items(id_asset);
CREATE INDEX idx_items_bin ON items(id_bin);

-- EVENTS

CREATE TABLE public.events (
        id SERIAL NOT NULL,
        id_channel INTEGER NOT NULL,
        start INTEGER NOT NULL,
        stop INTEGER,
        id_magic INTEGER,
        meta JSONB,
        CONSTRAINT events_pkey PRIMARY KEY (id)
    );

CREATE INDEX idx_event_channel ON events(id_channel);
CREATE INDEX idx_event_start ON events(start);
CREATE INDEX idx_event_magic ON events(id_magic);

-- USERS

CREATE TABLE public.users (
        id SERIAL NOT NULL,
        login VARCHAR(255) UNIQUE,
        password VARCHAR(255) NOT NULL,
        meta JSONB,
        CONSTRAINT users_pkey PRIMARY KEY (id)
    );

-- FULLTEXT INDEX

CREATE TABLE public.ft (
        id INTEGER NOT NULL,
        object_type INTEGER NOT NULL,
        weight INTEGER DEFAULT 0,
        value VARCHAR(255)
    );

CREATE INDEX idx_ft_id ON ft(id);
CREATE INDEX idx_ft_type ON ft(object_type);
CREATE INDEX idx_ft ON ft(value text_pattern_ops);

--
-- AUX
--

CREATE TABLE public.hosts (
        hostname VARCHAR(255) NOT NULL,
        last_seen INTEGER NOT NULL DEFAULT 0,
        status JSONB,
        CONSTRAINT hosts_pkey PRIMARY KEY(hostname)
    );

CREATE TABLE public.jobs (
        id SERIAL NOT NULL,
        id_action INTEGER NOT NULL,
        id_asset INTEGER,
        id_service INTEGER,
        id_user INTEGER,
        settings JSONB,
        priority INTEGER NOT NULL DEFAULT 3,
        retries INTEGER NOT NULL DEFAULT 0,
        status INTEGER DEFAULT 0,
        progress FLOAT NOT NULL DEFAULT 0,
        message TEXT NOT NULL DEFAULT 'Pending',
        creation_time INTEGER,
        start_time INTEGER,
        end_time INTEGER,
        CONSTRAINT jobs_pkey PRIMARY KEY (id)
    );

CREATE TABLE public.asrun (
        id SERIAL NOT NULL,
        id_channel INTEGER NOT NULL,
        id_item INTEGER REFERENCES public.items(id),
        id_asset INTEGER REFERENCES public.assets(id),
        start INTEGER NOT NULL,
        stop INTEGER NOT NULL,
        CONSTRAINT asrun_pkey PRIMARY KEY (id)
    );

CREATE INDEX asrun_start_idx ON asrun(start);
CREATE INDEX asrun_channel_idx ON asrun(id_channel);
CREATE INDEX asrun_asset_idx ON asrun(id_asset);
