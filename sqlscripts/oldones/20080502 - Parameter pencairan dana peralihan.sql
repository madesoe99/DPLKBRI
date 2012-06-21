INSERT INTO PARAMETER
  (key_parameter, numeric_value, varchar_value, description)
VALUES     ('PSN_CM_ALIH_<1TH', 3.0, NULL, '% by manfaat untuk dana peralihan < 1 TH');

UPDATE PARAMETER
SET numeric_value = 1 WHERE key_parameter = 'PERSEN_CAIR_MANFAAT_<1TH';

UPDATE PARAMETER
SET numeric_value = 1 WHERE key_parameter = 'PERSEN_CAIR_MANFAAT_>=1TH';
