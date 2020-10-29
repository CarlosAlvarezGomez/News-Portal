import React from 'react';
import './Article.css';

export class Article extends React.Component {
  render() {
    return (
      <div className="article">
        <div className="text">
          <h3>Main Headline Goes Here</h3>
          <h6>Author And Date Go Here</h6>
          <h5>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in volupt</h5>
        </div>
        <div className="image">
          <img src={require("../../Images/" + this.props.image + ".jpg")} />
        </div>
      </div>
    );
  }
}