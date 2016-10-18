var HotelsSearchBuilder = (function() {

    'use strict';

    var xhr = null;
    var term = null;

    function HotelsSearchBuilder() {
        this.$element = $('.search');
        this.$results = $('.results');
        this.setEventHandlers();
    };

    HotelsSearchBuilder.prototype.loadSuggestions = function() {
        this.$searchTerm = this.$element.find('.search').closest('input[type=text]');
        this.ajaxRequest(this.$searchTerm);
    }

    HotelsSearchBuilder.prototype.ajaxRequest = function(term) {
        var self = this;

        this.show('loading');

        if (xhr != null) {
            this.handleAbort();
        }        
        xhr = $.ajax({
            url: '/hotels/suggestions',
            method: 'POST',
            data: { 'term': term },
            success: function (data) {
                self.handleSuccess(data['suggestions']);
            },
            error: function (data, textStatus) {
                self.handleError(textStatus);
            },
            statusCode: {
                500: function() {
                    self.handleError(500);
                }
            }
        });
    }

    HotelsSearchBuilder.prototype.show = function(divClass) {
        this.$results.find('> div').hide();
        this.$results.find('.' + divClass).show()
    };

    HotelsSearchBuilder.prototype.handleSuccess = function(suggestions) {
        if (suggestions == null || suggestions.length == 0) {
            this.show('no-suggestions');
            return;
        }

        this.show('matches');
        var suggestionsList = this.$results.find('.matches .entries').empty();

        for (var i = 0; i < suggestions.length; i++) {
            suggestionsList.append(
                $('<div class="entry"/>')
            ).append(
                $('<a href="/hotels/' + suggestions[i]['id'] + '/show/"/>'
            ).append(suggestions[i]['name']))
        }
    }

    HotelsSearchBuilder.prototype.handleError = function(textStatus) {
        this.show('api-error');
    }

    HotelsSearchBuilder.prototype.handleAbort = function() {
        xhr.abort();
        this.show('loading');
    }

    HotelsSearchBuilder.prototype.loadPreview = function() {
        this.ajaxRequest(this.$element.find('input#search_term').val());
    }

    HotelsSearchBuilder.prototype.setEventHandlers = function() {
        var self = this;

        $('input#search_term').on('keyup', function(e) {
            if ($('input#search_term').val() != term && $('input#search_term').val().length > 3) {
                term = $('input#search_term').val();
                debouncePreview();
            }
        });

        var debouncePreview = $.debounce(500, function() {
            self.loadPreview();
        });
    };

    return HotelsSearchBuilder;
})();

$(document).ready(function(){
    new HotelsSearchBuilder();
});
