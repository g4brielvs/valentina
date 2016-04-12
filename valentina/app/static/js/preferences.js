const $ = require('jquery-browserify');

// DOM elements

const $preferences = $('form.preferences');
const $chatList = $('#chat_list');

// Show/hide methods

const swap = (from, to) => from.fadeOut(() => to.fadeIn());
const showPreferences = () => swap($chatList, $preferences);
const showChatList = () => swap($preferences, $chatList);

// Bind methods

$('#preferences').click(showPreferences);
$preferences.find('button[type=reset]').click(showChatList);
$preferences.find('button[type=submit]').click(function (e) {
  e.preventDefault();
  $(this).html('Salvando…').attr('disabled');
  let nickname = $preferences.find('input[name=nickname]').val();
  let url = $preferences.attr('action');
  if (nickname) {
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: { nickname: nickname },
      success: function (data) {
        $(this).removeAttr('disabled').html('Salvar');
        showChatList();
        var $main = $('main.col');
        if ($main.hasClass('first_access')) {
          firstAccessMode(false);
          $main.removeClass('first_access');
        }
      }.bind(this),
      error: function (xhr, status, err) {
        $(this).html('Salvar').removeAttr('disabled');
        console.error(url, status, err.toString());
      }.bind(this),
    });
  }
});

// Show preferences on first access

const firstAccessMode = (firstAccess) =>  {
  var label = this.find('span');
  if (firstAccess) {
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
};

const firstAccess = () =>  {
  if ($('main.col').hasClass('first_access')) {
    showPreferences();
    firstAccessMode(true);
  }
};

firstAccess();
