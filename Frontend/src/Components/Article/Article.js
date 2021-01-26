import React from 'react';
import './Article.css';

function addImage(imgLink) {
  if (imgLink != "") {
    return (
      <div className="image">
        <img src={imgLink} />
      </div>
    )}
}

export function Article(art) {
  console.log(art)
  return (
    <div className="article" href={art.Link}>
      <div className="textGroup">
        <h3 className="text">{art.Headline}</h3>
        <h6 className="text">By {art.Author}</h6>
        <h6 className="text">Updated {art.UpdateTime.substring(0,20)}</h6>
        <h4 className="text">{art.SubHeadline}</h4>
      </div>
      {addImage(art.Image)}
    </div>
  );
}