var address_fields = [
    '#archetypes-fieldname-address',
    '#archetypes-fieldname-zip',
    '#archetypes-fieldname-city',
    '#archetypes-fieldname-phone_office',
    '#archetypes-fieldname-phone_mobile',
    '#archetypes-fieldname-fax',
    '#archetypes-fieldname-email',
    '#archetypes-fieldname-www'
];

function show_fields() {
    $.each(address_fields, function(index, value) {
        $(value).show();
    });
}

function hide_fields() {
    $.each(address_fields, function(index, value) {
        $(value).hide();
    });
}

$(document).ready(function(){

    if($('#acquireAddress').attr('checked')) {
        hide_fields();
    }

    $('#acquireAddress').live("click", function() {
        if (this.checked) {
            hide_fields();
        }
        else {
            show_fields();
        }
    });
});
