class CreateAccommodations < ActiveRecord::Migration[5.0]
  def change
    create_table :accommodations do |t|

      t.timestamps
    end
  end
end
