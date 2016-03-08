var $ = require('jquery-browserify'); 
var response = $('#facebook');
var waiting = 'Aguarde alguns instantes enquanto procuramos o perfil da pessoa...';
var wrong_type = 'O endereço acima não parece ser de um usuário do Facebook, mas de um “página” ou “grupo”.';

var facebook_search = function (e) {
  e.preventDefault();
  var url = $(e.currentTarget).find('input[name=url]').val();
  if (url) {
    show_message(waiting);
    $.ajax({
      url: e.currentTarget.action,
      dataType: 'json',
      type: 'POST',
      data: {url: url},
      success: function(data){
        if (data.error) {
          show_message(data.error);
        } else if (data.type != 'pessoa') {
          show_message(wrong_type);
        } else {
          show_facebook_profile(data);
        }
      },
      error: function(xhr, status, err){
        console.error(e.currentTarget.action, status, err.toString());
      }
    });
  }
};

var create_profile_card = function (data) {
  var link = document.createElement('a');
  var avatar = document.createElement('img');
  link.setAttribute('target', '_blank');
  link.setAttribute('href', data.link)
  avatar.setAttribute('alt', data.name);
  avatar.setAttribute('src', data.picture);
  link.appendChild(avatar);
  link.appendChild(document.createElement('br'));
  link.appendChild(document.createTextNode(data.name));
  return link;
};

var create_add_form = function (data) {
  var names = data.name.split(' ');
  var form = document.createElement('form');
  var label = document.createElement('label');
  var alias = document.createElement('input');
  var why = document.createElement('p');
  var person = document.createElement('input');
  var add = document.createElement('button');
  var cancel = document.createElement('button');
  form.setAttribute('method', 'post');
  form.setAttribute('action', '/app/join/');
  label.innerHTML = 'Apelidar a sala sobre o(a) ' + names[0] + ' de:';
  alias.setAttribute('type', 'text');
  alias.setAttribute('name', 'alias');
  why.innerHTML = 'Esse apelido servirá para você, e só você, identificar essa sala. Por questões de privacidade e segurança evite usar o nome real da pessoa.'
  person.setAttribute('type', 'hidden');
  person.setAttribute('name', 'person');
  person.setAttribute('value', data.id);
  add.setAttribute('type', 'submit');
  add.innerHTML = 'Criar sala'
  cancel.setAttribute('type', 'reset');
  cancel.innerHTML = 'Cancelar';
  form.appendChild(label);
  form.appendChild(person);
  form.appendChild(alias);
  form.appendChild(why);
  form.appendChild(add);
  form.appendChild(cancel);
  return form;
};

var bind_buttons = function(){
  
  // bind cancel
  this.find('button[type=reset]').click(function(e){
    this.empty();
    $('input[name=url]').val('');
  }.bind(this));

  // bind add
  this.find('button[type=submit]').click(function(e){
    e.preventDefault();
    var person = this.find('input[name=person]').val();
    var alias = this.find('input[name=alias]').val();
    var url = $(e.currentTarget).parent().attr('action');
    var data = {person: person, alias: alias};
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: data,
      success: function(data){

        var li = document.createElement('li');
        var anchor = document.createElement('a');
        var alias = document.createElement('span');
        var valentinas = document.createElement('span');

        li.setAttribute('data-chat-url', data.url);
        alias.setAttribute('class', 'chat_alias');
        alias.innerHTML = data.alias
        valentinas.setAttribute('class', 'users');
        valentinas.innerHTML = data.valentinas + ' Valentina';
        if (data.valentinas > 1) {
          valentinas.innerHTML += 's';
        }

        anchor.appendChild(alias);
        anchor.appendChild(valentinas);
        li.appendChild(anchor);

        var chat_ul = $(this).parent().find('div.chats').find('ul').first();
        chat_ul.append(li).removeClass('hidden');
        global.render_chats();

      }.bind(this),
      error: function(xhr, status, err){
        console.error(url, status, err.toString());
      }
    });
    this.empty();
    $('input[name=url]').val('');
  }.bind(this));

}.bind(response);

var show_facebook_profile = function (data) {
  var card = create_profile_card(data);
  var form = create_add_form(data);
  this.empty().append(card).append(form);
  bind_buttons();
}.bind(response);

var show_message = function (text) {
  var warning = document.createElement('p');
  warning.innerHTML = text;
  this.empty();
  this.append(warning);
}.bind(response);

$('form[name=facebook-search]').submit(facebook_search);
