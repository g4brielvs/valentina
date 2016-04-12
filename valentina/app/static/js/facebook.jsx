const $ = require('jquery-browserify');
const React = require('react');
const ReactDOM = require('react-dom');
const Isvg = require('react-inlinesvg');

// Pluralize method

const pluralize = (amount, str) => {
  let pluralized = amount == 1 ? str : str + 's';
  return `${amount} ${pluralized}`;
};

// React Components

const ChatsMenu = React.createClass({
  getInitialState: function () {
    return {
      chats: [],
      joinUrl: this.props.dataset.joinUrl,
      message_content: null,
      profile: {},
      searchFor: '',
      searchFormDataset: {
        facebook: this.props.dataset.facebook,
        magnifier: this.props.dataset.magnifier,
      },
      searchFormOrResultStatus: 'idle',
      searchUrl: this.props.dataset.searchUrl,
    };
  },

  componentDidMount: function () {
    this.loadChats();
  },

  loadChats: function () {
    $.ajax({
      url: '/app/chats/',
      dataType: 'json',
      cache: false,
      success: function (data) {
        this.setState({ chats: data.chats });
        global.renderChats(this.state.chats);
      }.bind(this),

      error: function (xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this),
    });
  },

  handleSearchInput: function (e) {
    this.setState({ searchFor: e.target.value });
  },

  handleSearchSubmit: function (e) {
    e.preventDefault();

    if (this.state.searchFor) {

      // set waiting message
      this.setState({ status: 'waiting' });

      // start the search
      $.ajax({
        url: this.state.searchUrl,
        dataType: 'json',
        type: 'POST',
        data: { url: this.state.searchFor },
        success: function (data) {
          if (data.error) {
            this.setState({ status: 'other', message_content: data.error });
          } else if (data.type != 'pessoa') {
            this.setState({ status: 'wrong' });
          } else {
            this.setState({ status: 'success', profile: data });
          }
        }.bind(this),

        error: (xhr, status, err) =>  {
          console.error(e.currentTarget.action, status, err.toString());
        },
      });

    }
  },

  handleAliasInput: function (e) {
    this.setState({ alias: e.target.value });
  },

  handleCreateChat: function (e) {
    e.preventDefault();
    if (this.state.alias) {
      this.setState({ status: 'creating' });
      $.ajax({
        url: this.state.joinUrl,
        dataType: 'json',
        type: 'POST',
        data: { person: this.state.profile.id, alias: this.state.alias },
        success: function (data) {
          this.loadChats();
          this.setState({ status: 'idle', searchFor: '' });
        }.bind(this),

        error: (xhr, status, err) => {
          console.error(url, status, err.toString());
        },
      });
    }
  },

  handleCancel: function (e) {
    e.preventDefault();
    this.setState({ status: 'idle', searchFor: '' });
  },

  render: function () {
    return (
      <div>
        <SearchOrResultForm
          dataset={this.state.searchFormDataset}
          message_content={this.state.message_content}
          profile={this.state.profile}
          searchFor={this.state.searchFor}
          status={this.state.status}
          handleAliasInput={this.handleAliasInput}
          handleCancel={this.handleCancel}
          handleCreateChat={this.handleCreateChat}
          handleSearchInput={this.handleSearchInput}
          handleSearchSubmit={this.handleSearchSubmit}
        />
        <ChatButtons chats={this.state.chats} />
      </div>
    );
  },
});

const SearchOrResultForm = React.createClass({
  render: function () {
    let status = this.props.status;
    if (status !== 'success') {
      let content = status === 'other' ? this.props.message_content : null;
      let message = status === 'idle' ? null : status;
      return (
        <div>
          <SearchForm
            dataset={this.props.dataset}
            searchFor={this.props.searchFor}
            handleSearchSubmit={this.props.handleSearchSubmit}
            handleSearchInput={this.props.handleSearchInput}
          />
          <div id="facebook">
            <FormMessage message={message} content={content} />
          </div>
        </div>
      );
    } else {
      let names = this.props.profile.name.split(' ');
      let label = `Apelidar a sala sobre o(a) ${names[0]} de :`;
      return (
        <div id="facebook">
          <a target="_blank" href={this.props.profile.link}>
            <img alt={this.props.profile.name} src={this.props.profile.picture} />
            <br />
            {this.props.profile.name}
          </a>
          <form onSubmit={this.props.handleCreateChat}>
            <label for="alias">{label}</label>
            <input id="alias" type="text" onChange={this.props.handleAliasInput} />
            <p>
              Esse apelido servirá para você, e só você, identificar essa sala.
              Por questões de privacidade e segurança evite usar o nome real da pessoa.
            </p>
            <button type="submit" onClick={this.props.handleSubmit}>Criar sala</button>
            <button type="reset" onClick={this.props.handleCancel}>Cancelar</button>
          </form>
        </div>
      );
    }
  },
});

const SearchForm = React.createClass({
  getInitialState: function () {
    return {
      facebook: this.props.dataset.facebook,
      magnifier: this.props.dataset.magnifier,
    };
  },

  render: function () {
    let placeholder = 'Cole a URL do Facebook do agressor';
    return (
      <form
        name="facebook-search"
        className="search-bar"
        onSubmit={this.props.handleSearchSubmit}>
        <Isvg src={this.state.facebook}></Isvg>
        <input
          type="search"
          placeholder={placeholder}
          onChange={this.props.handleSearchInput}
          value={this.props.searchFor} />
        <button type="submit"><Isvg src={this.state.magnifier}></Isvg></button>
      </form>
    );
  },
});

const FormMessage = React.createClass({
  render: function () {
    if (this.props.message === 'waiting') {
      return (
        <p>Aguarde alguns instantes enquanto procuramos o perfil da pessoa...</p>
      );
    } else if (this.props.message === 'creating') {
      return (
        <p>Aguarde, criando sala…</p>
      );
    } else if (this.props.message === 'wrong') {
      return (
        <p>
          O endereço acima não parece ser de um usuário do Facebook, mas de
          um “página” ou “grupo”.
        </p>
      );
    } else if (this.props.message === 'other') {
      return (<p>{this.props.content}</p>);
    } else {
      return (<div></div>);
    }
  },
});

const ChatButtons = React.createClass({
  render: function () {
    if (this.props.chats.length > 0) {
      return (
        <div className="chats">
          <h3>Seus grupos</h3>
          <ul>
            {this.props.chats.map((chat) => <ChatButton key={chat.key} chat={chat} />)}
          </ul>
        </div>
      );
    } else {
      return (<div></div>);
    }
  },
});

const ChatButton = React.createClass({
  render: function () {
    return (
      <li
        data-url={this.props.chat.url }
        data-key={this.props.chat.key}
        data-active={this.props.chat.active}>
        <a>
          <span className="chat_alias">{this.props.chat.alias}</span>
          <span className="users">{pluralize(this.props.chat.valentinas, 'Valentina')}</span>
        </a>
      </li>
    );
  },
});

// Render

const chatListDOM = document.getElementById('chat_list');
const chatList = ReactDOM.render(
  <ChatsMenu dataset={chatListDOM.dataset} />,
  chatListDOM
);
