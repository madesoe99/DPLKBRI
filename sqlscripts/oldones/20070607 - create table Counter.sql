/* Creating table for class counter */

CREATE TABLE COUNTER(
  ID_CODE VARCHAR(50) NOT NULL,
  LAST_ID INTEGER,
  IS_LOCKED INTEGER,
PRIMARY KEY (ID_CODE)
);