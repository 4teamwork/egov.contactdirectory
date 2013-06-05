$(document).ready(function(){

    $('#acquireAddress').live("click", function() {
        if (this.checked) {
            $('#archetypes-fieldname-address').hide();
        }
        else {
            $('#archetypes-fieldname-address').show();
        }
    });
});

// archetypes-fieldname-zip
// archetypes-fieldname-city
// archetypes-fieldname-phone_office
// archetypes-fieldname-phone_mobile
// archetypes-fieldname-fax
// archetypes-fieldname-email
// archetypes-fieldname-www