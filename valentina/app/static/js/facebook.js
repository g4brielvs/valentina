let $ = require('jquery-browserify');
let $response = $('#facebook');
let waiting = 'Aguarde alguns instantes enquanto procuramos o perfil da pessoa...';
let wrongType = 'O endereço acima não parece ser de um usuário do Facebook, mas de um “página” ou “grupo”.';

var facebookSearch = (e) =>  {
  e.preventDefault();
  var url = $(e.currentTarget).find('input[name=url]').val();
  if (url) {
    showMessage(waiting);
    $.ajax({
      url: e.currentTarget.action,
      dataType: 'json',
      type: 'POST',
      data: { url: url },
      success: (data) =>  {
        if (data.error) {
          showMessage(data.error);
        } else if (data.type != 'pessoa') {
          showMessage(wrongType);
        } else {
          showFacebookProfile(data);
        }
      },

      error: (xhr, status, err) =>  {
        console.error(e.currentTarget.action, status, err.toString());
      },
    });
  }
};

const createProfileCard = (data) =>  {
  let link = document.createElement('a');
  let avatar = document.createElement('img');
  link.setAttribute('target', '_blank');
  link.setAttribute('href', data.link);
  avatar.setAttribute('alt', data.name);
  avatar.setAttribute('src', data.picture);
  link.appendChild(avatar);
  link.appendChild(document.createElement('br'));
  link.appendChild(document.createTextNode(data.name));
  return link;
};

const createAddForm = (data) =>  {
  let names = data.name.split(' ');
  let form = document.createElement('form');
  let label = document.createElement('label');
  let alias = document.createElement('input');
  let why = document.createElement('p');
  let person = document.createElement('input');
  let add = document.createElement('button');
  let cancel = document.createElement('button');
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
  add.innerHTML = 'Criar sala';
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

const bindButtons = function () {

  // bind cancel
  this.find('button[type=reset]').click(function (e) {
    this.empty();
    $('input[name=url]').val('');
  }.bind(this));

  // bind add
  this.find('button[type=submit]').click(function (e) {
    e.preventDefault();
    let person = this.find('input[name=person]').val();
    let alias = this.find('input[name=alias]').val();
    let url = $(e.currentTarget).parent().attr('action');
    let data = { person: person, alias: alias };
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: data,
      success: function (data) {

        let li = document.createElement('li');
        let anchor = document.createElement('a');
        let alias = document.createElement('span');
        let valentinas = document.createElement('span');

        li.setAttribute('data-chat-url', data.url);
        alias.setAttribute('class', 'chatAlias');
        alias.innerHTML = data.alias;
        valentinas.setAttribute('class', 'users');
        valentinas.innerHTML = data.valentinas + ' Valentina';
        if (data.valentinas > 1) valentinas.innerHTML += 's';
        anchor.appendChild(alias);
        anchor.appendChild(valentinas);
        li.appendChild(anchor);

        let chatUl = $(this).parent().find('div.chats').find('ul').first();
        chatUl.append(li).removeClass('hidden');
        global.renderChats();

      }.bind(this),

      error: (xhr, status, err) => {
        console.error(url, status, err.toString());
      },
    });
    this.empty();
    $('input[name=url]').val('');
  }.bind(this));

}.bind($response);

const showFacebookProfile = function (data) {
  let card = createProfileCard(data);
  let form = createAddForm(data);
  this.empty().append(card).append(form);
  bindButtons();
}.bind($response);

const showMessage = function (text) {
  let warning = document.createElement('p');
  warning.innerHTML = text;
  this.empty();
  this.append(warning);
}.bind($response);

$('form[name=facebook-search]').submit(facebookSearch);
