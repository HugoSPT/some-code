class Accommodation < ActiveRecord::Base
	require 'rest_client'

    @url

    def self.getData
        response = RestClient.get @url, {content_type: :json, accept: :json}
    end

    def self.get_all()
         @url = "http://localhost:5000/api/v1.0/accommodations/"
        JSON.parse(Accommodation.getData)
    end
end
