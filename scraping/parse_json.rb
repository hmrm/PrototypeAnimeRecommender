require 'json'

data = JSON.parse(STDIN.read)["anime"]

data.each do |dict|
  print dict["id"].to_i 
  print " "
  print dict["score"].to_f.to_i
  print ","
end
puts ""
