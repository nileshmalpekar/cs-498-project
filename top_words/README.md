### Run Top Mapper / Reducer

- Remove output directory
`hadoop fs -rm -r -f output-count/`

- Create HDFS folder
`hadoop fs -mkdir -p ./input`

- Copy captions inside dataset (out of docker proccess)
`cp -p ../../captions/* ./dataset`

- Copy dataset to input folder
`hadoop fs -put ./dataset/* ./input`

- Count Words
`hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar -mapper 'word_count_mapper.py stopwords.txt' -file word_count_mapper.py -reducer 'word_count_reducer.py' -file word_count_reducer.py -input input/ -output output`

- Export counts
`hadoop fs -get output/part-00000 export/word-count.txt`

- Get Top (out of docker proccess)
`python top_words.py`
