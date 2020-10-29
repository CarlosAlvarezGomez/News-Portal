import React from 'react';
import './Button.css';

export class Button extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <button
        onClick={
          () => { this.props.handleOnClick(this.props.text.toLowerCase()) }}>
        {this.props.text}
      </button>);
  }
}