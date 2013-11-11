require 'rubygems'
require 'tweetstream'
require 'yaml'
require 'json'

TweetStream.configure do |config|
  config.consumer_key       = 'CH1c6Cb24PN3yPPmTFA'
  config.consumer_secret    = 'L2jREcQTR9WjJS0mUwBrIYRoUUHrayqCsRjOzfI20'
  config.oauth_token        = '6484062-g6wHZPohAGIu1LfgQjPl74ndPw6KPqDIWrHEFwOIt2'
  config.oauth_token_secret = 'PZEGBYgx9JXzyCRUmnkiSf7wueZfRkjhj3ai0bHJjSbJo'
  config.auth_method        = :oauth
end


EM.run do
	MAX_TWEETS = 10000
	tweets = 0
	nfile = 0 
        rawword = ARGV[0] 
	word = rawword.sub('_',' ')
	file = File.open(rawword+"/"+word+"-"+nfile.to_s(),  File::RDWR|File::CREAT, 0755)
	TweetStream::Client.new.on_error do |message|
	  puts "Error reading stream: #{message}"
	end.track(word) do |status|
	  begin
		file.puts status.to_yaml
		file.flush
		tweets += 1
		if tweets > MAX_TWEETS
		 nfile += 1
		 tweets = 0
		 file.close unless file == nil
	 	 file = File.open(rawword+"/"+word+"-"+nfile.to_s(),  File::RDWR|File::CREAT, 0755)
		end
		rescue IOError => e
		 #some error occur, dir not writable etc.
		 puts "Error writing file...: #{e}"
		 puts e
		rescue StandardError => e
		 puts e
		 puts "Unknown error writing file..."
		#ensure
		# file.close unless file == nil
		
	  end
	end
end
