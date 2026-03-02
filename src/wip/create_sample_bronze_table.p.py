edi_315A_df = df[df.Name.str.contains('315A')].iloc[:10001]
path_list = edi_315A_df['Path'].tolist()

binary_df = spark.read.format("binaryFile").load(path_list)
bronze_df = binary_df.withColumn("content", binary_df["content"].cast("string"))

display(bronze_df)
