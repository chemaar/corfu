require 'rubygems'
require 'tweetstream'

TweetStream.configure do |config|
  config.consumer_key       = 'CH1c6Cb24PN3yPPmTFA'
  config.consumer_secret    = 'L2jREcQTR9WjJS0mUwBrIYRoUUHrayqCsRjOzfI20'
  config.oauth_token        = '6484062-g6wHZPohAGIu1LfgQjPl74ndPw6KPqDIWrHEFwOIt2'
  config.oauth_token_secret = 'PZEGBYgx9JXzyCRUmnkiSf7wueZfRkjhj3ai0bHJjSbJo'
  config.auth_method        = :oauth
end


EM.run do


	infile = File.open("seed-words-expanded.txt", 'r')
	contentsArray=[] 
	infile.each_line {|line|	
	    contentsArray.push line.sub('_',' ')
	  }
        infile.close
	puts contentsArray

	root = File.expand_path(File.join(File.dirname(__FILE__), '..'))
	#require File.join(root, "config", "environment")

	daemon = TweetStream::Daemon.new('tracker', :log_output => true)
	daemon.on_inited do
	  ActiveRecord::Base.connection.reconnect!
	  ActiveRecord::Base.logger = Logger.new(File.open('stream.log', 'w+'))
	end
	daemon.track(contentsArray) do |tweet|
	  puts tweet
	  Status.create_from_tweet(tweet)
	end

end
