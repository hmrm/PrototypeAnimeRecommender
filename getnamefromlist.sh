while read -r line
do
    curl "http://mal-api.com/anime/"$line | ruby getname.rb
done