$(document).ready(function() {

    $('.nav-opener').on('click', function(e) {
        e.preventDefault();
        $(this).parent().toggleClass('nav-active');
        $('body').toggleClass('scroll-none');
    });

    $('.quotes-slider').slick({
        infinite: true,
        arrows: false,
        dots: true,
        fade: true,
        cssEase: 'linear',
        speed: 300,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        centerMode: false,
    });

    $.fancybox.defaults.closeExisting = true;
    // Contact Us Thanks Modal
    $('.contactUsThanksModal').on('click', function() {
        $.fancybox.open( $('#contactUsThanksModal'), {
            touch: false
        });
        return false;
    });
    if ($(window).scrollTop() >= 100) {
        $('.header').addClass('fixed-header');
    }
    else {
        $('.header').removeClass('fixed-header');
    }
});

$(window).on('load resize orientationchange', function() {
    if ( $(window).width() < 768 ) {
        $('.feature-list').readmore({
            speed: 1000,
            moreLink: '<a href="#" class="btn btn-grey btn-lg-br">Show all features</a>',
            lessLink: '<a href="#" class="btn btn-grey btn-lg-br">Hide all features</a>',
            heightMargin: 24
        });
    }
    else{
        $('.feature-list').readmore('destroy');
    }

});

$(window).scroll(function(){
    if ($(window).scrollTop() >= 100) {
        $('.header').addClass('fixed-header');
    }
    else {
        $('.header').removeClass('fixed-header');
    }
});