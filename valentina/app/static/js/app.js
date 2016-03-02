var React = require('react');
var ReactDOM = require('react-dom');

var sample = [
  {
    author: 'Valentina',
    ago: '3 minutos atrás',
    content: 'Here comes the message…'
  },
  {
    author: 'Valentina',
    ago: '3 minutos atrás',
    content: 'Here comes the message…'
  },
  {
    author: 'Valentina',
    ago: '3 minutos atrás',
    content: 'Here comes the message…',
    className: 'me'
  },
  {
    author: 'Valentina',
    ago: '3 minutos atrás',
    content: 'Here comes the message…'
  },
  {
    author: 'Valentina',
    ago: '3 minutos atrás',
    content: 'Here comes the message…'
  },
  {
    author: 'Valentina',
    ago: '3 minutos atrás',
    content: 'Here comes the message…',
    className: 'me'
  },
  {
    author: 'Valentina',
    ago: '3 minutos atrás',
    content: 'Here comes the message…'
  },
];

var ChatTimeline =  React.createClass({
  render: function() {
    var messageNodes = this.props.data.map(function(message) {
      return (
        React.createElement('li', {className: message.className},
          React.createElement('span', {className: 'author'}, message.author),
          React.createElement('p', null, message.content),
          React.createElement('span', {className: 'ago'}, message.ago)
        )
      );
    });
    return (
      React.createElement('ol', null, messageNodes)
    );
  }
});

var ChatBox = React.createClass({
  render: function() {
    return (
      React.createElement('section', {className: "col chat"},
        React.createElement('div', {className: "controls"},
          React.createElement('button', null, '&times;'),
          React.createElement('h2', null, 'Fulano')
        ),
        React.createElement('div', {className: 'timeline'},
          React.createElement(ChatTimeline, {data: this.props.data})
        ),
        React.createElement('div', {className: 'input'},
          React.createElement('form', {action: '#'},
            React.createElement('textarea'),
            React.createElement('button', null, 'Enviar')
          )
        )
      )
    );
  }
});

ReactDOM.render(
  React.createElement(ChatBox, {data: sample}),
  document.getElementById('chat_panels')
);
