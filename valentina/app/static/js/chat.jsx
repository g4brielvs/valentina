var $ = require('jquery-browserify');
var React = require('react');
var ReactDOM = require('react-dom');

// ReactJS components

var ReportButton = React.createClass({
  handleReport: function(e) {
    var pk = $(e.target).parent().parent().parent().parent().attr('id');
    var url = '/app/report/';
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: {pk : pk},
      success: function(data){
        var flash = document.createElement('div');
        flash.setAttribute('class', 'flash-success');
        flash.innerHTML = 'Muito obrigado, você está ajudando a fazer a Valentina melhor!';
        document.body.appendChild(flash);
        setTimeout(function () {
          $('div.flash-success').fadeOut(345, function(){$(this).remove();});
        }, 10000);
      }.bind(this),
      error: function(xhr, status, err){
        console.error(url, status, err.toString());
      }
    });
  },
  render: function() {
    if (this.props.className == 'me') {
      return(
        <a></a>
      );
    } else {
      return (
        React.createElement('a', {className: 'report', title: 'Reportar', onClick: this.handleReport},
          React.createElement('svg', {version: '1.1', x: '0px', y: '0px', viewBox:'0 0 16 16'},
            React.createElement('path', {d: 'M15.9,15.1L8.4,2.3C8.3,2.1,8.2,2,8,2S7.6,2.1,7.6,2.3L0.1,15.2c-0.1,0.2-0.1,0.4,0,0.5C0.2,15.9,0.3,16,0.5,16h15 c0.3,0,0.5-0.2,0.5-0.5C16,15.3,16,15.2,15.9,15.1z M8.8,14H7.2v-1.5h1.6V14z M8.8,11.3H7.2V6.6h1.6V11.3z'})
          )
        )
      );
    }
  }
});

var ChatHeading = React.createClass({
  render: function() {
    return (
      <div className="controls">
          <button>&times;</button>
          <h2>{this.props.chat.alias}</h2>
      </div>
    );
  }
});

var ChatTimeline =  React.createClass({
  render: function() {
    return (
      <div className="timeline">
        <ol>
          {this.props.messages.map(function(message){
            return (
              <li className={message.className} key={message.id} id={message.id}>
                <span className="author">
                  {message.author}
                  <ReportButton className={message.className} />
                </span>
                <p>{message.content}</p>
                <span className="ago">{message.ago}</span>
              </li>
            );
          })}
        </ol>
      </div>
    );
  }
});

var ChatForm = React.createClass({
  getInitialState: function(){
    return {message: ''};
  },
  handleMessageChange: function(e){
    this.setState({message: e.target.value});
  },
  handleKeyPress: function(e){
    var keyCode = e.key ? e.key : e.which;
    if (keyCode === "Enter") {
      this.handleSubmit(e);
    }
  },
  handleSubmit: function(e){
    e.preventDefault();
    var chat = this.props.chat.id;
    var content = this.state.message;
    if (!chat || !content) {
      return;
    }
    this.props.onMessageSubmit({content: content, chat: chat});
    this.setState({message: ''});
  },
  render: function(){
    return (
      <div className="input">
        <form onSubmit={this.handleSubmit}>
          <textarea onChange={this.handleMessageChange} onKeyPress={this.handleKeyPress} value={this.state.message}></textarea>
          <button type="submit">Enviar</button>
        </form>
      </div>
    );
  }
});

var ChatBox = React.createClass({
  getInitialState: function(){
    return {chat: this.props.chat, messages: []};
  },
  scrollToLastMessage: function (){
    $("div.timeline").each(function(){
      $(this).animate({scrollTop: $(this).prop("scrollHeight")}, 500);
    });
  },
  loadMessages: function() {
    $.ajax({
      url: this.props.chat.url,
      dataType: 'json',
      cache: false,
      success: function(data){
        this.setState({chat: data['chat'], messages: data['messages']});
        this.scrollToLastMessage();
      }.bind(this),
      error: function(xhr, status, err){
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleMessageSubmit: function(message){
    $.ajax({
      url: this.props.chat.url,
      dataType: 'json',
      type: 'POST',
      data: message,
      error: function(xhr, status, err){
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function(){
    this.loadMessages();
    setInterval(this.loadMessages, this.props.fetchInterval);
  },
  render: function() {
    return (
      <section className="col chat">
        <ChatHeading chat={this.state.chat} />
        <ChatTimeline messages={this.state.messages} />
        <ChatForm chat={this.state.chat} onMessageSubmit={this.handleMessageSubmit} />
      </section>
    );
  }
});

var ChatBoxes = React.createClass({
  getInitialState: function(){
    return {chats: this.props.chats};
  },
  render: function(){
    return(
      <div>
        {this.state.chats.map(function(chat){
          return (
            <ChatBox key={chat.key} chat={chat} fetchInterval={3000} />
          );
        })}
      </div>
    );
  }
});

// Get user chats and render ReactJS components

var get_chats = function () {
  var chats = [];
  $('li[data-chat-url]').each(function(){
    chats.push($(this).attr('data-chat-url'));
  });
  var re = /(\/app\/chat\/)(\d+)(\/)/;
  if (chats.length > 0) {
    return chats.map(function(chat){
      return {
        key: chat.replace(/\//g, ''),
        id: re.exec(chat)[2],
        url: chat
      };
    });
  }
  return chats;
};

var chat_boxes = ReactDOM.render(
  <ChatBoxes chats={get_chats()} />,
  document.getElementById('chat_panels')
);

// make render_chats available globally so users can add chat boxes from outside
global.render_chats = function () {
  var chats = get_chats();
  chat_boxes.setState({chats: chats});
};
