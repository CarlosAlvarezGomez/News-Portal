import React from 'react';
import './Article.css';

export function Article(art, index, columnName) {
  if (((columnName === 'left') && (index%2 === 0)) || ((columnName === 'right') && (index%2 === 1))){
    return;
  }

  if (art.Image !== "") {
    return (
      <a href={art.Link}>
        <div className="article">
          <div className="textGroup1">
            <h3 className="text">{art.Headline}</h3>
            <h6 className="text">By {art.Author}</h6>
            <h6 className="text">Updated {art.UpdateTime.substring(0,20)}</h6>
            <h4 className="text">{art.SubHeadline}</h4>
          </div>
          <div className="image">
            <img src={art.Image} alt='Not Found' />
          </div>
        </div>
      </a>
    );
  } else {
    return (
      <a href={art.Link}>
        <div className="article">
          <div className="textGroup2">
            <h3 className="text">{art.Headline}</h3>
            <h6 className="text">By {art.Author}</h6>
            <h6 className="text">Updated {art.UpdateTime.substring(0,20)}</h6>
            <h4 className="text">{art.SubHeadline}</h4>
          </div>
        </div>
      </a>
    );
  }

  
}