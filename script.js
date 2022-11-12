$(document).ready(function(){
    $("#guideButton").css('opacity', '0');
    $("#repoButton").css('opacity', '0');
    $("#tabcpp-title").css('opacity', '0');
    $("#description").css('opacity', '0');
    $("#tabcpp-title").animate({opacity: 1}, 2000);
    $("#guideButton").delay(1000).animate({opacity: 1}, 1000);
    $("#repoButton").delay(1500).animate({opacity: 1}, 1000);
    $("#description").delay(2500).animate({opacity: 1}, 2000);
});
