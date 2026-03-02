df = (spark.sql("select element_at(split(regexp_replace(advanasys_filename_raw, '\\.complete$', ''), '/'), -1) AS FIL_NM, transaction_set_control_number_st as TRNSCN_SET_CTL_ID, r4_values, 'DAAS' as SRC_NM, CAST(transaction_set_control_number_st as INT) as FIL_REC_NB, TO_DATE(SUBSTRING(advanasys_filename_raw, CHARINDEX('315A_20', advanasys_filename_raw) + 5, 8), 'yyyyMMdd') as OBSRVN_DT from dla_daas.dteb_315a where advanasys_filename_raw like '%20240205_190509000_0000001140%'"))

df.display()
