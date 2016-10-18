class Hotel < ActiveRecord::Base
    require 'rest_client'

    @url

    def self.formatData(hotel)
        data = {
            'name' => hotel[:name],
            'address' => hotel[:address],
            'accommodation_id' => hotel[:accommodations_id],
            'stars_rating_id' => hotel[:star_rating_id]
        }

        return data
    end

    def self.postData(params, formatData=true)
        if formatData
            params = Hotel.formatData(params)
        end

        begin
            response = RestClient.post @url, params.to_json, {content_type: :json, accept: :json}
        rescue RestClient::ExceptionWithResponse => e
            return e.response
        end
        return response
    end

    def self.getData
        begin
            return RestClient.get @url, {content_type: :json, accept: :json}
        rescue RestClient::ExceptionWithResponse => e
            return e.response
        end
        return response
    end

    def self.putData(params)
        begin
            return RestClient.put @url, Hotel.formatData(params).to_json, {content_type: :json, accept: :json}
        rescue RestClient::ExceptionWithResponse => e
            return e.response
        end
        return response
    end

    def self.deleteData
        begin
            return RestClient.delete @url, {content_type: :json, accept: :json}
        rescue RestClient::ExceptionWithResponse => e
            return e.response
        end
        return response
    end

    def self.get_all()
         @url = "http://localhost:5000/api/v1.0/hotels/"
         response = Hotel.getData
         return {'code'=> response.code}.update(JSON.parse(response))
    end

    def self.get(hotelId)
         @url = "http://localhost:5000/api/v1.0/hotels/" + hotelId
         response = Hotel.getData
         return {'code'=> response.code}.update(JSON.parse(response))
    end

    def self.delete(hotelId)
         @url = "http://localhost:5000/api/v1.0/hotels/" + hotelId
         response = Hotel.deleteData
        return {'code'=> response.code}.update(JSON.parse(response))
    end

    def self.create(hotel)
         @url = "http://localhost:5000/api/v1.0/hotels/"
         response = Hotel.postData(hotel)
         return {'code'=> response.code}.update(JSON.parse(response))
    end

    def self.update(hotelId, hotel)
         @url = "http://localhost:5000/api/v1.0/hotels/" + hotelId
         response = Hotel.putData(hotel)
        return {'code'=> response.code}.update(JSON.parse(response))
    end

    def self.get_suggestions(term)
         @url = "http://localhost:5000/api/v1.0/suggestions/"
         response = Hotel.postData(term, false)
         return {'code'=> response.code}.update(JSON.parse(response))
    end
end
