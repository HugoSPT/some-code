class CreateStarRatings < ActiveRecord::Migration[5.0]
  def change
    create_table :star_ratings do |t|

      t.timestamps
    end
  end
end
