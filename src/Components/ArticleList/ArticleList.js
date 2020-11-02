import React, { useState } from 'react';
import './ArticleList.css';
import { Article } from '../Article/Article';
import { useGetArticles } from './useGetArticles';

export class ArticleList extends React.Component {
  handleScroll(e) {
    const bottom = e.target.scrollHeight - e.target.scrollTop === e.target.clientHeight;
    if (bottom) {

    }
  }

  render() {
    return (
      <ul>
        <div className="row">
          <div className="column">
            <Article image={this.props.category} />
            <Article image={this.props.category} />
            <Article image={this.props.category} />
            <Article image={this.props.category} />
            <Article image={this.props.category} />
          </div>
          <div className="column">
            <Article image={this.props.category} />
            <Article image={this.props.category} />
            <Article image={this.props.category} />
            <Article image={this.props.category} />
            <Article image={this.props.category} />
          </div>
        </div>
      </ul>
    )
  }
}