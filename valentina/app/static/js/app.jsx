var $ = require('jquery-browserify');
var React = require('react');
var ReactDOM = require('react-dom');

var get_chats = function () {
  var body = document.getElementsByTagName('body')[0];
  var chats = body.getAttribute('data-chats');
  return chats.split(',');
};

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
    render: function(){
      return (
        <div className="input">
          <form action="#" method="post">
            <textarea></textarea>
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
  loadMessages: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data){
        this.setState({chat: data['chat'], messages: data['messages']});
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
        <ChatForm chat={this.state.chat} />
      </section>
    );
  }
});

ReactDOM.render(
  <ChatBox url="/app/chat/1" fetchInterval={3000} />,
  document.getElementById('chat_panels')
);
