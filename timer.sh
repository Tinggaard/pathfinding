#/bin/sh

# create file (truncate if exists)
date > timings.txt

dir="solutions/"

# -v flag available
[ "$1" = "-v" ] || [ "$1" = "-V" ] && verbose=true || verbose=false

# algs to iterate
algs="dijkstra
astar
breadthfirst
depthfirst
rightturn"

# create dir for solutions
[ ! -d $dir ] && mkdir $dir

# iterate folders
for folder in mazes/*/ ; do

  # the sub-dir to create
  comb="$dir$(echo $folder | cut --complement -c 1-6)"

  # create sub-dirs for each generation method
  if [ ! -d $comb ]; then
    echo "Creating folder $comb"
    mkdir $comb

    # create sub-sub dir for algorithms
    cd $comb
    mkdir $algs
    cd ../..
  fi

  # iterate files in each folder (after size order)
  # for img in `ls -v $folder`; do

  # skip the very large images
  for im in 51 101 501 1001 2501 ; do
    img="$im.png"

    # iterate algorithms
    for alg in $algs ; do

      #input file
      i=$folder$img
      # output file
      o="$comb$alg/$img"

      # print if verbose
      $verbose && echo "Working on '$i' with algorithm $alg"

      # append the output to a file
      pathfinding solve $i -a $alg -o $o -f >> timings.txt
      # echo "pathfinding solve $i -a $alg -o $o -f" >> timings.txt

    done
  done
done
