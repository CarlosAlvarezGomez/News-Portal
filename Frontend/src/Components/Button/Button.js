import React from 'react';
import './Button.css';

export const Button = (text) => {

    return (
        <button key={'Button: ' + text} onClick={() => window.location= ('https://newspalate.com/' + text).toLowerCase()}>
          {text}
        </button>
      );
}