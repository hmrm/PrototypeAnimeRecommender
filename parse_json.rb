require 'json'

data = JSON.parse(STDIN.read)["anime"]

ratings = Array.new(15177)

ratings.map! { |x| 0 }

data.each do |dict|
  ratings[dict["id"].to_i] = dict["score"].to_f.to_i
end

print ratings
