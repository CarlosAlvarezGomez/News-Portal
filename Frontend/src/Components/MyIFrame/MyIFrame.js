import React from 'react';
import './MyIFrame.css';

export const MyIFrame = (url) => {

    let xhr = new XMLHttpRequest();
    xhr.open('get', url);
    xhr.send();

    xhr.onload = function() {
        console.log(xhr.response);
    };

    const parseHtml = html => new DOMParser().parseFromString(html, 'text/html').body.innerText;
    return (
        
        <iframe src={url}></iframe>
      );
}