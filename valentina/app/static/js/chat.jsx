const $ = require('jquery-browserify');
const React = require('react');
const ReactDOM = require('react-dom');

// Hash function to gnerate temporary message IDs

String.prototype.hashCode = function () {
  let hash = 0;
  if (this.length === 0) return hash;
  for (var chr of this) {
    hash  = ((hash << 5) - hash) + chr;
    hash |= 0; // Convert to 32bit integer
  }

  return hash;
};

// ReactJS components

const ReportButton = React.createClass({
  handleReport: function (e) {
    let pk = $(e.target).parent().parent().parent().parent().attr('id');
    let url = '/app/report/';
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: { pk: pk },
      success: function (data) {
        let flash = document.createElement('div');
        flash.setAttribute('class', 'flash-success');
        flash.innerHTML = 'Muito obrigado, você está ajudando a fazer a Valentina melhor!';
        document.body.appendChild(flash);
        setTimeout(function () {
          $('div.flash-success').fadeOut(345, function () {$(this).remove();});
        }, 10000);
      }.bind(this),
      error: function (xhr, status, err) {
        console.error(url, status, err.toString());
      },
    });
  },

  render: function () {
    if (this.props.className == 'me') {
      return (
        <a></a>
      );
    } else {
      return (
        React.createElement('a', { className: 'report', title: 'Reportar', onClick: this.handleReport },
          React.createElement('svg', { version: '1.1', x: '0px', y: '0px', viewBox:'0 0 16 16' },
            React.createElement('path', { d: 'M15.9,15.1L8.4,2.3C8.3,2.1,8.2,2,8,2S7.6,2.1,7.6,2.3L0.1,15.2c-0.1,0.2-0.1,0.4,0,0.5C0.2,15.9,0.3,16,0.5,16h15 c0.3,0,0.5-0.2,0.5-0.5C16,15.3,16,15.2,15.9,15.1z M8.8,14H7.2v-1.5h1.6V14z M8.8,11.3H7.2V6.6h1.6V11.3z' })
          )
        )
      );
    }
  },
});

const ChatHeading = React.createClass({
  render: function () {
    return (
      <div className="controls">
          <button>&times;</button>
          <h2>{this.props.chat.alias}</h2>
      </div>
    );
  },
});

const ChatTimeline =  React.createClass({
  render: function () {
    return (
      <div className="timeline">
        <ol>
          {this.props.messages.map((message) => (
            <li className={message.className} key={message.id} id={message.id}>
              <span className="author">
                {message.author}
                <ReportButton className={message.className} />
              </span>
              <p>{message.content}</p>
              <span className="ago">{message.ago}</span>
            </li>
          ))}
        </ol>
      </div>
    );
  },
});

const ChatForm = React.createClass({
  getInitialState: () => ({ message: '' }),
  handleMessageChange: function (e) {
    this.setState({ message: e.target.value });
  },

  handleKeyPress: function (e) {
    let keyCode = e.key ? e.key : e.which;
    if (keyCode === 'Enter') {
      this.handleSubmit(e);
    }
  },

  handleSubmit: function (e) {
    e.preventDefault();
    let chat = this.props.chat.id;
    let author = this.props.chat.user;
    let content = this.state.message;
    if (!chat || !content) {
      return;
    }

    this.props.onMessageSubmit({ content: content, chat: chat, author: author });
    this.setState({ message: '' });
  },

  render: function () {
    return (
      <div className="input">
        <form onSubmit={this.handleSubmit}>
          <textarea value={this.state.message}
            onChange={this.handleMessageChange} onKeyPress={this.handleKeyPress}>
          </textarea>
          <button type="submit">Enviar</button>
        </form>
      </div>
    );
  },
});

const ChatBox = React.createClass({
  getInitialState: function () {
    return { chat: this.props.chat, messages: [] };
  },

  scrollToLastMessage: function () {
    $('div.timeline').each(function () {
      $(this).animate({ scrollTop: $(this).prop('scrollHeight') }, 500);
    });
  },

  loadMessages: function () {
    $.ajax({
      url: this.props.chat.url,
      dataType: 'json',
      cache: false,
      success: function (data) {
        this.setState({ chat: data.chat, messages: data.messages });
        this.scrollToLastMessage();
      }.bind(this),

      error: function (xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this),
    });
  },

  handleMessageSubmit: function (message) {

    // add a temporary message placeholder to the timeline
    let messages = this.state.messages;
    let chat = this.state.chat;
    let id = chat.user + Date.now() + message.content;
    message.ago = 'Enviando...';
    message.id = 'tmp' + id.hashCode();
    message.className = 'me';
    let tmpMessages = messages.concat([message]);
    this.setState({ chat: chat, messages: tmpMessages });

    // send message to the server
    $.ajax({
      url: this.props.chat.url,
      dataType: 'json',
      type: 'POST',
      data: { content: message.content, chat: message.chat },
      error: function (xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this),
    });

  },

  componentDidMount: function () {
    this.loadMessages();
    setInterval(this.loadMessages, this.props.fetchInterval);
  },

  render: function () {
    return (
      <section className="col chat">
        <ChatHeading chat={this.state.chat} />
        <ChatTimeline messages={this.state.messages} />
        <ChatForm chat={this.state.chat} onMessageSubmit={this.handleMessageSubmit} />
      </section>
    );
  },
});

const ChatBoxes = React.createClass({
  getInitialState: function () {
    return { chats: this.props.chats };
  },

  render: function () {
    return (
      <div>
        {this.state.chats.map((chat) => (
          <ChatBox key={chat.key} chat={chat} fetchInterval={3456} />
        ))}
      </div>
    );
  },
});

// Get user chats and render ReactJS components

const getChats = function () {
  let chats = [];
  let re = /(\/app\/chat\/)(\d+)(\/)/;

  $('li[data-chat-url]').each(function () {
    chats.push($(this).attr('data-chat-url'));
  });

  if (chats.length > 0) {
    return chats.map(function (chat) {
      return {
        key: chat.replace(/\//g, ''),
        id: re.exec(chat)[2],
        url: chat,
      };
    });
  }

  return chats;
};

const chatBoxes = ReactDOM.render(
  <ChatBoxes chats={getChats()} />,
  document.getElementById('chat_panels')
);

// make render_chats available globally so users can add chat boxes from outside
global.renderChats = function () {
  let chats = getChats();
  chatBoxes.setState({ chats: chats });
};
