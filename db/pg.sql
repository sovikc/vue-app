CREATE TABLE user_account (
  account_id serial NOT NULL PRIMARY KEY,
  account_uuid varchar(50) NOT NULL UNIQUE,
  full_name varchar(300) NOT NULL,
  email varchar(200) NOT NULL UNIQUE,
  pass varchar(200) NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_actioned_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE report (
  report_id serial NOT NULL PRIMARY KEY,
  report_uuid varchar(50) NOT NULL UNIQUE,
  report_label text,
  account_uuid varchar(50),
  locale varchar(200) NOT NULL,
  timezone varchar(200) NOT NULL,
  timezone_offset interval,
  tz_daylight_savings boolean,
  has_timezone_data boolean,
  record_console_log_requested boolean,
  record_network_log_requested boolean,
  ip_address varchar(200),
  video_location varchar(200),
  env_log_location varchar(200),
  session_log_location varchar(200),
  audio_file_location varchar(200),
  console_log_location varchar(200),
  network_log_location varchar(200),
  perf_log_location varchar(200),
  report_description text,
  session_start_time timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  session_end_time timestamp with time zone,
  session_using_start_page boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE console_log_entry (
  console_log_id serial NOT NULL PRIMARY KEY,
  report_uuid varchar(50) NOT NULL,
  account_uuid varchar(50),
  log_level varchar(50) NOT NULL,
  log_source varchar(50) NOT NULL,
  log_text text,
  entry_timestamp decimal,
  log_url text,
  entry_record jsonb
);

CREATE TABLE network_log_entry (
  network_log_id serial NOT NULL PRIMARY KEY,
  report_uuid varchar(50) NOT NULL,
  account_uuid varchar(50),
  request_id varchar(50) NOT NULL,
  resource_type varchar(50),
  resource_url text,
  network_event varchar(50) NOT NULL,
  entry_timestamp decimal NOT NULL,
  entry_wall_time decimal,
  entry_record jsonb NOT NULL
);
