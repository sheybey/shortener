(function () {
  'use strict';
  var container;

  function dismiss(event) {
    var row = event.target.parentNode;
    event.target.removeEventListener('click', dismiss);
    row.parentNode.removeChild(row);
  }

  function close_button() {
    var close = document.createElement('span');
    close.textContent = '\u00d7';
    close.classList.add('close');
    close.title = 'Dismiss';
    close.addEventListener('click', dismiss);
    return close;
  }

  window.message = function (text, klass) {
    var row = document.createElement('div');
    var message = document.createElement('p');

    message.textContent = text;

    row.classList.add('row');
    row.classList.add('message');
    row.classList.add(klass);
    row.appendChild(message);
    row.appendChild(close_button());

    container.insertBefore(row, container.firstChild);
  }

  document.addEventListener('DOMContentLoaded', function () {
    container = document.querySelector('.container');
    container.querySelectorAll('.message').forEach(function (message) {
      message.appendChild(close_button());
    });
  });
}());
