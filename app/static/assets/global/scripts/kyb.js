var updateMenu = function(menuId) {
    $(menuId).children().append('<span class="selected"></span>')
    $(menuId).addClass('active open')
    $('.nav-item').not(menuId).removeClass('start active open')
    $('.nav-item').not(menuId).children().find('.selected').remove()
}