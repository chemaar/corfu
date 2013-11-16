require 'rubygems'
require 'alchemy_api'
require 'json'

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



end


AlchemyAPI.key = "1857e92fe08277fd01aefd94a53c1a7b08315068"
ta = TweetAnalysis.new ("1")
ta.rawtext = "This is a very good product"
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
puts ta.inspect
