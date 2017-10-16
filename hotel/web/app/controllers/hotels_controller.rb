class HotelsController < ApplicationController
  def index
  end

  def all
    @results = Hotel.get_all()['hotels']
  end

  def show
    hotels = Hotel.get(params[:id])['hotels']
    if hotels.empty?
      render :status => 404
    end

    accommodations = Accommodation.get_all()
    stars = StarRating.get_all()

    @hotel = hotels[0]
    @star = stars['stars_rating'][@hotel['stars_rating_id']-1]['rating']
    @accommodation = accommodations['accommodations'][@hotel['accommodation_id']-1]['type']

    render "show"
  end

  def edit
    @accommodations = Accommodation.get_all()
    @stars = StarRating.get_all()
    @hotels = Hotel.get(params[:id])['hotels']
    render "edit"
  end

  def add
    @accommodations = Accommodation.get_all()
    @stars = StarRating.get_all()
    render "create"
  end

  def create
    Hotel.create(params)
    redirect_to hotels_all_path
  end

  def update
    @response = Hotel.update(params[:id], params)
    redirect_to hotel_path
  end

  def suggestions
    response = Hotel.get_suggestions({'term' => params[:term]})
    render json: response.to_json
  end

  def destroy
    Hotel.delete(params[:id])
    redirect_to hotels_all_path
  end
end
