

$('.close_button a').onclick(function(){
     $(this).parent(".close_button").hide(); // something like that
$.ajax{
            url: "{% url 'app_label:view_name' %}",
            data: {'data':$(this).data("pk")},
            method: "POST",
            success: function (result,status,xhr) {

                alert('closed Successfully.');

            },

})