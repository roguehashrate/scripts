#!/usr/bin/env ruby
# This basic little program is made to display the julian calendar as well as tell you the full yy-ddd format at the bottom
require 'rainbow/refinement'
using Rainbow

puts "Julian Calendar".yellow

system("ncal -j")
puts "\n"

today = %x(date +%g%j)
puts "Today is: #{today}".green

