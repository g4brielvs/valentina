var $ = require('jquery-browserify');

var preferences = $('form.preferences');
var chat_list = $('nav.chat_list');

var swap = function (from, to) {
  from.fadeOut(function(){
    to.fadeIn();
  });
};

var show_preferences = function (){
  swap(chat_list, preferences);
};

var show_chat_list = function () {
  swap(preferences, chat_list);
};

$('#preferences').click(show_preferences);

preferences.find('button[type=reset]').click(show_chat_list);

preferences.find('button[type=submit]').click(function(e){
  e.preventDefault();
  $(this).attr('disabled');
  $(this).html('Salvando…');
  var nickname = preferences.find('input[name=nickname]').val();
  var url = preferences.attr('action');
  if (nickname) {
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: {nickname: nickname},
      success: function(data) {
        $(this).removeAttr('disabled').html('Salvar');
        show_chat_list();
        var main = $('main.col');
        if (main.hasClass('first_access')) {
          first_access_mode(false);
          main.removeClass('first_access');
        }
      }.bind(this),
      error: function(xhr, status, err){
        $(this).removeAttr('disabled')
        $(this).html('Salvar');
        console.error(url, status, err.toString());
      }.bind(this)
    });
  }
});

var first_access_mode = function (first_access) {
  var label = this.find('span');
  if (first_access) {
    $('#preferences').hide();
    this.find('button[type=reset]').hide();
    this.find('h3').hide();
    label.html(label.html().replace('é', 'será'));
  } else {
    $('#preferences').show();
    this.find('button[type=reset]').show();
    this.find('h3').show();
    label.html(label.html().replace('será', 'é'));
  }
}.bind(preferences);

var first_access = function () {
  if ($('main.col').hasClass('first_access')) {
    show_preferences();
    first_access_mode(true);
  }
};

first_access();
