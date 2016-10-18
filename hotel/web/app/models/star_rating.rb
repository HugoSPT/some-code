class StarRating < ActiveRecord::Base
	require 'rest_client'

    @url

    def self.getData
        response = RestClient.get @url, {content_type: :json, accept: :json}
    end

    def self.get_all()
         @url = "http://localhost:5000/api/v1.0/stars_rating/"
        JSON.parse(StarRating.getData)
    end
end
