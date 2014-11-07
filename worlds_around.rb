require 'json'
require 'date'
require_relative "haversine.rb"

class WorldsAround
  attr_accessor :worlds_array
  attr_reader :user, :worlds
  def initialize(user_file, worlds_file)
    @user = JSON.parse(File.read("sample_user.json"))["user"]
    @worlds_array = JSON.parse(File.read("sample_worlds.json"))["data"]
  end
  def active_worlds
    userdatetime = DateTime.parse(user["usertime"])
    @worlds_array.select do |world|
      if world["time"]["timestart"]
       starttime = DateTime.parse(world["time"]["timestart"])
       endtime = DateTime.parse(world["time"]["timeend"])
       starttime < userdatetime && endtime > userdatetime
     end || (world["time"]["timestart"] == nil )
   end
  end
  def within_worlds
    userloc = user["userloc"]["coordinates"]
    lat1, long1 = userloc[0], userloc[1]
    active_worlds.select do |world|
      worldloc = world["loc"]["coordinates"]
      worldradius = world["radius"]
      lat2, long2 = worldloc[0], worldloc[1]
      haversine(lat1, long1, lat2, long2) < worldradius
    end
  end
  def rank_worlds
    within_worlds.map do |world|
      count = 0
      world["tags"].each do |worldtag|
        user["tags"].each do |usertag|
          if worldtag == usertag
            count += 1
          end
        end
      end
      world["shared_tag_count"] = count
      world
    end.sort_by do |world| 
      world["shared_tag_count"]
    end.reverse
  end
end

a = WorldsAround.new('sample_user.json', 'sample_worlds.json')
a.rank_worlds