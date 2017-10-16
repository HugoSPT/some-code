Rails.application.routes.draw do
    root 'hotels#index'
    get 'hotels/add'
    post 'hotels/suggestions'
    get 'hotels/all'

    resources :hotels do
        member do
            get 'show'
            get 'edit'
            post 'update'
            post 'create'
        end
    end
end
