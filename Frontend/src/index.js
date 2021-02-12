import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Main from './Main';
import ReadArticle from './ReadArticle'
import * as serviceWorker from './serviceWorker';

const url = window.location.toString()

// Goes to main page if there is no 'article' after the domain name
if (url.substring(22,29) !== 'article') {
  ReactDOM.render(
    <React.StrictMode>
      <Main />
    </React.StrictMode>,
    document.getElementById('root')
  );

// Goes to the read article page if 'article' is right after the domain name
} else {
  ReactDOM.render(
    <React.StrictMode>
      <ReadArticle />
    </React.StrictMode>,
    document.getElementById('root')
  );
}


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
