#/bin/sh

# create file (truncate if exists)
date > timings.txt

# iterate folders
for folder in mazes/*/ ; do
# for folder in */ ; do

  # iterate files in each folder (after size order)
  for img in `ls -v $folder`; do

    # iterate algorithms
    for alg in dijkstra astar breadthfirst depthfirst rightturn ; do
      # append the output to a file
      # ./src/main.py -i $img -a $alg -v >> timings.txt
      echo "./src/main.py -i $img -a $alg" >> timings.txt

    done
  done
done
