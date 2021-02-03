import React from 'react';
import './Button.css';

export const Button = (text) => {

    return (
        <button key={'Button: ' + text} onClick={() => window.location= ('http://localhost:3000/' + text).toLowerCase()}>
          {text}
        </button>
      );
}