require 'rubygems'
require 'tweetstream'
require 'json'

TweetStream.configure do |config|
  config.consumer_key       = 'CH1c6Cb24PN3yPPmTFA'
  config.consumer_secret    = 'L2jREcQTR9WjJS0mUwBrIYRoUUHrayqCsRjOzfI20'
  config.oauth_token        = '6484062-g6wHZPohAGIu1LfgQjPl74ndPw6KPqDIWrHEFwOIt2'
  config.oauth_token_secret = 'PZEGBYgx9JXzyCRUmnkiSf7wueZfRkjhj3ai0bHJjSbJo'
  config.auth_method        = :oauth
end


EM.run do
	MAX_TWEETS = 10
	tweets = 0
	nfile = 0 
	infile = File.open("mini-seed-words-expanded.txt", 'r')
	contentsArray=[] 
	infile.each_line {|line|	
	    contentsArray.push line.sub('_',' ')
	  }
        infile.close
	puts contentsArray
	file = File.open("tweets-"+nfile.to_s(),  File::RDWR|File::CREAT, 0644)
	if file
	 puts "Open"
	end
	TweetStream::Client.new.on_error do |message|
	  puts "Error reading stream: #{message}"
	end.track(contentsArray) do |status|
	  begin
		puts status.text
		file.puts status.inspect
		file.flush
		tweets += 1
		puts tweets.to_s()
		if tweets > MAX_TWEETS
		 nfile += 1
		 tweets = 0
		 file.close unless file == nil
		 file = File.open("tweets-"+nfile.to_s(),  File::RDWR|File::CREAT, 0644)
		end
		rescue IOError => e
		 #some error occur, dir not writable etc.
		 puts "Error writing file...: #{e}"
		 puts e
		rescue 
		 puts "Unknown error writing file..."
		#ensure
		# file.close unless file == nil
		
	  end
	end
end
