var React = require('react');
var ReactDOM = require('react-dom');

var chat = {alias: "Fulano", id: 'chat42'}

var messages = [
  {
    id: 'chat1',
    author: 'Valentina',
    ago: '15 minutos atrás',
    content: 'Here comes the message…'
  },
  {
    id: 'chat2',
    author: 'Valentina',
    ago: '12 minutos atrás',
    content: 'Here comes the message…'
  },
  {
    id: 'chat3',
    author: 'Valentina',
    ago: '9 minutos atrás',
    content: 'Here comes the message…',
    className: 'me'
  },
  {
    id: 'chat4',
    author: 'Valentina',
    ago: '7 minutos atrás',
    content: 'Here comes the message…'
  },
  {
    id: 'chat5',
    author: 'Valentina',
    ago: '5 minutos atrás',
    content: 'Here comes the message…'
  },
  {
    id: 'chat6',
    author: 'Valentina',
    ago: '2 minutos atrás',
    content: 'Here comes the message…',
    className: 'me'
  },
  {
    id: 'chat7',
    author: 'Valentina',
    ago: '1 minutos atrás',
    content: 'Here comes the message…'
  },
];

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
              <li className="{message.className}" key={message.id} id={message.id}>
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
  render: function() {
    return (
      <section className="col chat" key={this.props.chat.id} id={this.props.chat.id}>
        <ChatHeading chat={this.props.chat} />
        <ChatTimeline messages={this.props.messages} />
        <ChatForm chat={this.props.chat} />
      </section>
    );
  }
});

ReactDOM.render(
  <ChatBox messages={messages} chat={chat} />,
  document.getElementById('chat_panels')
);
