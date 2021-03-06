/*-------------------------------------------------------------------------------*/


/*-------------------------------------------------------------------------------*/
// 클릭시 이동
$(document).ready(function () {
    // 위로
    /*
    $(function () {
      $('#upper').click(function () {
        $('body, html').animate({ scrollTop: 0 }, 800);//800 : 0.8초동안 이동
        return false;
      });
    });
    */
    // 밑으로
    var scrollHeight = $('.chk_upd_section').outerHeight();	//높이
    $('.next_btn').click(function () {
        $('body, html').animate({ scrollTop: scrollHeight*1.2}, 800);
        return false;
    });
    $('.next_btn_1').click(function () {
        $('body, html').animate({ scrollTop: scrollHeight*2.2}, 800);
        return false;
    });
    $('.next_btn_2').click(function () {
        $('body, html').animate({ scrollTop: scrollHeight*3.2}, 800);
        return false;
    });
    $('.next_btn_3').click(function () {
        $('body, html').animate({ scrollTop: scrollHeight*4.2}, 800);
        return false;
    });
    $('.next_btn_4').click(function () {
        $('body, html').animate({ scrollTop: scrollHeight*5.2}, 800);
        return false;
    });
});
