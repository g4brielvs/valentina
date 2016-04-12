const $ = require('jquery-browserify');
const React = require('react');
const ReactDOM = require('react-dom');
const Isvg = require('react-inlinesvg');

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

    // flash id
    let flashId = `report-${this.props.messageKey}`;

    // show “sending report” message
    let sending = document.createElement('div');
    sending.setAttribute('class', 'flash-info');
    sending.setAttribute('id', flashId);
    sending.innerHTML = 'Aguarde, reportando a mensagem…';
    document.body.appendChild(sending);

    // send report
    let key = this.props.messageKey;
    let url = '/app/report/';
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: { key: this.props.messageKey },
      success: function (data) {
        let flash = document.getElementById(flashId);
        flash.setAttribute('class', 'flash-success');
        flash.innerHTML = 'Muito obrigado, você está ajudando a fazer a Valentina melhor!';
        setTimeout(function () {
          $(flash).fadeOut(345, function () {$(this).remove();});
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
        <a onClick={this.handleReport}>
          <Isvg src={this.props.svg}></Isvg>
        </a>
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
            <li className={message.className} key={message.key}>
              <span className="author">
                {message.author}
                <ReportButton
                  className={message.className}
                  messageKey={message.key}
                  svg={this.props.report}
                />
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
    let key = chat.user + Date.now() + message.content;
    message.ago = 'Enviando...';
    message.key = 'tmp' + key.hashCode();
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
        <ChatTimeline messages={this.state.messages} report={this.props.report} />
        <ChatForm chat={this.state.chat} onMessageSubmit={this.handleMessageSubmit} />
      </section>
    );
  },
});

const ChatBoxes = React.createClass({
  getInitialState: function () {
    return { chats: this.props.chats, report: this.props.report };
  },

  render: function () {
    return (
      <div>
        {this.state.chats.map((chat) => (
          <ChatBox key={chat.key} chat={chat} report={this.state.report} fetchInterval={3456} />
        ))}
      </div>
    );
  },
});

// Get user chats and render ReactJS components

const chatBoxesDOM = document.getElementById('chat_panels');
const chatBoxes = ReactDOM.render(
  <ChatBoxes chats={[]} report={chatBoxesDOM.dataset.report} />,
  chatBoxesDOM
);

// make render_chats available globally
// (so loadChats, from facebook.jsx, can call it once user add/delete chats)

global.renderChats = function (chats) {
  chatBoxes.setState({ chats: chats.filter((chat) => chat.active) });
};
