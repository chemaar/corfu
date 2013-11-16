require 'rubygems'
require 'tweetstream'
require 'yaml'
require 'json'
require 'alchemy_api'


class TweetAnalysis
   def initialize(id)
      @id=id
   end

   def id=(value)
	@id = value
   end
   def id
	@id
   end

   def rawtext=(value)
	@rawtext = value
   end
   def rawtext
	@rawtext
   end

   def polarity=(value)
	@polarity = value
   end
   def polarity
	@polarity
   end


   def score=(value)
	@score = value
   end
   def score
	@score
   end

    def keywords=(value)
	@keywords = value
   end
   def keywords
	@keywords
   end



   def language=(value)
	@language = value
   end
   def language
	@language
   end


   def status=(value)
	@status = value
   end
   def status
	@status
   end

end


AlchemyAPI.key = "1857e92fe08277fd01aefd94a53c1a7b08315068"


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
		puts "Getting tweet..."
		#Process tweet
		ta = TweetAnalysis.new (status.id)
		ta.rawtext = status.text
		results = AlchemyAPI.search(:sentiment_analysis, :text => ta.rawtext)
		ta.polarity = results['type']
		ta.score = results['score']
		results = AlchemyAPI.search(:keyword_extraction, :text => ta.rawtext)
		keywords = Hash.new 
		results.each do |result|
			keywords[result['text']] = result['relevance']
		end
		ta.keywords = keywords
		results = AlchemyAPI.search(:language_detection, :text => ta.rawtext)
		ta.language = results['language']
		ta.status = status
		#end process tweet
		file.puts ta.to_yaml
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
