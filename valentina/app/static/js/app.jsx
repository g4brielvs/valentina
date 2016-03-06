var $ = require('jquery-browserify');
var React = require('react');
var ReactDOM = require('react-dom');

var get_chats = function () {
  var body = document.getElementsByTagName('body')[0];
  var chats = body.getAttribute('data-chats');
  return chats.split(',');
};

var get_cookie = function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

var csrfSafeMethod = function (method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", get_cookie('csrftoken'));
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
                <span className="author">{message.author}</span>
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
          <textarea onChange={this.handleMessageChange}></textarea>
          <button type="submit">Enviar</button>
        </form>
      </div>
    );
  }
});

var ChatBox = React.createClass({
  getInitialState: function(){
    var chat_id = get_chats();
    var chat_details = {id: chat_id[0]};
    return {chat: chat_details, messages: []};
  },
  scrollToLastMessage: function (){
    $("div.timeline").each(function(){
      $(this).animate({scrollTop: $(this).prop("scrollHeight")}, 500);
    });
  },
  loadMessages: function() {
    $.ajax({
      url: this.props.url,
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
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: message,
      success: function(data) {
        this.setState({chat: data['chat'], messages: data['messages']});
        this.scrollToLastMessage();
      }.bind(this),
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
      <section className="col chat" key={this.state.chat.id}>
        <ChatHeading chat={this.state.chat} />
        <ChatTimeline messages={this.state.messages} />
        <ChatForm chat={this.state.chat} onMessageSubmit={this.handleMessageSubmit} />
      </section>
    );
  }
});

ReactDOM.render(
  <ChatBox url="/app/chat/1/" fetchInterval={3000} />,
  document.getElementById('chat_panels')
);
