$(function() {
    $("#analysis-form").submit(function(event){
    event.preventDefault();
    var post_url = $(this).attr("action");
    var request_method = $(this).attr("method");
    var form_data = $(this).serializeArray();
    var body = JSON.stringify({
        'analyzer': form_data[1]["value"],
        'text': form_data[2]["value"]
    })
    var index = form_data[0]["value"]

    post_url = ''
    $.ajax({
        url : 'http://ec2-34-201-3-67.compute-1.amazonaws.com:9200/' + index + '/_analyze',
        contentType : 'application/json',
        type : 'POST',
        data : body
    }).done(function(response){ //
        $("#server-results").html('<pre>' + JSON.stringify(response) + '</pre>');
    });
});
});