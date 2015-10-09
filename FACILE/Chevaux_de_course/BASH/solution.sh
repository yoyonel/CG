#!/usr/bin/env bash
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# quicksorts positional arguments
# return is in array qsort_ret
# Note: iterative, NOT recursive! :)
qsort() {
   (($#==0)) && return 0
   local stack=( 0 $(($#-1)) ) beg end i pivot smaller larger
   qsort_ret=("$@")
   while ((${#stack[@]})); do
      beg=${stack[0]}
      end=${stack[1]}
      stack=( "${stack[@]:2}" )
      smaller=() larger=()
      pivot=${qsort_ret[beg]}
      for ((i=beg+1;i<=end;++i)); do
         if [[ "${qsort_ret[i]}" < "$pivot" ]]; then
            smaller+=( "${qsort_ret[i]}" )
         else
            larger+=( "${qsort_ret[i]}" )
         fi
      done
      qsort_ret=( "${qsort_ret[@]:0:beg}" "${smaller[@]}" "$pivot" "${larger[@]}" "${qsort_ret[@]:end+1}" )
      if ((${#smaller[@]}>=2)); then stack+=( "$beg" "$((beg+${#smaller[@]}-1))" ); fi
      if ((${#larger[@]}>=2)); then stack+=( "$((end-${#larger[@]}+1))" "$end" ); fi
   done
}

read N
array=()
for (( i=0; i<N; i++ )); do
    read Pi
    array+=Pi
done

qsort "${array[@]}"
declare -p qsort_ret

let "min_sub=50000000"
for (( i=1; i<N-1; i++ )); do
    let "sub=qsort_ret[i-1]-qsort_ret[i]"
    let "min_sub=sub<min_sub?sub:min_sub"
done

# Write an action using echo
# To debug: echo "Debug messages..." >&2
echo min