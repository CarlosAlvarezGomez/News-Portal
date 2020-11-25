import React from 'react';
import './Button.css';

export const Button = (setCategory, text) => {

    return (
      <button
        onClick={
          () => { setCategory(text.toLowerCase()) }}>
        {text}
      </button>);
}