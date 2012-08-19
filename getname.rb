require 'json'

data = JSON.parse(STDIN.read)
puts data["title"]
